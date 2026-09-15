#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2345AI导航专用深度抓取脚本
遍历所有12个分类页面，滚动加载全部站点，提取真实URL

用法：
  python crawl_2345ai.py              # 抓取所有分类
  python crawl_2345ai.py --quick      # 只抓前3个分类测试
  python crawl_2345ai.py --category ailiaotianwenda  # 只抓指定分类
"""

import json
import os
import re
import sys
import time
import argparse
from datetime import datetime

try:
    import requests
except ImportError:
    print('请先安装requests: pip install requests')
    sys.exit(1)

# 项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 12个分类
CATEGORIES = [
    {'slug': 'changyongtuijian', 'name': '热门AI工具'},
    {'slug': 'ailiaotianwenda', 'name': 'AI智能对话'},
    {'slug': 'aituxiang', 'name': 'AI图像绘画'},
    {'slug': 'aispcz', 'name': 'AI视频创作'},
    {'slug': 'aiyinpin', 'name': 'AI音频音乐'},
    {'slug': 'aiwenbenxiezuo', 'name': 'AI文本工具'},
    {'slug': 'aibangong', 'name': 'AI办公工具'},
    {'slug': 'aisheji', 'name': 'AI设计工具'},
    {'slug': 'aixuexiyanjiu', 'name': 'AI学习资讯'},
    {'slug': 'aibianchengkaifa', 'name': 'AI代码编程'},
    {'slug': 'aixunlianmoxing', 'name': 'AI训练模型'},
    {'slug': 'ai-qi-ta-ling-yu', 'name': 'AI行业分类'},
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def fetch_category_page(slug, page=1):
    """获取分类页面HTML"""
    url = f'https://www.2345ai.com/favorites/{slug}'
    if page > 1:
        url += f'/page/{page}'

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.encoding = 'utf-8'
        return resp.text
    except Exception as e:
        print(f'  获取页面失败: {e}')
        return ''


def parse_sites_from_html(html, category_name):
    """从HTML中解析站点"""
    sites = []

    # 匹配站点卡片 article.posts-item 中的a标签（必须有data-url属性）
    # 格式：<a ... data-url="真实URL" ... title="站点名称" ...>
    pattern = r'<a[^>]*data-url="([^"]*)"[^>]*title="([^"]*)"[^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.DOTALL)

    for url, name, inner_html in matches:
        url = url.strip()
        name = name.strip()

        if not url or not name:
            continue

        # 跳过内部URL（2345ai自己的页面）
        if '2345ai.com' in url:
            continue

        # 提取描述
        desc = ''
        desc_match = re.search(r'class="[^"]*desc[^"]*"[^>]*>(.*?)</', inner_html, re.DOTALL)
        if desc_match:
            desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()

        # 清理名称中的HTML实体
        name = re.sub(r'&[a-z]+;', '', name).strip()

        sites.append({
            'name': name,
            'url': url,
            'description': desc,
            'category': category_name,
            'icon': '',
        })

    return sites


def get_total_count(html):
    """获取分类总站点数"""
    match = re.search(r'共\s*(\d+)\s*篇', html)
    if match:
        return int(match.group(1))
    return 0


def has_next_page(html):
    """检查是否有下一页"""
    return '下一页' in html or 'next page' in html.lower()


def crawl_category(slug, name):
    """抓取单个分类的所有站点"""
    print(f'\n--- [{name}] ---')
    all_sites = []
    page = 1
    total = 0

    while True:
        print(f'  抓取第{page}页...')
        html = fetch_category_page(slug, page)

        if not html:
            break

        if page == 1:
            total = get_total_count(html)
            print(f'  站点总数: {total}')

        sites = parse_sites_from_html(html, name)
        print(f'  本页解析到: {len(sites)}个站点')

        if not sites:
            break

        all_sites.extend(sites)

        # 判断是否还有下一页
        # 方式1：根据总数计算
        if total > 0 and len(all_sites) >= total:
            break

        # 方式2：本页站点数少于30，说明是最后一页
        if len(sites) < 30:
            break

        # 方式3：安全限制，最多20页
        if page >= 20:
            break

        page += 1
        time.sleep(1)

    # 去重
    unique_sites = []
    seen_urls = set()
    for site in all_sites:
        url = site['url'].lower().rstrip('/')
        if url not in seen_urls:
            seen_urls.add(url)
            unique_sites.append(site)

    print(f'  合计: {len(all_sites)}个，去重后: {len(unique_sites)}个')
    return unique_sites


def main():
    parser = argparse.ArgumentParser(description='2345AI导航深度抓取')
    parser.add_argument('--quick', action='store_true', help='快速模式，只抓前3个分类')
    parser.add_argument('--category', type=str, help='只抓取指定分类slug')
    parser.add_argument('--output', type=str, default='', help='输出文件路径')
    args = parser.parse_args()

    print('=' * 60)
    print('2345AI导航深度抓取')
    print('=' * 60)
    print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    # 选择要抓取的分类
    if args.category:
        categories = [c for c in CATEGORIES if c['slug'] == args.category]
        if not categories:
            print(f'错误: 未找到分类 {args.category}')
            return
    elif args.quick:
        categories = CATEGORIES[:3]
    else:
        categories = CATEGORIES

    print(f'抓取分类数: {len(categories)}')
    print()

    # 抓取所有分类
    all_sites = []
    for cat in categories:
        sites = crawl_category(cat['slug'], cat['name'])
        all_sites.extend(sites)

    # 全局去重
    unique_sites = []
    seen_urls = set()
    for site in all_sites:
        url = site['url'].lower().rstrip('/')
        if url not in seen_urls:
            seen_urls.add(url)
            unique_sites.append(site)

    print()
    print('=' * 60)
    print(f'抓取完成!')
    print(f'  总计: {len(all_sites)}个站点')
    print(f'  去重后: {len(unique_sites)}个站点')
    print('=' * 60)

    # 按分类统计
    cat_stats = {}
    for site in unique_sites:
        cat = site['category']
        cat_stats[cat] = cat_stats.get(cat, 0) + 1
    print('\n分类统计:')
    for cat, count in sorted(cat_stats.items(), key=lambda x: -x[1]):
        print(f'  {cat}: {count}个')

    # 输出结果
    result = {
        'source_name': '2345AI导航',
        'source_url': 'https://www.2345ai.com/',
        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'categories': [{'name': cat, 'count': count} for cat, count in cat_stats.items()],
        'sites': unique_sites,
    }

    # 保存到文件
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(PROJECT_ROOT, 'tools', 'crawler', 'crawl_result_2345ai.json')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f'\n结果已保存到: {output_path}')

    # 输出CRAWL_RESULT格式（供管理后台解析）
    print()
    print('=' * 50)
    print('CRAWL_RESULT:' + json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
