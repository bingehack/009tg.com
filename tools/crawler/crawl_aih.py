#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AIH超级导航站 (aimomap.cn / aih.zone) 抓取脚本
纯JS渲染站，直接下载data.json数据文件解析
22个分类，站点字段：name/url/description(部分有needVPN)
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
    'source_name': 'AIH超级导航站',
    'data_url': 'https://www.aimomap.cn/data.json',
    'output_dir': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'raw'),
}

# 追踪参数清理
TRACKING_PARAMS = {'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
                    'utm-source', 'ref', 'referrer', 'from', 'spm', 'scm', 'fr', 'bd_vid',
                    'channel', 'invitecode', 'invite_code', 'aff', 'aff_code', 'code',
                    'souceid', 'sourceid', 'sqm', 'sharecode', 't', 'sharerUserId',
                    'invitationType', 'inviterId', 'agentChannel', 'ch', 'utm', 'cgv'}


def clean_tracking_params(url):
    """清理URL中的追踪参数"""
    try:
        parsed = urlparse(url)
        query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        cleaned_params = {k: v for k, v in query_params.items() if k.lower() not in TRACKING_PARAMS}
        new_query = urlencode(cleaned_params)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    except Exception:
        return url


def download_data_json(url):
    """下载data.json数据文件"""
    import requests
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                         timeout=20, verify=False)
        if r.status_code == 200:
            return r.json()
        else:
            print(f'  下载失败: HTTP {r.status_code}')
            return None
    except Exception as e:
        print(f'  下载异常: {e}')
        return None


def parse_data(data):
    """解析data.json，提取所有分类和站点"""
    categories = {}

    for cat in data:
        cat_name = cat.get('category', '').strip()
        if not cat_name:
            continue

        is_group = cat.get('isGroup', False)
        sites = []

        if is_group:
            # 分组分类：有subcategories，每个subcategory有sites
            subs = cat.get('subcategories', [])
            if isinstance(subs, list):
                for sub in subs:
                    sub_name = sub.get('name', '')
                    sub_sites = sub.get('sites', [])
                    if isinstance(sub_sites, list):
                        for s in sub_sites:
                            site = parse_site(s)
                            if site:
                                sites.append(site)
        else:
            # 非分组分类：直接有sites，或者结构不同
            # 尝试直接找sites
            if 'sites' in cat and isinstance(cat['sites'], list):
                for s in cat['sites']:
                    site = parse_site(s)
                    if site:
                        sites.append(site)
            # 尝试subcategories
            elif 'subcategories' in cat and isinstance(cat['subcategories'], list):
                for sub in cat['subcategories']:
                    sub_sites = sub.get('sites', [])
                    if isinstance(sub_sites, list):
                        for s in sub_sites:
                            site = parse_site(s)
                            if site:
                                sites.append(site)

        if sites:
            # 去重（同一分类内）
            seen = set()
            unique_sites = []
            for s in sites:
                if s['domain'] not in seen:
                    seen.add(s['domain'])
                    unique_sites.append(s)
            categories[cat_name] = unique_sites
            print(f'  [{cat_name}]: {len(unique_sites)}个工具')

    return categories


def parse_site(s):
    """解析单个站点"""
    name = s.get('name', '').strip()
    url = s.get('url', '').strip()
    description = s.get('description', '').strip()

    if not name or not url:
        return None

    # 清理追踪参数
    url = clean_tracking_params(url)
    url = normalize_url(url)

    if not is_valid_site_url(url):
        return None

    domain = get_domain(url)

    return {
        'name': name,
        'url': url,
        'domain': domain,
        'description': description,
    }


def main():
    print('=' * 60)
    print(f'AIH超级导航站抓取工具')
    print(f'数据文件: {CONFIG["data_url"]}')
    print('=' * 60)

    # 1. 加载已有域名去重池
    existing_domains = load_existing_domains()
    print(f'\n已加载去重池: {len(existing_domains)}个域名')

    # 2. 下载data.json
    print('\n[1/3] 下载data.json...')
    data = download_data_json(CONFIG['data_url'])
    if not data:
        print('ERROR: data.json下载失败!')
        return
    print(f'  下载成功: {len(data)}个分类')

    # 3. 解析
    print('\n[2/3] 解析分类和工具...')
    categories = parse_data(data)

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
