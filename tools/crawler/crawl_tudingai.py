#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图钉AI导航 (tudingai.com) 抓取脚本
原Tbox AI子站重定向到此站，22个AI子分类，312工具
抓取首页所有分类的工具，直接从data-url属性获取真实URL
"""

import sys
import os
import json
import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# 导入通用工具
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crawler_utils import (
    fetch_page,
    get_domain,
    normalize_url,
    is_valid_site_url,
    load_existing_domains,
    save_raw_output,
    print_crawl_summary,
)

# ========== 配置区 ==========
CONFIG = {
    'source_name': '图钉AI导航',
    'base_url': 'https://www.tudingai.com/',
    'output_dir': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'raw'),
}

# 需要从URL中移除的追踪参数
TRACKING_PARAMS = {'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
                    'utm-source', 'utm-medium', 'utm-campaign', 'ref', 'referrer', 'from',
                    'spm', 'scm', 'fr', 'bd_vid'}


def clean_tracking_params(url):
    """清理URL中的追踪参数"""
    try:
        parsed = urlparse(url)
        query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        # 移除追踪参数
        cleaned_params = {k: v for k, v in query_params.items() if k.lower() not in TRACKING_PARAMS}
        # 重建URL
        new_query = urlencode(cleaned_params)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    except Exception:
        return url


def clean_tool_name(name):
    """清理工具名称，去掉推荐/新上架标记"""
    name = re.sub(r'^荐\s*', '', name)
    name = re.sub(r'^新\s*', '', name)
    return name.strip()


def parse_homepage(html):
    """解析首页，提取所有分类和工具"""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    categories = {}

    # 遍历所有content-card（每个分类一个）
    for card in soup.find_all('div', class_='content-card'):
        h4 = card.find('h4')
        if not h4:
            continue
        cat_name = h4.get_text(strip=True).strip()

        # 跳过非工具分类（AI博客是特殊分类，包含整个页面工具，跳过）
        if cat_name in ['AI博客', '最新文章', '友情链接']:
            continue

        # 找工具卡片
        sites = []
        for site_a in card.find_all('a', class_='sites-body'):
            name_elem = site_a.find('h3', class_='item-title')
            name = clean_tool_name(name_elem.get_text(strip=True)) if name_elem else ''

            desc_elem = site_a.find('div', class_='text-muted')
            description = desc_elem.get_text(strip=True) if desc_elem else ''

            url = site_a.get('data-url', '')
            if not url:
                continue

            # 清理追踪参数
            url = clean_tracking_params(url)
            url = normalize_url(url)

            if not is_valid_site_url(url):
                continue

            domain = get_domain(url)

            sites.append({
                'name': name,
                'url': url,
                'domain': domain,
                'description': description,
            })

        if sites:
            categories[cat_name] = sites
            print(f'  [{cat_name}]: {len(sites)}个工具')

    return categories


def main():
    print('=' * 60)
    print(f'图钉AI导航抓取工具')
    print(f'目标: {CONFIG["base_url"]}')
    print('=' * 60)

    # 1. 加载已有域名去重池
    existing_domains = load_existing_domains()
    print(f'\n已加载去重池: {len(existing_domains)}个域名')

    # 2. 抓取首页
    print('\n[1/3] 抓取首页...')
    html = fetch_page(CONFIG['base_url'])
    if not html:
        print('ERROR: 首页抓取失败!')
        return
    print(f'  首页大小: {len(html)}字节')

    # 3. 解析
    print('\n[2/3] 解析分类和工具...')
    categories = parse_homepage(html)

    total_parsed = sum(len(sites) for sites in categories.values())
    print(f'\n共解析: {len(categories)}个分类, {total_parsed}个工具')

    # 4. 去重并按分类输出
    print('\n[3/3] 去重并输出...')
    all_new_sites = 0
    all_skipped_duplicate = 0
    new_domains = set()

    for cat_name, sites in categories.items():
        new_sites = []
        for site in sites:
            domain = site['domain']
            if domain not in existing_domains and domain not in new_domains:
                new_sites.append(site)
                new_domains.add(domain)
            else:
                all_skipped_duplicate += 1

        if new_sites:
            save_raw_output(
                category_name=cat_name,
                sites=new_sites,
                source_name=CONFIG['source_name'],
                output_dir=CONFIG['output_dir'],
                overwrite=True,
            )
            all_new_sites += len(new_sites)

    # 汇总
    print('\n' + '=' * 60)
    print_crawl_summary(
        source_name=CONFIG['source_name'],
        categories_count=len(categories),
        sites_total=total_parsed,
        sites_added=all_new_sites,
        sites_skipped_duplicate=all_skipped_duplicate,
        sites_skipped_invalid=0,
    )
    print('=' * 60)


if __name__ == '__main__':
    main()
