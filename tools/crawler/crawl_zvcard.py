#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zvcard.com 专用抓取脚本（合并版）
针对 WordPress + onenav 主题的导航站结构

支持两种抓取模式：
  --mode quick  快速模式：抓取首页分页（默认，约1-2分钟）
  --mode deep   深度模式：遍历所有分类页面+分类内分页（约5-10分钟，数据更全）

用法：
  python crawl_zvcard.py --mode quick
  python crawl_zvcard.py --mode deep
"""

import sys
import os
import json
import re
import time
import argparse
from urllib.parse import urlparse, urljoin, urlunparse, unquote
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
    'max_pages_quick': 10,      # 快速模式最大页数
    'max_pages_per_cat': 20,    # 深度模式每个分类最大页数
    'delay': 1.5,                # 请求间隔（秒）
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
    parsed = urlparse(url)
    clean_params = []
    if parsed.query:
        for param in parsed.query.split('&'):
            if param and not param.lower().startswith(('utm_', 'ref=', 'channel=', 'from=', 'spm=')):
                clean_params.append(param)
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


def fetch_page(url, retries=3):
    """抓取页面，带重试"""
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=CONFIG['timeout'], verify=False, allow_redirects=True)
            resp.encoding = resp.apparent_encoding or 'utf-8'
            return resp.text, resp.status_code
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            print(f'  抓取失败: {url} - {e}')
            return None, 0


def parse_cards(soup, default_category='未分类'):
    """解析onenav主题的站点卡片"""
    sites = []
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
                href = card.get('href', '')
                if href.startswith('http') and 'zvcard.com' not in href:
                    url = href

            if not url or not url.startswith('http'):
                continue

            url = normalize_url(url)
            domain = get_domain(url)

            # 去重（本页内）
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

            name = re.sub(r'[\n\r\t]', ' ', name).strip()
            name = re.sub(r'\s+', ' ', name)

            # 提取描述
            description = ''
            desc_el = card.find('p')
            if desc_el:
                description = desc_el.get_text(strip=True)
            if not description:
                desc_el2 = card.find('div', class_=lambda x: x and 'desc' in x.lower())
                if desc_el2:
                    description = desc_el2.get_text(strip=True)
            if not description:
                all_text = card.get_text(strip=True)
                if all_text and all_text != name:
                    description = all_text.replace(name, '').strip()
            if description and len(description) > 200:
                description = description[:200] + '...'

            # 提取图标
            icon = ''
            img = card.find('img')
            if img:
                icon = img.get('src', '')
                if icon and not icon.startswith('http'):
                    icon = urljoin(CONFIG['base_url'], icon)

            sites.append({
                'name': name,
                'url': url,
                'description': description,
                'category': default_category,
                'icon': icon,
            })
        except Exception as e:
            continue

    return sites


def discover_category_pages():
    """从首页发现所有分类页面（favorites + sitetag）"""
    print('=== 发现分类页面 ===')
    html, status = fetch_page(CONFIG['base_url'])
    if not html:
        print('无法获取首页')
        return []

    soup = BeautifulSoup(html, 'html.parser')
    categories = []
    seen = set()

    for a in soup.find_all('a', href=True):
        href = a['href']
        cat_name = a.get_text(strip=True)

        # favorites分类
        if '/archives/favorites/' in href:
            full_url = CONFIG['base_url'] + href if href.startswith('/') else href
            slug = href.rstrip('/').split('/')[-1]
            if not cat_name:
                cat_name = slug
            if full_url not in seen:
                seen.add(full_url)
                categories.append({'url': full_url, 'name': cat_name, 'type': 'favorites', 'slug': slug})

        # sitetag分类
        elif '/archives/sitetag/' in href:
            full_url = CONFIG['base_url'] + href if href.startswith('/') else href
            slug = unquote(href.rstrip('/').split('/')[-1])
            if not cat_name:
                cat_name = slug
            if full_url not in seen:
                seen.add(full_url)
                categories.append({'url': full_url, 'name': cat_name, 'type': 'sitetag', 'slug': slug})

    print(f'共发现 {len(categories)} 个分类页面')
    for cat in categories[:10]:
        print(f'  [{cat["type"]}] {cat["name"]}')
    if len(categories) > 10:
        print(f'  ... 还有{len(categories)-10}个')
    return categories


def crawl_quick():
    """快速模式：抓取首页分页"""
    print(f'开始抓取（快速模式）: {CONFIG["base_url"]}')
    print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'最大页数: {CONFIG["max_pages_quick"]}')
    print()

    all_sites = []
    all_categories = []
    seen_domains = set()
    total_pages = 0

    for page in range(1, CONFIG['max_pages_quick'] + 1):
        url = CONFIG['base_url'] + '/' if page == 1 else f'{CONFIG["base_url"]}/page/{page}'
        print(f'[{page}/{CONFIG["max_pages_quick"]}] 抓取: {url}')

        html, status = fetch_page(url)
        if not html or status != 200:
            print(f'  页面状态: {status}，停止抓取')
            break

        total_pages += 1
        soup = BeautifulSoup(html, 'html.parser')

        # 按分类区块解析
        page_sites = []
        headings = soup.find_all(['h2', 'h3', 'h4'])
        for heading in headings:
            cat_name = heading.get_text(strip=True)
            if not cat_name or len(cat_name) > 30:
                continue
            skip_words = ['最新资讯', '友情链接', '热门标签', '猜你喜欢', '精品推荐']
            if any(w in cat_name for w in skip_words):
                continue
            if cat_name not in all_categories:
                all_categories.append(cat_name)
            container = heading.find_next_sibling()
            if container:
                sites = parse_cards(container, cat_name)
                page_sites.extend(sites)

        # 如果按区块解析不到，直接解析整个页面
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

        print(f'  本页站点: {len(page_sites)}个，新增: {new_count}个，累计: {len(all_sites)}个')

        # 检查是否有下一页
        next_link = soup.find('a', href=lambda x: x and f'/page/{page + 1}' in x)
        if not next_link and page > 1:
            print(f'  没有下一页，停止抓取')
            break

        if page < CONFIG['max_pages_quick']:
            time.sleep(CONFIG['delay'])

    return all_sites, all_categories, total_pages


def crawl_deep():
    """深度模式：遍历所有分类页面+分类内分页"""
    print(f'开始抓取（深度模式）: {CONFIG["base_url"]}')
    print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()

    # 1. 发现所有分类页面
    categories = discover_category_pages()
    if not categories:
        print('未发现分类页面')
        return [], [], 0

    # 2. 遍历每个分类页面，支持分页
    all_sites_dict = {}  # url -> site dict
    all_categories = []
    total_pages = 0

    for i, cat in enumerate(categories, 1):
        print(f'\n[{i}/{len(categories)}] 抓取: {cat["name"]} ({cat["type"]})')
        if cat['name'] not in all_categories:
            all_categories.append(cat['name'])

        cat_new_count = 0
        for page in range(1, CONFIG['max_pages_per_cat'] + 1):
            url = cat['url'] if page == 1 else f'{cat["url"]}/page/{page}'
            html, status = fetch_page(url)
            if not html or status != 200:
                break

            total_pages += 1
            soup = BeautifulSoup(html, 'html.parser')
            sites = parse_cards(soup, cat['name'])

            if not sites:
                break

            page_new = 0
            for site in sites:
                site_url = site['url'].rstrip('/')
                if site_url not in all_sites_dict:
                    all_sites_dict[site_url] = site
                    page_new += 1
                    cat_new_count += 1
                else:
                    # 补充描述
                    if not all_sites_dict[site_url].get('description') and site.get('description'):
                        all_sites_dict[site_url]['description'] = site['description']

            print(f'  第{page}页: {len(sites)}个，新增{page_new}个')

            # 检查是否有下一页
            next_link = soup.find('a', href=lambda x: x and f'/page/{page + 1}' in x)
            if not next_link:
                break

            time.sleep(CONFIG['delay'])

        print(f'  分类累计新增: {cat_new_count}个，总站点: {len(all_sites_dict)}个')

    all_sites = list(all_sites_dict.values())
    return all_sites, all_categories, total_pages


def main():
    parser = argparse.ArgumentParser(description='zvcard.com 抓取脚本')
    parser.add_argument('--mode', choices=['quick', 'deep'], default='quick',
                        help='抓取模式: quick=快速(首页分页), deep=深度(全分类遍历)')
    args = parser.parse_args()

    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # 执行抓取
    if args.mode == 'deep':
        all_sites, all_categories, total_pages = crawl_deep()
    else:
        all_sites, all_categories, total_pages = crawl_quick()

    # 统计分类
    cat_counts = {}
    for site in all_sites:
        cat = site.get('category', '未分类')
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    categories_result = [{'name': k, 'count': v} for k, v in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)]

    # 输出结果
    print()
    print('=' * 50)
    print(f'抓取完成! (模式: {args.mode})')
    print(f'  抓取页数: {total_pages}')
    print(f'  分类数: {len(categories_result)}')
    print(f'  站点数: {len(all_sites)}')
    print()
    print('分类列表（前20）:')
    for cat in categories_result[:20]:
        print(f'  - {cat["name"]}: {cat["count"]}个')

    # 构建结果
    result = {
        'source_name': CONFIG['source_name'],
        'source_url': CONFIG['base_url'],
        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'crawl_mode': args.mode,
        'pages_crawled': total_pages,
        'categories': categories_result,
        'sites': all_sites,
    }

    # 保存到raw目录
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    output_file = os.path.join(raw_dir, f'zvcard_{args.mode}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f'\n结果已保存: {output_file}')

    # 输出结果到stdout（供Web后台解析）
    print('\n' + '=' * 50)
    print('CRAWL_RESULT:' + json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
