#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并zvcard抓取站点到完整版导航.json
1. 修复未映射站点的分类
2. 按域名去重
3. 合并到主数据
4. 自动分配ID
"""

import json
import os
import re
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_domain(url):
    from urllib.parse import urlparse
    try:
        domain = urlparse(url).hostname.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return ''

def normalize_url(url):
    from urllib.parse import urlparse, urlunparse
    if not url:
        return ''
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    parsed = urlparse(url)
    clean_params = []
    if parsed.query:
        for param in parsed.query.split('&'):
            if param and not param.lower().startswith(('utm_', 'ref=', 'channel=', 'from=', 'spm=', 'invite', 'promotion', 'ppf=', 'kwd=', 'ls=', 'lk=', 'r=', 'tc=', 'code=')):
                clean_params.append(param)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '&'.join(clean_params), ''))

# 未映射站点的手动分类修复
MANUAL_FIX = {
    'vmcard': '虚拟卡',
    'vmcardio': '虚拟卡',
    'telegram': '社媒资源',
    'whatsapp': '社媒资源',
    'myspace': '社媒资源',
    'vk.com': '社媒资源',
    'linkedin': '社媒资源',
    'clubhouse': '社媒资源',
    'quora': '社媒资源',
    'reddit': '社媒资源',
    'snapchat': '社媒资源',
    'pinterest': '社媒资源',
    'tumblr': '社媒资源',
    'discord': '社媒资源',
    'threads': '社媒资源',
    'tiktok': '社媒资源',
    'socialmediaexaminer': '社媒资源',
}

def fix_category(site):
    """手动修复未映射站点的分类"""
    name = site.get('name', '').lower()
    url = site.get('url', '').lower()
    text = f"{name} {url}"

    for keyword, category in MANUAL_FIX.items():
        if keyword in text:
            return category
    return site.get('category', '未分类')


def main():
    # 读取映射后的抓取结果
    crawl_data = load_json(os.path.join(PROJECT_ROOT, 'raw', 'zvcard导航_已分类.json'))
    sites = crawl_data.get('sites', [])
    print(f'读取抓取结果: {len(sites)}个站点')

    # 读取主数据
    nav_data = load_json(os.path.join(PROJECT_ROOT, '完整版导航.json'))
    groups = nav_data.get('groups', [])
    print(f'主数据: {len(groups)}个分类')

    # 建立分类名→分类ID的映射
    category_map = {}
    for g in groups:
        category_map[g['name']] = g['id']

    # 建立已有域名集合
    existing_domains = set()
    existing_ids = set()
    for g in groups:
        for s in g.get('sites', []):
            domain = get_domain(s.get('url', ''))
            if domain:
                existing_domains.add(domain)
            existing_ids.add(s.get('id', 0))

    print(f'已有站点域名: {len(existing_domains)}个')

    # 修复分类、去重、合并
    new_id = max(existing_ids) + 1 if existing_ids else 1
    added_count = 0
    duplicate_count = 0
    category_added = {}

    for site in sites:
        # 修复分类
        site['category'] = fix_category(site)
        category_name = site['category']

        # 检查分类是否存在
        if category_name not in category_map:
            print(f'  警告: 分类"{category_name}"不存在，跳过站点: {site["name"]}')
            continue

        # 规范化URL
        site['url'] = normalize_url(site['url'])
        domain = get_domain(site['url'])

        # 去重
        if domain and domain in existing_domains:
            duplicate_count += 1
            continue

        # 找到目标分类
        target_group = next((g for g in groups if g['name'] == category_name), None)
        if not target_group:
            continue

        # 添加站点
        new_site = {
            'id': new_id,
            'group_id': target_group['id'],
            'name': site['name'],
            'url': site['url'],
            'icon': '',
            'description': site.get('description', ''),
            'description_en': '',
            'notes': f'来源：zvcard导航',
            'order_num': new_id,
            'is_public': 1,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        target_group['sites'].append(new_site)
        existing_domains.add(domain)
        category_added[category_name] = category_added.get(category_name, 0) + 1
        new_id += 1
        added_count += 1

    # 更新导出日期
    nav_data['exportDate'] = datetime.now().strftime('%Y-%m-%d')

    # 保存
    save_json(nav_data, os.path.join(PROJECT_ROOT, '完整版导航.json'))

    # 统计
    total_sites = sum(len(g.get('sites', [])) for g in groups)
    print(f'\n合并完成!')
    print(f'  新增站点: {added_count}个')
    print(f'  重复跳过: {duplicate_count}个')
    print(f'  总站点数: {total_sites}个')
    print(f'\n分类新增统计:')
    for cat, count in sorted(category_added.items(), key=lambda x: x[1], reverse=True):
        print(f'  {cat}: +{count}个')


if __name__ == '__main__':
    main()
