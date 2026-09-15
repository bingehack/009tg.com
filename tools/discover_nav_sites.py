#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导航站发现脚本
从已知导航站的友情链接递归发现同类站点，保存为源站列表

用法：
  python discover_nav_sites.py              # 默认发现，深度2层
  python discover_nav_sites.py --depth 3    # 指定递归深度
  python discover_nav_sites.py --seed https://www.zvcard.com  # 指定种子站
"""

import sys
import os
import json
import re
import time
import argparse
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
    'timeout': 15,
    'delay': 1.0,
    'max_sites': 200,  # 最大发现站点数
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 导航站关键词（用于判断是否为同类站）
NAV_KEYWORDS = [
    '导航', '网址', '工具', '收录', '导航站', '网址导航', '工具导航',
    '网站导航', '导航网', '网址大全', '网站大全', '工具集合', '工具集',
    'nav', 'navigation', 'directory', 'bookmark', 'links',
    'onenav', 'navsite', 'daohang',
]

# 排除的域名（非导航站或社交媒体）
EXCLUDE_DOMAINS = [
    'google.com', 'facebook.com', 'twitter.com', 'youtube.com',
    'github.com', 'baidu.com', 'qq.com', 'weibo.com', 'zhihu.com',
    'bilibili.com', 'taobao.com', 'jd.com', 'amazon.com',
    'wikipedia.org', 'stackoverflow.com', 'medium.com',
    'gov.cn', 'edu.cn',
]

# 已知种子站
DEFAULT_SEEDS = [
    'https://www.zvcard.com',
    'https://www.tboxn.com',
    'https://www.ainav.cn',
    'https://www.uisdc.com',
]


def get_domain(url):
    """提取域名"""
    try:
        domain = urlparse(url).hostname.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return ''


def is_nav_site(url, title='', text=''):
    """判断是否为导航站"""
    domain = get_domain(url)

    # 排除已知非导航站
    for excl in EXCLUDE_DOMAINS:
        if domain.endswith(excl) or domain == excl:
            return False

    # 检查标题和文本中的导航关键词
    combined = (title + ' ' + text).lower()
    for kw in NAV_KEYWORDS:
        if kw.lower() in combined:
            return True

    # 检查URL路径中的导航关键词
    path = urlparse(url).path.lower()
    for kw in ['nav', 'daohang', 'navigation', 'directory']:
        if kw in path:
            return True

    return False


def fetch_page(url):
    """抓取页面"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=CONFIG['timeout'],
                            verify=False, allow_redirects=True)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        return resp.text, resp.url, resp.status_code
    except Exception as e:
        return None, url, 0


def extract_links(html, base_url):
    """从页面提取所有链接"""
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        text = a.get_text(strip=True)

        if not href or href.startswith('#') or href.startswith('javascript:'):
            continue

        # 相对URL转绝对
        if href.startswith('/'):
            href = urljoin(base_url, href)
        elif not href.startswith('http'):
            continue

        links.append({'url': href, 'text': text})

    return links


def extract_friend_links(html, base_url):
    """提取友情链接（页脚区域）"""
    soup = BeautifulSoup(html, 'html.parser')
    friend_links = []

    # 查找友情链接区域
    friend_selectors = [
        '.friend-links', '.friend-link', '.flink', '.links',
        '.friend', '.blogroll', '.linkcat', '#links',
        'div[class*="friend"]', 'div[class*="link"]',
        'footer a', '.footer a', '.copyright a',
    ]

    for selector in friend_selectors:
        try:
            elements = soup.select(selector)
            for el in elements:
                if el.name == 'a':
                    href = el.get('href', '')
                    text = el.get_text(strip=True)
                    if href and href.startswith('http'):
                        friend_links.append({'url': href, 'text': text})
                else:
                    for a in el.find_all('a', href=True):
                        href = a['href']
                        text = a.get_text(strip=True)
                        if href and href.startswith('http'):
                            friend_links.append({'url': href, 'text': text})
        except:
            continue

    return friend_links


def discover(seeds, max_depth=2):
    """递归发现导航站"""
    discovered = {}  # domain -> site info
    queue = []  # (url, depth)
    visited = set()

    # 初始化队列
    for seed in seeds:
        queue.append((seed, 0))

    total_checked = 0

    while queue and len(discovered) < CONFIG['max_sites']:
        url, depth = queue.pop(0)
        domain = get_domain(url)

        if not domain or domain in visited:
            continue
        visited.add(domain)

        total_checked += 1
        print(f'[{total_checked}] 检查: {url} (深度{depth})')

        html, final_url, status = fetch_page(url)
        if not html or status != 200:
            print(f'  无法访问，跳过')
            continue

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.get_text(strip=True) if soup.title else ''

        # 判断是否为导航站
        if is_nav_site(final_url, title, soup.get_text()[:2000]):
            if domain not in discovered:
                discovered[domain] = {
                    'url': final_url,
                    'domain': domain,
                    'title': title[:100],
                    'discovered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source_depth': depth,
                    'status': 'pending',  # pending=待抓取, crawled=已抓取, failed=抓取失败
                    'last_crawled': None,
                    'crawl_count': 0,
                    'sites_found': 0,
                }
                print(f'  ✓ 发现导航站: {title[:50]}')

        # 如果没到最大深度，继续递归
        if depth < max_depth:
            # 优先从友情链接提取
            friend_links = extract_friend_links(html, final_url)
            all_links = extract_links(html, final_url)

            # 合并，友情链接优先
            combined = friend_links + [l for l in all_links if l['url'] not in [f['url'] for f in friend_links]]

            new_count = 0
            for link in combined[:50]:  # 每个页面最多提取50个链接
                link_domain = get_domain(link['url'])
                if link_domain and link_domain not in visited:
                    # 简单判断：链接文本包含导航关键词
                    if any(kw in link['text'] for kw in ['导航', '网址', '工具', '收录', 'nav']):
                        queue.append((link['url'], depth + 1))
                        new_count += 1

            if new_count > 0:
                print(f'  加入队列: {new_count}个待检查')

        time.sleep(CONFIG['delay'])

    return discovered


def main():
    parser = argparse.ArgumentParser(description='导航站发现脚本')
    parser.add_argument('--depth', type=int, default=2, help='递归深度（默认2）')
    parser.add_argument('--seed', type=str, nargs='+', default=None, help='种子站URL')
    parser.add_argument('--output', type=str, default='nav_sources.json', help='输出文件名')
    args = parser.parse_args()

    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    seeds = args.seed if args.seed else DEFAULT_SEEDS

    print('=' * 60)
    print('导航站发现脚本')
    print('=' * 60)
    print(f'种子站: {len(seeds)}个')
    print(f'递归深度: {args.depth}')
    print(f'最大发现: {CONFIG["max_sites"]}个')
    print()

    # 读取已有列表（增量更新）
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), args.output)
    existing = {}
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            existing = data.get('sites', {})
        print(f'已有源站: {len(existing)}个')

    # 发现新站点
    discovered = discover(seeds, max_depth=args.depth)

    # 合并已有和新发现
    merged = dict(existing)
    new_count = 0
    for domain, info in discovered.items():
        if domain not in merged:
            merged[domain] = info
            new_count += 1
        else:
            # 更新标题等信息
            if info.get('title') and not merged[domain].get('title'):
                merged[domain]['title'] = info['title']

    # 保存
    result = {
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_sites': len(merged),
        'new_discovered': new_count,
        'sites': merged,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print()
    print('=' * 60)
    print(f'发现完成!')
    print(f'  新发现: {new_count}个')
    print(f'  总计: {len(merged)}个')
    print(f'  已保存: {output_path}')
    print()
    print('源站列表（前20）:')
    for i, (domain, info) in enumerate(sorted(merged.items(), key=lambda x: x[1].get('source_depth', 99))[:20], 1):
        status = info.get('status', 'pending')
        print(f'  {i}. [{status}] {info["title"][:40]} - {domain}')


if __name__ == '__main__':
    main()
