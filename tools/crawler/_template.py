#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_template.py - 导航站抓取脚本模板

使用方法：
    1. 复制本文件，重命名为目标站名称，如 crawl_ai_tools_cn.py
    2. 修改 CONFIG 中的目标站信息
    3. 根据目标站的 HTML 结构修改 parse_categories() 和 parse_sites()
    4. 运行: python crawl_xxx.py

依赖：
    pip install requests beautifulsoup4
"""

import os
import sys
import json

# 确保能导入同目录的 crawler_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crawler_utils import (
    fetch_page, polite_sleep, get_domain, normalize_url,
    is_valid_site_url, clean_text, truncate_text,
    load_existing_domains, load_raw_domains,
    save_raw_output, print_crawl_summary, safe_filename,
)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('请先安装 beautifulsoup4: pip install beautifulsoup4')
    sys.exit(1)


# ============================================================
# 配置区 - 根据目标站修改
# ============================================================
CONFIG = {
    # 目标站名称（用于输出文件名和来源标识）
    'source_name': 'example_nav',

    # 目标站首页URL
    'base_url': 'https://www.example-nav.com',

    # 分类列表页URL（如果分类在首页，填首页URL）
    'category_page_url': 'https://www.example-nav.com',

    # 分类映射：目标站分类名 → 我们的分类名
    # 不需要映射的分类会用原名，映射为 None 的分类会跳过
    'category_mapping': {
        # '目标站分类名': '我们的分类名',
        # 'AI工具': 'AI常用工具',
        # '不需要的分类': None,
    },

    # 默认父分类（如果目标站没有层级，所有分类都归到这个父分类下）
    'default_parent_category': '下海推荐',

    # 请求延迟范围（秒）
    'delay_range': (1, 3),

    # 超时时间（秒）
    'timeout': 15,

    # 最大重试次数
    'retries': 3,
}


# ============================================================
# 解析函数 - 根据目标站 HTML 结构修改
# ============================================================
def parse_categories(html, base_url):
    """
    从分类列表页解析出所有分类

    Args:
        html: 页面HTML内容
        base_url: 目标站基础URL（用于补全相对路径）

    Returns:
        list: [{'name': '分类名', 'url': '分类页URL'}, ...]
    """
    soup = BeautifulSoup(html, 'html.parser')
    categories = []

    # TODO: 根据目标站结构修改选择器
    # 示例：假设分类在 <div class="nav"> <a href="...">分类名</a> </div> 中
    # nav = soup.find('div', class_='nav')
    # if nav:
    #     for a in nav.find_all('a', href=True):
    #         name = clean_text(a.get_text())
    #         url = a['href']
    #         if name and url:
    #             # 补全相对路径
    #             if not url.startswith('http'):
    #                 url = base_url.rstrip('/') + '/' + url.lstrip('/')
    #             categories.append({'name': name, 'url': url})

    return categories


def parse_sites(html, category_url):
    """
    从分类详情页解析出所有站点

    Args:
        html: 页面HTML内容
        category_url: 当前分类页URL（用于补全相对路径）

    Returns:
        list: [{'name': '站点名', 'url': '站点URL', 'description': '描述', 'icon': '图标URL'}, ...]
    """
    soup = BeautifulSoup(html, 'html.parser')
    sites = []

    # TODO: 根据目标站结构修改选择器
    # 示例：假设站点卡片在 <div class="site-card"> 中
    # for card in soup.find_all('div', class_='site-card'):
    #     # 站点名
    #     name_el = card.find('a', class_='site-name')
    #     name = clean_text(name_el.get_text()) if name_el else ''
    #
    #     # 站点URL
    #     url = ''
    #     if name_el and name_el.get('href'):
    #         url = name_el['href']
    #         if not url.startswith('http'):
    #             url = category_url.rstrip('/') + '/' + url.lstrip('/')
    #
    #     # 描述
    #     desc_el = card.find('p', class_='site-desc')
    #     description = clean_text(desc_el.get_text()) if desc_el else ''
    #
    #     # 图标
    #     icon = ''
    #     img_el = card.find('img', class_='site-icon')
    #     if img_el and img_el.get('src'):
    #         icon = img_el['src']
    #         if not icon.startswith('http'):
    #             icon = category_url.rstrip('/') + '/' + icon.lstrip('/')
    #
    #     if name and url:
    #         sites.append({
    #             'name': name,
    #             'url': url,
    #             'description': description,
    #             'icon': icon,
    #         })

    return sites


# ============================================================
# 主抓取流程 - 一般不需要修改
# ============================================================
def main():
    config = CONFIG
    source_name = config['source_name']
    delay_range = config['delay_range']

    print('=' * 50)
    print(f'开始抓取: {source_name}')
    print(f'目标站: {config["base_url"]}')
    print('=' * 50)

    # 1. 加载已有域名（去重用）
    print('\n[1/4] 加载已有站点域名...')
    existing_domains = load_existing_domains()
    raw_domains = load_raw_domains()
    all_known_domains = existing_domains | raw_domains
    print(f'  完整版导航.json: {len(existing_domains)} 个域名')
    print(f'  raw/ 待合并: {len(raw_domains)} 个域名')
    print(f'  合计去重池: {len(all_known_domains)} 个域名')

    # 2. 抓取分类列表
    print(f'\n[2/4] 抓取分类列表: {config["category_page_url"]}')
    html = fetch_page(
        config['category_page_url'],
        timeout=config['timeout'],
        retries=config['retries'],
        delay_range=delay_range,
    )
    if not html:
        print('  错误: 无法抓取分类列表页，退出')
        return

    categories = parse_categories(html, config['base_url'])
    print(f'  解析到 {len(categories)} 个分类')

    # 应用分类映射
    mapped_categories = []
    for cat in categories:
        target_name = config['category_mapping'].get(cat['name'], cat['name'])
        if target_name is None:
            print(f'  跳过分类(映射为None): {cat["name"]}')
            continue
        cat['mapped_name'] = target_name
        mapped_categories.append(cat)

    print(f'  映射后 {len(mapped_categories)} 个分类')

    # 3. 遍历分类抓取站点
    print(f'\n[3/4] 遍历分类抓取站点...')
    stats = {
        'categories_count': 0,
        'sites_total': 0,
        'sites_added': 0,
        'sites_skipped_duplicate': 0,
        'sites_skipped_invalid': 0,
    }

    for idx, cat in enumerate(mapped_categories, 1):
        cat_name = cat['mapped_name']
        cat_url = cat['url']
        print(f'\n  [{idx}/{len(mapped_categories)}] {cat_name}')
        print(f'    URL: {cat_url}')

        # 抓取分类页
        html = fetch_page(cat_url, timeout=config['timeout'],
                          retries=config['retries'], delay_range=delay_range)
        if not html:
            print(f'    跳过: 无法抓取')
            continue

        # 解析站点
        sites = parse_sites(html, cat_url)
        stats['categories_count'] += 1
        stats['sites_total'] += len(sites)
        print(f'    解析到 {len(sites)} 个站点')

        # 去重和过滤
        valid_sites = []
        for site in sites:
            url = normalize_url(site.get('url', ''))
            domain = get_domain(url)

            # 无效URL
            if not url or not domain:
                stats['sites_skipped_invalid'] += 1
                continue

            # 非工具站过滤
            if not is_valid_site_url(url):
                stats['sites_skipped_invalid'] += 1
                continue

            # 重复域名
            if domain in all_known_domains:
                stats['sites_skipped_duplicate'] += 1
                continue

            # 新增
            site['url'] = url
            valid_sites.append(site)
            all_known_domains.add(domain)
            stats['sites_added'] += 1

        print(f'    有效新增: {len(valid_sites)}, 重复: {stats["sites_skipped_duplicate"]}, 无效: {stats["sites_skipped_invalid"]}')

        # 保存到 raw/
        if valid_sites:
            save_raw_output(
                category_name=cat_name,
                sites=valid_sites,
                source_name=source_name,
                parent_category=config.get('default_parent_category'),
            )

        # 礼貌延迟
        if idx < len(mapped_categories):
            polite_sleep(delay_range)

    # 4. 输出统计
    print('\n[4/4] 抓取完成')
    print_crawl_summary(
        source_name=source_name,
        categories_count=stats['categories_count'],
        sites_total=stats['sites_total'],
        sites_added=stats['sites_added'],
        sites_skipped_duplicate=stats['sites_skipped_duplicate'],
        sites_skipped_invalid=stats['sites_skipped_invalid'],
    )

    if stats['sites_added'] > 0:
        print(f'\n下一步:')
        print(f'  1. 检查 raw/ 目录下的输出文件')
        print(f'  2. 运行 python tools/build_data.py 合并数据')
        print(f'  3. 运行 python tools/cache_favicons.py 下载favicon')
        print(f'  4. 运行 python tools/generate_new_html.py 生成HTML')


if __name__ == '__main__':
    main()
