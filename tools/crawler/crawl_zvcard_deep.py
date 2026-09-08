#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zvcard.com 深度抓取脚本
遍历所有分类页面（favorites + sitetag），抓取所有站点并去重
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

BASE_URL = 'https://www.zvcard.com'

def get_page(url, retries=3):
    """获取页面内容，带重试"""
    for i in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.encoding = 'utf-8'
            return resp.text
        except Exception as e:
            print(f'  获取失败 ({i+1}/{retries}): {e}')
            time.sleep(2)
    return None

def extract_sites_from_page(html, category_name):
    """从页面HTML中提取站点"""
    sites = []
    if not html:
        return sites
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 查找站点卡片（a标签，class含site-）
    site_cards = soup.find_all('a', class_=lambda x: x and 'site-' in x)
    
    for card in site_cards:
        name = card.get('title', '').strip()
        url = card.get('data-url', '').strip()
        
        # 从卡片内获取描述
        desc = ''
        desc_elem = card.find('div', class_=lambda x: x and 'desc' in x.lower())
        if desc_elem:
            desc = desc_elem.get_text(strip=True)
        
        # 从卡片内获取图标
        icon = ''
        img = card.find('img')
        if img:
            icon = img.get('src', '')
            if icon and not icon.startswith('http'):
                icon = urljoin(BASE_URL, icon)
        
        if name and url:
            sites.append({
                'name': name,
                'url': url,
                'description': desc,
                'category': category_name,
                'icon': icon,
            })
    
    return sites

def discover_category_pages():
    """从首页发现所有分类页面"""
    print('=== 发现分类页面 ===')
    html = get_page(BASE_URL)
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
            if href.startswith('/'):
                full_url = BASE_URL + href
            else:
                full_url = href
            
            # 从URL提取分类slug
            slug = href.rstrip('/').split('/')[-1]
            if not cat_name:
                cat_name = slug
            
            if full_url not in seen:
                seen.add(full_url)
                categories.append({
                    'url': full_url,
                    'name': cat_name,
                    'type': 'favorites',
                    'slug': slug,
                })
                print(f'  [favorites] {cat_name}: {full_url}')
        
        # sitetag分类
        elif '/archives/sitetag/' in href:
            if href.startswith('/'):
                full_url = BASE_URL + href
            else:
                full_url = href
            
            # 解码URL中的中文
            from urllib.parse import unquote
            slug = unquote(href.rstrip('/').split('/')[-1])
            if not cat_name:
                cat_name = slug
            
            if full_url not in seen:
                seen.add(full_url)
                categories.append({
                    'url': full_url,
                    'name': cat_name,
                    'type': 'sitetag',
                    'slug': slug,
                })
                print(f'  [sitetag] {cat_name}: {full_url}')
    
    print(f'共发现 {len(categories)} 个分类页面')
    return categories

def crawl_all_categories(categories):
    """抓取所有分类页面的站点"""
    print('\n=== 开始深度抓取 ===')
    
    all_sites = {}  # url -> site dict
    category_stats = []
    
    for i, cat in enumerate(categories, 1):
        print(f'\n[{i}/{len(categories)}] 抓取: {cat["name"]} ({cat["type"]})')
        print(f'  URL: {cat["url"]}')
        
        html = get_page(cat['url'])
        if not html:
            print(f'  获取失败，跳过')
            category_stats.append({'name': cat['name'], 'count': 0, 'status': 'failed'})
            continue
        
        sites = extract_sites_from_page(html, cat['name'])
        print(f'  本页站点数: {len(sites)}')
        
        new_count = 0
        dup_count = 0
        for site in sites:
            url = site['url'].rstrip('/')
            if url not in all_sites:
                all_sites[url] = site
                new_count += 1
            else:
                dup_count += 1
                # 如果已有站点没有描述，用新的描述
                if not all_sites[url].get('description') and site.get('description'):
                    all_sites[url]['description'] = site['description']
        
        print(f'  新增: {new_count}, 重复: {dup_count}, 累计: {len(all_sites)}')
        category_stats.append({'name': cat['name'], 'count': len(sites), 'new': new_count, 'status': 'ok'})
        
        time.sleep(1)  # 礼貌延迟
    
    return all_sites, category_stats

def main():
    print('=' * 60)
    print('zvcard.com 深度抓取')
    print('=' * 60)
    
    # 1. 发现分类页面
    categories = discover_category_pages()
    if not categories:
        print('未发现分类页面')
        return
    
    # 2. 抓取所有分类
    all_sites, category_stats = crawl_all_categories(categories)
    
    # 3. 统计结果
    print('\n' + '=' * 60)
    print('抓取完成！')
    print('=' * 60)
    print(f'分类页面数: {len(categories)}')
    print(f'去重后站点总数: {len(all_sites)}')
    
    print('\n各分类统计:')
    for stat in category_stats:
        status_icon = '✓' if stat['status'] == 'ok' else '✗'
        print(f'  {status_icon} {stat["name"]}: {stat["count"]}个')
    
    # 4. 保存结果
    sites_list = list(all_sites.values())
    result = {
        'source_name': 'zvcard.com',
        'source_url': BASE_URL,
        'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'crawl_type': 'deep',
        'categories': [{'name': c['name'], 'type': c['type']} for c in categories],
        'total_sites': len(sites_list),
        'sites': sites_list,
    }
    
    output_file = 'raw/zvcard深度抓取.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f'\n结果已保存: {output_file}')
    
    # 5. 输出前20个站点预览
    print('\n站点预览（前20个）:')
    for i, site in enumerate(sites_list[:20], 1):
        print(f'  {i}. {site["name"]} -> {site["url"]}')
    
    print('\n' + '=' * 60)
    print('CRAWL_RESULT:' + json.dumps({
        'source_name': 'zvcard.com',
        'total_sites': len(sites_list),
        'categories_count': len(categories),
    }, ensure_ascii=False))

if __name__ == '__main__':
    main()
