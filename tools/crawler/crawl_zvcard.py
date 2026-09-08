#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zvcard.com 专用抓取脚本
针对 WordPress + onenav 主题的导航站结构
支持分页抓取、分类识别、自动去重
"""

import sys
import os
import json
import re
import time
from urllib.parse import urlparse, urljoin
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
CONFIG = {
    'source_name': 'zvcard导航',
    'base_url': 'https://www.zvcard.com',
    'max_pages': 10,  # 最大抓取页数
    'delay': 1.5,  # 请求间隔（秒）
    'timeout': 20,
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


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
    from urllib.parse import urlunparse
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '&'.join(clean_params), ''))


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
    """抓取页面"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=CONFIG['timeout'], verify=False, allow_redirects=True)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        return resp.text, resp.status_code
    except Exception as e:
        print(f'  抓取失败: {url} - {e}')
        return None, 0


def parse_cards(soup, default_category='未分类'):
    """解析onenav主题的站点卡片"""
    sites = []

    # onenav主题卡片结构: <a href="/sites/XXXX.html" data-url="真实URL" data-id="XXXX" class="card no-c mb-4 site-XXXX" title="站点名">
    # 注意：卡片是<a>标签，不是<div>标签！真实URL在data-url属性中

    cards = []

    # 方式1: 匹配包含 site- 的a标签
    cards.extend(soup.find_all('a', attrs={'class': re.compile(r'site-\d+')}))

    # 方式2: 匹配有 data-url 属性的a标签
    if not cards:
        cards.extend(soup.find_all('a', attrs={'data-url': True}))

    seen_domains = set()
    for card in cards:
        try:
            # 真实URL在 data-url 属性中
            url = card.get('data-url', '')
            if not url:
                # 如果没有data-url，尝试href（排除站内链接）
                href = card.get('href', '')
                if href.startswith('http') and 'zvcard.com' not in href:
                    url = href

            if not url or not url.startswith('http'):
                continue

            url = normalize_url(url)
            domain = get_domain(url)

            # 去重
            if domain and domain in seen_domains:
                continue
            if domain:
                seen_domains.add(domain)

            # 站点名称在 title 属性中
            name = card.get('title', '')
            if not name:
                name = card.get_text(strip=True)
            if not name or len(name) > 100:
                continue

            # 清理名称
            name = re.sub(r'[\n\r\t]', ' ', name).strip()
            name = re.sub(r'\s+', ' ', name)

            # 提取描述（从卡片内容中）
            description = ''
            desc_el = card.find('p')
            if desc_el:
                description = desc_el.get_text(strip=True)
            if not description:
                # 尝试找卡片中的其他文本（排除名称）
                all_text = card.get_text(strip=True)
                if all_text and all_text != name:
                    description = all_text.replace(name, '').strip()
            if description and len(description) > 200:
                description = description[:200] + '...'

            sites.append({
                'name': name,
                'url': url,
                'description': description,
                'category': default_category,
                'icon': '',
            })
        except Exception as e:
            continue

    return sites


def parse_categories(soup):
    """解析页面中的分类区块"""
    categories = []

    # onenav主题分类标题通常是 h3.text-md 或 h4.text-gray
    # 找所有可能的分类标题
    headings = soup.find_all(['h2', 'h3', 'h4'])

    for heading in headings:
        text = heading.get_text(strip=True)
        if not text or len(text) > 30:
            continue

        # 排除非分类标题
        skip_words = ['最新资讯', '友情链接', '热门标签', '猜你喜欢', '精品推荐']
        if any(w in text for w in skip_words):
            continue

        # 检查这个标题后面是否有站点卡片
        next_sibling = heading.find_next_sibling()
        has_cards = False
        check_count = 0
        while next_sibling and check_count < 5:
            if next_sibling.find_all('div', attrs={'class': re.compile(r'site-\d+|card')}):
                has_cards = True
                break
            next_sibling = next_sibling.find_next_sibling()
            check_count += 1

        if has_cards:
            categories.append(text)

    return categories


def crawl():
    """主抓取函数"""
    print(f'开始抓取: {CONFIG["base_url"]}')
    print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'最大页数: {CONFIG["max_pages"]}')
    print()

    all_sites = []
    all_categories = []
    seen_domains = set()
    total_pages = 0

    for page in range(1, CONFIG['max_pages'] + 1):
        if page == 1:
            url = CONFIG['base_url'] + '/'
        else:
            url = f'{CONFIG["base_url"]}/page/{page}'

        print(f'[{page}/{CONFIG["max_pages"]}] 抓取: {url}')

        html, status = fetch_page(url)
        if not html or status != 200:
            print(f'  页面状态: {status}，停止抓取')
            break

        total_pages += 1
        soup = BeautifulSoup(html, 'html.parser')

        # 解析分类
        categories = parse_categories(soup)
        for cat in categories:
            if cat not in all_categories:
                all_categories.append(cat)

        # 解析卡片（先按分类区块解析）
        page_sites = []

        # 方式1: 按分类区块解析
        headings = soup.find_all(['h2', 'h3', 'h4'])
        for heading in headings:
            cat_name = heading.get_text(strip=True)
            if not cat_name or len(cat_name) > 30:
                continue

            skip_words = ['最新资讯', '友情链接', '热门标签', '猜你喜欢', '精品推荐']
            if any(w in cat_name for w in skip_words):
                continue

            # 找标题后面的卡片容器
            container = heading.find_next_sibling()
            if container:
                sites = parse_cards(container, cat_name)
                page_sites.extend(sites)

        # 方式2: 如果按区块解析不到，直接解析整个页面
        if len(page_sites) < 5:
            page_sites = parse_cards(soup, '未分类')

        # 去重并合并
        new_count = 0
        for site in page_sites:
            domain = get_domain(site['url'])
            if domain and domain not in seen_domains:
                seen_domains.add(domain)
                all_sites.append(site)
                new_count += 1
            elif not domain:
                all_sites.append(site)
                new_count += 1

        print(f'  本页站点: {len(page_sites)}个，新增: {new_count}个')
        print(f'  累计站点: {len(all_sites)}个，分类: {len(all_categories)}个')

        # 检查是否有下一页
        next_link = soup.find('a', href=lambda x: x and f'/page/{page + 1}' in x)
        if not next_link and page > 1:
            print(f'  没有下一页，停止抓取')
            break

        # 请求间隔
        if page < CONFIG['max_pages']:
            time.sleep(CONFIG['delay'])

    # 统计分类
    cat_counts = {}
    for site in all_sites:
        cat = site.get('category', '未分类')
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    all_categories = [{'name': k, 'count': v} for k, v in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)]

    print()
    print('=' * 50)
    print(f'抓取完成!')
    print(f'  抓取页数: {total_pages}')
    print(f'  分类数: {len(all_categories)}')
    print(f'  站点数: {len(all_sites)}')
    print()
    print('分类列表:')
    for cat in all_categories[:20]:
        print(f'  - {cat["name"]}: {cat["count"]}个')

    # 构建结果
    result = {
        'source_name': CONFIG['source_name'],
        'source_url': CONFIG['base_url'],
        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'pages_crawled': total_pages,
        'categories': all_categories,
        'sites': all_sites,
    }

    # 保存到raw目录
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    output_file = os.path.join(raw_dir, f'zvcard导航_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f'\n结果已保存: {output_file}')

    # 输出结果到stdout（供Web后台解析）
    print('\n' + '=' * 50)
    print('CRAWL_RESULT:' + json.dumps(result, ensure_ascii=False))

    return result


if __name__ == '__main__':
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    crawl()
