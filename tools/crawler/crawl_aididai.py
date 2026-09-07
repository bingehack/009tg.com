#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI地带 (aididai.cn) 抓取脚本
阶段一测试：抓取指定分类的工具站点

站点结构：
- 分类页: https://www.aididai.cn/favorites/{slug}/
- 工具卡片: a.sites-body > div.item-body > h3.item-title + div.text-muted
- 工具链接: /go/?url=base64(真实URL)
"""

import sys
import os
import base64
import re
import time
from urllib.parse import urljoin, urlparse, parse_qs

# 添加crawler目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler'))
from crawler_utils import (
    fetch_page, get_domain, normalize_url, is_valid_site_url,
    clean_text, truncate_text, load_existing_domains, load_raw_domains,
    save_raw_output, print_crawl_summary
)
from bs4 import BeautifulSoup

# ============================================================
# 配置区
# ============================================================
CONFIG = {
    'source_name': 'AI地带',
    'source_url': 'https://www.aididai.cn',
    'base_url': 'https://www.aididai.cn',
    'delay': 0.5,                           # 请求间隔（秒）
    'timeout': 12,                          # 超时（秒）
    'max_retries': 2,                       # 最大重试次数
    'max_pages_per_category': 3,            # 每个分类最多抓取页数（每页20个）
    # 测试模式：只抓取指定分类，None则抓取全部分类
    'test_categories': None,
}

# 分类slug映射（从首页提取的分类名→slug）
CATEGORY_SLUGS = {
    'AI图像工具': 'ai%e5%9b%be%e5%83%8f%e5%b7%a5%e5%85%b7',
    'AI Agent/智能体': 'aiagent-intelligentagent',
    'AI短剧视频': 'aishortdramavideo',
    'AI视频工具': 'ai%e8%a7%86%e9%a2%91%e5%b7%a5%e5%85%b7',
    'AI写作工具': 'ai%e5%86%99%e4%bd%9c%e5%b7%a5%e5%85%b7',
    'AI设计工具': 'ai%e8%ae%be%e8%ae%a1%e5%b7%a5%e5%85%b7',
    'AI对话': 'ai%e5%af%b9%e8%af%9d%e5%b7%a5%e5%85%b7',
    'AI编程': 'ai%e7%bc%96%e7%a8%8b%e5%b7%a5%e5%85%b7',
    'AI办公': 'ai%e5%8a%9e%e5%85%ac%e5%b7%a5%e5%85%b7',
    'AI翻译': 'ai%e8%af%ad%e8%a8%80%e7%bf%bb%e8%af%91',
    'AI搜索': 'aisearch',
    'AI开发平台': 'ai%e5%bc%80%e5%8f%91%e6%a1%86%e6%9e%b6',
    'AI音频': 'ai%e9%9f%b3%e9%a2%91%e5%b7%a5%e5%85%b7',
    'AI内容检测': 'ai%e5%86%85%e5%ae%b9%e6%a3%80%e6%b5%8b',
    'AI学习资源': 'ai%e5%ad%a6%e4%b9%a0%e7%bd%91%e7%ab%99',
    'AI资讯获取': 'ainews',
    'AI公众号': 'wechat-oas',
}


def decode_go_url(go_url):
    """
    解码 /go/?url=base64 格式的跳转链接，返回真实URL
    """
    try:
        parsed = urlparse(go_url)
        params = parse_qs(parsed.query)
        if 'url' in params:
            encoded = params['url'][0]
            # base64解码（处理padding）
            padding = 4 - len(encoded) % 4
            if padding != 4:
                encoded += '=' * padding
            decoded = base64.b64decode(encoded).decode('utf-8', errors='ignore')
            return decoded
    except Exception as e:
        pass
    return None


def parse_categories(html, base_url):
    """
    从首页HTML中提取分类列表
    返回: [(分类名, 分类页URL), ...]
    """
    soup = BeautifulSoup(html, 'html.parser')
    categories = []

    # 查找"查看全部"链接
    for a in soup.find_all('a', string=re.compile(r'查看全部')):
        href = a.get('href', '')
        if '/favorites/' in href:
            # 从URL提取分类slug，尝试映射到分类名
            slug = href.split('/favorites/')[-1].strip('/')
            # 反向查找分类名
            cat_name = None
            for name, s in CATEGORY_SLUGS.items():
                if s == slug:
                    cat_name = name
                    break
            if not cat_name:
                # 尝试URL解码
                try:
                    from urllib.parse import unquote
                    cat_name = unquote(slug)
                except:
                    cat_name = slug

            full_url = urljoin(base_url, href)
            categories.append((cat_name, full_url))

    return categories


def fetch_real_url_from_detail(detail_url, timeout=15):
    """
    从详情页提取真实URL
    详情页中有"打开网站"按钮，href为 /go/?url=base64(真实URL)
    """
    html = fetch_page(detail_url, timeout=timeout, retries=2)
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # 查找"打开网站"按钮
    for a in soup.find_all('a', string=re.compile(r'打开网站|访问官网|立即访问')):
        href = a.get('href', '')
        if '/go/?url=' in href:
            real_url = decode_go_url(href)
            if real_url:
                return real_url

    # 备用：查找所有 /go/ 链接，取第一个
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/go/?url=' in href:
            real_url = decode_go_url(href)
            if real_url:
                return real_url

    return None


def parse_sites(category_base_url, category_name, base_url, delay=0.5, max_pages=3, timeout=12, max_retries=2):
    """
    从分类页（支持分页）提取工具站点
    分类页的工具卡片链接是详情页(/sites/xxx.html)，需要进入详情页提取真实URL
    返回: [{'name':..., 'url':..., 'description':...}, ...]
    """
    sites = []
    seen_detail_urls = set()  # 防止不同页重复

    for page in range(1, max_pages + 1):
        # 构建分页URL
        if page == 1:
            page_url = category_base_url
        else:
            page_url = category_base_url.rstrip('/') + f'/page/{page}/'

        print(f'\n  --- 第 {page} 页: {page_url} ---')
        html = fetch_page(page_url, timeout=timeout, retries=max_retries)
        if not html:
            print(f'  第 {page} 页获取失败，停止翻页')
            break

        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('a.sites-body')
        print(f'  找到 {len(cards)} 个工具卡片')

        if len(cards) == 0:
            print(f'  第 {page} 页无工具，停止翻页')
            break

        page_count = 0
        for idx, card in enumerate(cards):
            try:
                # 提取名称
                title_el = card.select_one('h3.item-title b') or card.select_one('h3.item-title')
                name = clean_text(title_el.get_text()) if title_el else ''

                # 提取描述
                desc_el = card.select_one('div.text-muted') or card.select_one('.line1.text-muted')
                description = clean_text(desc_el.get_text()) if desc_el else ''
                description = truncate_text(description, 200)

                # 提取详情页URL
                href = card.get('href', '')
                if not href:
                    continue

                # 构建完整详情页URL
                if href.startswith('/'):
                    detail_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    detail_url = href
                else:
                    continue

                # 跨页去重（同一个详情页只抓一次）
                if detail_url in seen_detail_urls:
                    continue
                seen_detail_urls.add(detail_url)

                # 从详情页提取真实URL
                print(f'  [{idx+1}/{len(cards)}] {name[:22]:22s} -> ', end='')
                real_url = fetch_real_url_from_detail(detail_url, timeout=timeout)

                if not real_url:
                    print('失败(无真实URL)')
                    continue

                # 规范化URL
                real_url = normalize_url(real_url)

                # 验证是否为有效站点URL
                if not is_valid_site_url(real_url):
                    print(f'跳过(无效)')
                    continue

                # 过滤空名称
                if not name:
                    name = get_domain(real_url)

                print(f'OK -> {get_domain(real_url)}')
                sites.append({
                    'name': name,
                    'url': real_url,
                    'description': description,
                })
                page_count += 1

                # 请求间隔
                time.sleep(delay)

            except Exception as e:
                print(f'  解析卡片出错: {e}')
                continue

        print(f'  第 {page} 页有效工具: {page_count} 个')

    return sites


def main():
    print("=" * 60)
    print(f"AI地带 (aididai.cn) 抓取脚本 - 全量抓取")
    print("=" * 60)

    # 切换到项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    # 加载已有域名（去重）
    print("\n加载已有域名池...")
    existing_domains = load_existing_domains('完整版导航.json')
    raw_domains = load_raw_domains('raw')
    all_existing = existing_domains | raw_domains
    print(f"  完整版导航.json: {len(existing_domains)} 个域名")
    print(f"  raw/ 目录: {len(raw_domains)} 个域名")
    print(f"  合计去重池: {len(all_existing)} 个域名")

    # 获取首页，提取分类
    print(f"\n获取首页: {CONFIG['source_url']}")
    home_html = fetch_page(CONFIG['source_url'], timeout=CONFIG['timeout'])
    if not home_html:
        print("获取首页失败！")
        return

    categories = parse_categories(home_html, CONFIG['base_url'])
    print(f"首页提取到 {len(categories)} 个分类")
    for name, url in categories:
        print(f"  - {name}: {url}")

    # 测试模式：只抓取指定分类
    if CONFIG.get('test_categories'):
        test_names = CONFIG['test_categories']
        categories = [(name, url) for name, url in categories if name in test_names]
        print(f"\n测试模式：只抓取 {len(categories)} 个分类: {[c[0] for c in categories]}")

    # 遍历分类抓取
    all_sites = []
    category_stats = []

    for cat_name, cat_url in categories:
        print(f"\n{'='*40}")
        print(f"抓取分类: {cat_name}")
        print(f"URL: {cat_url}")

        sites = parse_sites(
            category_base_url=cat_url,
            category_name=cat_name,
            base_url=CONFIG['base_url'],
            delay=CONFIG['delay'],
            max_pages=CONFIG['max_pages_per_category'],
            timeout=CONFIG['timeout'],
            max_retries=CONFIG['max_retries']
        )

        if not sites:
            print(f"  未获取到工具，跳过")
            category_stats.append((cat_name, 0, 0))
            continue

        print(f"\n  共解析到 {len(sites)} 个有效工具")

        # 去重
        new_sites = []
        for site in sites:
            domain = get_domain(site['url'])
            if domain and domain not in all_existing:
                all_existing.add(domain)
                new_sites.append(site)

        print(f"  去重后新增: {len(new_sites)} 个")
        category_stats.append((cat_name, len(sites), len(new_sites)))
        all_sites.extend(new_sites)

        # 每个分类单独保存到 raw/ 目录（category 保留 AI 地带原始分类名，供映射表转换）
        if new_sites:
            output_file = save_raw_output(
                category_name=cat_name,
                sites=new_sites,
                source_name=CONFIG['source_name'],
                output_dir='raw',
                overwrite=True
            )
            print(f"  已保存: {output_file}")

        # 请求间隔
        time.sleep(CONFIG['delay'])

    # 输出结果
    print(f"\n{'='*60}")
    print(f"抓取完成！")
    print(f"{'='*60}")
    print(f"\n分类统计:")
    for name, total, new in category_stats:
        print(f"  {name}: 共{total}个, 新增{new}个")
    print(f"\n总计新增: {len(all_sites)} 个站点")
    print(f"\n各分类 raw 文件已保存到 raw/ 目录")
    print(f"下一步: python tools/build_data.py (按映射表归类) → python tools/generate_new_html.py")

    if all_sites:
        # 打印前10个样本
        print(f"\n前10个样本:")
        for i, site in enumerate(all_sites[:10]):
            print(f"  {i+1}. {site['name'][:30]:30s} | {site['url'][:50]:50s} | {site['description'][:40]}")
    else:
        print("\n没有新增站点（可能全部已存在）")


if __name__ == '__main__':
    main()
