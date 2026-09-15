#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从抓取结果文件导入站点，LLM自动分类，合并到完整版导航.json

用法：
  python import_crawl_result.py tools/crawler/crawl_result_2345ai.json
  python import_crawl_result.py tools/crawler/crawl_result_2345ai.json --dry-run
"""

import json
import os
import sys
import argparse
from datetime import datetime

# 项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'tools', 'web_admin'))

from llm_classifier import classify_and_map_sites, get_all_categories


def load_nav_data():
    with open(os.path.join(PROJECT_ROOT, '完整版导航.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def save_nav_data(data):
    with open(os.path.join(PROJECT_ROOT, '完整版导航.json'), 'w', encoding='utf-8') as f:
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


def main():
    parser = argparse.ArgumentParser(description='导入抓取结果')
    parser.add_argument('input_file', help='抓取结果JSON文件路径')
    parser.add_argument('--dry-run', action='store_true', help='试运行，不修改数据')
    parser.add_argument('--min-confidence', type=int, default=60, help='最低置信度')
    args = parser.parse_args()

    print('=' * 60)
    print('导入抓取结果')
    print('=' * 60)
    print(f'输入文件: {args.input_file}')
    print(f'模式: {"试运行" if args.dry_run else "正式"}')
    print()

    # 读取抓取结果
    if not os.path.exists(args.input_file):
        print(f'错误: 文件不存在 {args.input_file}')
        return

    with open(args.input_file, 'r', encoding='utf-8') as f:
        crawl_data = json.load(f)

    sites = crawl_data.get('sites', [])
    print(f'抓取站点数: {len(sites)}')
    print(f'来源: {crawl_data.get("source_name", "")}')
    print()

    # 加载现有数据，去重
    nav_data = load_nav_data()
    groups = nav_data.get('groups', [])
    existing_domains = set()
    existing_ids = set()

    for g in groups:
        for s in g.get('sites', []):
            domain = get_domain(s.get('url', ''))
            if domain:
                existing_domains.add(domain)
            if s.get('id'):
                existing_ids.add(s['id'])

    # 过滤重复站点
    new_sites = []
    duplicate_count = 0
    for site in sites:
        domain = get_domain(site.get('url', ''))
        if domain and domain in existing_domains:
            duplicate_count += 1
            continue
        new_sites.append(site)

    print(f'重复站点: {duplicate_count}个')
    print(f'待分类站点: {len(new_sites)}个')
    print()

    if not new_sites:
        print('没有新站点需要导入')
        return

    # LLM自动分类
    print('=== LLM自动分类 ===')
    result = classify_and_map_sites(new_sites, platform='siliconflow', min_confidence=args.min_confidence)

    print(f'自动映射: {len(result["auto_mapped"])}个')
    print(f'待人工确认: {len(result["need_review"])}个')
    print(f'分类失败: {len(result["failed"])}个')
    print()

    # 显示分类统计
    cat_stats = {}
    for site, cat_id in result['auto_mapped']:
        cat = next((c for c in get_all_categories() if c['id'] == cat_id), None)
        cat_name = cat['full_name'] if cat else str(cat_id)
        cat_stats[cat_name] = cat_stats.get(cat_name, 0) + 1

    print('=== 分类统计 ===')
    for cat_name, count in sorted(cat_stats.items(), key=lambda x: -x[1]):
        print(f'  {cat_name}: {count}个')
    print()

    if args.dry_run:
        print('=== 试运行完成，未修改数据 ===')
        return

    # 合并到导航数据
    print('=== 合并到导航数据 ===')
    new_id = max(existing_ids) + 1 if existing_ids else 1
    added = 0

    for site, cat_id in result['auto_mapped']:
        target_group = next((g for g in groups if g['id'] == int(cat_id)), None)
        if not target_group:
            continue

        new_site = {
            'id': new_id,
            'group_id': int(cat_id),
            'name': site.get('name', ''),
            'url': site.get('url', ''),
            'icon': '',
            'description': site.get('description', ''),
            'description_en': site.get('description_en', ''),
            'notes': f'来源：{crawl_data.get("source_name", "抓取导入")}',
            'order_num': new_id,
            'is_public': 1,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        target_group['sites'].append(new_site)
        existing_domains.add(get_domain(site.get('url', '')))
        new_id += 1
        added += 1

    nav_data['exportDate'] = datetime.now().strftime('%Y-%m-%d')
    save_nav_data(nav_data)

    print(f'成功导入: {added}个站点')
    print()
    print('=== 导入完成 ===')
    print('接下来请运行:')
    print('  python tools/cache_favicons.py  # 下载favicon')
    print('  python tools/generate_new_html.py  # 生成首页')
    print('  python tools/generate_category_pages.py  # 生成分类页')
    print('  python tools/generate_site_detail_pages.py  # 生成详情页')
    print('  python tools/update_sitemap.py  # 更新sitemap')
    print('  git add -A && git commit -m "导入站点" && git push  # 提交部署')


if __name__ == '__main__':
    main()
