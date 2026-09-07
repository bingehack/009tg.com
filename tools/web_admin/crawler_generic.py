#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用导航站抓取脚本
功能：输入任意导航站URL，自动识别结构并抓取工具站点
支持：服务端渲染站、纯JS渲染站（尝试查找data.json）
输出：标准格式JSON（categories + sites），输出到stdout
"""

import sys
import os
import json
import re
import time
import hashlib
from urllib.parse import urlparse, urljoin, urlunparse
from datetime import datetime

try:
    import requests
except ImportError:
    print('ERROR: 缺少requests库，请运行: pip install requests')
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('ERROR: 缺少beautifulsoup4库，请运行: pip install beautifulsoup4')
    sys.exit(1)

# 配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

TIMEOUT = 15
MAX_RETRIES = 2

def normalize_url(url):
    """规范化URL"""
    if not url:
        return ''
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    # 去除追踪参数
    parsed = urlparse(url)
    clean_params = []
    if parsed.query:
        for param in parsed.query.split('&'):
            if param and not param.lower().startswith(('utm_', 'ref=', 'channel=', 'from=', 'spm=')):
                clean_params.append(param)
    clean_query = '&'.join(clean_params)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, clean_query, ''))

def get_domain(url):
    """提取域名"""
    try:
        domain = urlparse(url).hostname.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return ''

def fetch_page(url):
    """抓取页面，带重试"""
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False, allow_redirects=True)
            resp.encoding = resp.apparent_encoding or 'utf-8'
            return resp.text, resp.url
        except requests.exceptions.SSLError:
            try:
                resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False, allow_redirects=True)
                resp.encoding = resp.apparent_encoding or 'utf-8'
                return resp.text, resp.url
            except Exception as e:
                if attempt < MAX_RETRIES:
                    time.sleep(2)
                    continue
                print(f'ERROR: SSL错误 - {e}')
                return None, url
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES:
                time.sleep(2)
                continue
            print(f'ERROR: 连接超时 - {url}')
            return None, url
        except Exception as e:
            if attempt < MAX_RETRIES:
                time.sleep(2)
                continue
            print(f'ERROR: 抓取失败 - {e}')
            return None, url
    return None, url

def try_find_js_data(html, base_url):
    """尝试从JS中查找数据（纯JS渲染站）"""
    # 1. 查找内联的JS数据数组
    patterns = [
        r'(?:const|let|var)\s+(?:allSites|sites|siteList|dataList|tools|websiteList)\s*=\s*(\[.*?\]);',
        r'(?:const|let|var)\s+(?:allData|appData|pageData)\s*=\s*(\{.*?\});',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                if isinstance(data, list) and len(data) > 0:
                    return data, 'inline_js_array'
                elif isinstance(data, dict) and 'sites' in data:
                    return data['sites'], 'inline_js_object'
            except:
                continue

    # 2. 查找data.json或类似的API
    api_patterns = [
        r'["\']([^"\']*data\.json[^"\']*)["\']',
        r'["\']([^"\']*api/[^"\']*(?:sites|list|data)[^"\']*)["\']',
        r'fetch\(["\']([^"\']+)["\']',
        r'axios\.(?:get|post)\(["\']([^"\']+)["\']',
    ]
    for pattern in api_patterns:
        matches = re.findall(pattern, html)
        for api_url in matches:
            if api_url.startswith('/'):
                api_url = urljoin(base_url, api_url)
            elif not api_url.startswith('http'):
                api_url = urljoin(base_url, '/' + api_url)
            if 'json' in api_url.lower() or 'api' in api_url.lower() or 'data' in api_url.lower():
                try:
                    resp = requests.get(api_url, headers=HEADERS, timeout=TIMEOUT, verify=False)
                    if resp.status_code == 200:
                        data = resp.json()
                        if isinstance(data, list) and len(data) > 0:
                            return data, 'api_json'
                        elif isinstance(data, dict):
                            for key in ['sites', 'data', 'list', 'items', 'websites']:
                                if key in data and isinstance(data[key], list) and len(data[key]) > 0:
                                    return data[key], 'api_json_object'
                except:
                    continue

    return None, None

def parse_server_rendered(html, base_url):
    """解析服务端渲染的页面"""
    soup = BeautifulSoup(html, 'html.parser')
    sites = []
    categories = []

    # 常见的工具卡片选择器
    card_selectors = [
        '.site-item', '.website-item', '.tool-item', '.card-item',
        '.app-item', '.link-item', '.nav-item', '.url-item',
        '.site-card', '.website-card', '.tool-card',
        'li.site', 'li.website', 'li.tool', 'li.app',
        '.item-box', '.site-box', '.web-box',
        'a[class*="site"]', 'a[class*="web"]', 'a[class*="tool"]',
        '.card', '.item',
    ]

    # 查找分类
    category_selectors = [
        '.category-title', '.cat-title', '.group-title', '.section-title',
        'h2.category', 'h3.category', 'h2.cat', 'h3.cat',
        '.category-name', '.cat-name', '.group-name',
        'h2', 'h3', 'h4',
    ]

    # 策略1：按分类区块解析
    # 查找包含标题和卡片的区块
    sections = soup.select('.category, .cat-group, .group, .section, .category-section')
    if not sections:
        # 尝试用标题+后续卡片的方式
        all_headings = soup.find_all(['h2', 'h3', 'h4'])
        current_category = '未分类'
        for heading in all_headings:
            heading_text = heading.get_text(strip=True)
            if heading_text and len(heading_text) < 30:
                current_category = heading_text
                if current_category not in [c['name'] for c in categories]:
                    categories.append({'name': current_category, 'count': 0})

            # 查找标题后面的卡片
            next_sibling = heading.find_next_sibling()
            while next_sibling:
                cards = next_sibling.select(', '.join(card_selectors[:15]))
                for card in cards:
                    site = extract_site_from_card(card, base_url, current_category)
                    if site:
                        sites.append(site)
                next_sibling = next_sibling.find_next_sibling()
                if next_sibling and next_sibling.name in ['h2', 'h3', 'h4']:
                    break

    # 策略2：直接查找所有卡片
    if len(sites) < 10:
        sites = []
        categories = []
        for selector in card_selectors[:20]:
            cards = soup.select(selector)
            if len(cards) >= 5:
                for card in cards:
                    site = extract_site_from_card(card, base_url, '未分类')
                    if site:
                        sites.append(site)
                if len(sites) >= 5:
                    break

    # 去重
    unique_sites = []
    seen_domains = set()
    for site in sites:
        domain = get_domain(site['url'])
        if domain and domain not in seen_domains:
            seen_domains.add(domain)
            unique_sites.append(site)
        elif not domain:
            unique_sites.append(site)

    # 统计分类
    cat_counts = {}
    for site in unique_sites:
        cat = site.get('category', '未分类')
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    categories = [{'name': k, 'count': v} for k, v in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)]

    return unique_sites, categories

def extract_site_from_card(card, base_url, default_category):
    """从卡片元素中提取站点信息"""
    # 查找链接
    link = card.find('a', href=True)
    if not link:
        return None

    url = link['href']
    if url.startswith('/') or url.startswith('#') or 'javascript:' in url:
        # 可能是跳转链接，尝试从data属性获取真实URL
        for attr in ['data-url', 'data-href', 'data-link', 'data-site', 'data-original-url', 'data-real-url']:
            if attr in link.attrs:
                url = link[attr]
                break
        else:
            # 尝试从卡片的data属性获取
            for attr in ['data-url', 'data-href', 'data-link']:
                if attr in card.attrs:
                    url = card[attr]
                    break

    if not url or url.startswith('#') or 'javascript:' in url or url == '/':
        return None

    # 相对URL转绝对URL
    if url.startswith('/'):
        url = urljoin(base_url, url)
    elif not url.startswith('http'):
        url = 'https://' + url

    url = normalize_url(url)

    # 提取名称
    name = ''
    name_selectors = ['.site-name', '.website-name', '.tool-name', '.app-name', '.title', 'h3', 'h4', '.name']
    for selector in name_selectors:
        el = card.select_one(selector)
        if el:
            name = el.get_text(strip=True)
            break
    if not name:
        name = link.get_text(strip=True)
    if not name:
        # 尝试从img的alt属性
        img = card.find('img')
        if img and img.get('alt'):
            name = img['alt']
    if not name or len(name) > 100:
        return None

    # 清理名称
    name = re.sub(r'[\n\r\t]', ' ', name).strip()
    name = re.sub(r'\s+', ' ', name)

    # 提取描述
    description = ''
    desc_selectors = ['.site-desc', '.website-desc', '.tool-desc', '.app-desc', '.description', '.desc', '.summary', 'p']
    for selector in desc_selectors:
        el = card.select_one(selector)
        if el:
            description = el.get_text(strip=True)
            if description:
                break
    if description and len(description) > 200:
        description = description[:200] + '...'

    # 提取分类
    category = default_category
    cat_el = card.select_one('.category, .cat, .tag')
    if cat_el:
        cat_text = cat_el.get_text(strip=True)
        if cat_text and len(cat_text) < 30:
            category = cat_text

    return {
        'name': name,
        'url': url,
        'description': description,
        'category': category,
        'icon': '',
    }

def crawl(url):
    """主抓取函数"""
    print(f'开始抓取: {url}')
    print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    # 抓取页面
    html, final_url = fetch_page(url)
    if not html:
        print('ERROR: 无法抓取页面')
        return None

    print(f'页面大小: {len(html)} 字节')
    print(f'最终URL: {final_url}')

    base_url = final_url

    # 尝试查找JS数据
    js_data, data_source = try_find_js_data(html, base_url)
    sites = []
    categories = []

    if js_data:
        print(f'发现JS数据 ({data_source})，共 {len(js_data)} 条')
        # 解析JS数据
        for item in js_data:
            if isinstance(item, dict):
                name = item.get('name') or item.get('title') or item.get('site_name') or ''
                site_url = item.get('url') or item.get('link') or item.get('href') or item.get('website') or ''
                description = item.get('description') or item.get('desc') or item.get('summary') or ''
                category = item.get('category') or item.get('cat') or item.get('group') or '未分类'

                if name and site_url:
                    site_url = normalize_url(site_url)
                    if site_url.startswith('http'):
                        sites.append({
                            'name': name.strip(),
                            'url': site_url,
                            'description': description.strip()[:200],
                            'category': str(category).strip(),
                            'icon': '',
                        })
    else:
        print('未发现JS数据，尝试解析服务端渲染HTML...')
        sites, categories = parse_server_rendered(html, base_url)

    # 去重
    unique_sites = []
    seen_domains = set()
    for site in sites:
        domain = get_domain(site['url'])
        if domain and domain not in seen_domains:
            seen_domains.add(domain)
            unique_sites.append(site)
        elif not domain:
            unique_sites.append(site)

    # 统计分类
    cat_counts = {}
    for site in unique_sites:
        cat = site.get('category', '未分类')
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    categories = [{'name': k, 'count': v} for k, v in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)]

    print(f'\n抓取完成:')
    print(f'  分类数: {len(categories)}')
    print(f'  站点数: {len(unique_sites)}')
    print(f'\n分类列表:')
    for cat in categories[:20]:
        print(f'  - {cat["name"]}: {cat["count"]}个')

    # 构建结果
    result = {
        'source_name': get_domain(url) or url,
        'source_url': url,
        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'categories': categories,
        'sites': unique_sites,
    }

    return result

def main():
    if len(sys.argv) < 2:
        print('用法: python crawler_generic.py <目标站点URL>')
        print('示例: python crawler_generic.py https://www.example-nav.com')
        sys.exit(1)

    url = sys.argv[1].strip()
    if not url.startswith('http'):
        url = 'https://' + url

    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    result = crawl(url)

    if result:
        # 输出结果到stdout（供Web后台解析）
        print('\n' + '='*50)
        print('CRAWL_RESULT:' + json.dumps(result, ensure_ascii=False))
    else:
        print('CRAWL_RESULT:' + json.dumps({'error': '抓取失败'}, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()
