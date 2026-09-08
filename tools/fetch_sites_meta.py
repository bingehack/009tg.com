#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取所有站点的meta信息（keywords、description、title）
用于站点详情页的个性化介绍，避免千篇一律
"""

import json
import os
import requests
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
TIMEOUT = 8  # 单个请求超时
MAX_WORKERS = 10  # 并发线程数
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def get_domain(url):
    """提取域名"""
    try:
        return urlparse(url).netloc.lower()
    except:
        return ''

def fetch_meta(site):
    """抓取单个站点的meta信息"""
    url = site.get('url', '')
    domain = get_domain(url)
    site_id = site.get('id', 0)
    
    if not url or not domain:
        return site_id, domain, None
    
    result = {
        'url': url,
        'domain': domain,
        'title': '',
        'description': '',
        'keywords': '',
        'og_title': '',
        'og_description': '',
        'status': 'pending',
    }
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        
        if resp.status_code != 200:
            result['status'] = f'http_{resp.status_code}'
            return site_id, domain, result
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # title
        if soup.title and soup.title.string:
            result['title'] = soup.title.string.strip()[:200]
        
        # meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            result['description'] = meta_desc['content'].strip()[:500]
        
        # meta keywords
        meta_kw = soup.find('meta', attrs={'name': 'keywords'})
        if meta_kw and meta_kw.get('content'):
            result['keywords'] = meta_kw['content'].strip()[:300]
        
        # og:title
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        if og_title and og_title.get('content'):
            result['og_title'] = og_title['content'].strip()[:200]
        
        # og:description
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            result['og_description'] = og_desc['content'].strip()[:500]
        
        # 如果没有meta description，用og:description
        if not result['description'] and result['og_description']:
            result['description'] = result['og_description']
        
        # 如果没有title，用og:title
        if not result['title'] and result['og_title']:
            result['title'] = result['og_title']
        
        result['status'] = 'success' if (result['description'] or result['title']) else 'no_meta'
        
    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
    except requests.exceptions.ConnectionError:
        result['status'] = 'connection_error'
    except requests.exceptions.SSLError:
        result['status'] = 'ssl_error'
    except Exception as e:
        result['status'] = f'error_{type(e).__name__}'
    
    return site_id, domain, result

def main():
    print('=' * 60)
    print('抓取站点meta信息')
    print('=' * 60)
    
    # 加载主数据
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 收集所有站点
    all_sites = []
    def collect_sites(group):
        for site in group.get('sites', []):
            all_sites.append(site)
        for child in group.get('children', []):
            collect_sites(child)
    for g in data['groups']:
        collect_sites(g)
    
    # 域名去重
    domain_sites = {}
    for site in all_sites:
        domain = get_domain(site.get('url', ''))
        if domain and domain not in domain_sites:
            domain_sites[domain] = site
    
    unique_sites = list(domain_sites.values())
    print(f'总站点数: {len(all_sites)}')
    print(f'唯一域名数: {len(unique_sites)}')
    print(f'并发线程: {MAX_WORKERS}, 超时: {TIMEOUT}秒')
    print('-' * 60)
    
    # 加载已有的meta数据（断点续传）
    meta_file = 'data/sites_meta.json'
    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta_data = json.load(f)
        print(f'已加载已有meta数据: {len(meta_data)} 条')
    else:
        meta_data = {}
        os.makedirs('data', exist_ok=True)
    
    # 过滤已抓取成功的
    to_fetch = []
    for site in unique_sites:
        domain = get_domain(site.get('url', ''))
        if domain in meta_data and meta_data[domain].get('status') == 'success':
            continue
        to_fetch.append(site)
    
    print(f'需要抓取: {len(to_fetch)} 个域名')
    print(f'已成功跳过: {len(unique_sites) - len(to_fetch)} 个')
    print('-' * 60)
    
    if not to_fetch:
        print('所有域名已抓取完成！')
        return
    
    # 并发抓取
    start_time = time.time()
    results = {}
    success_count = 0
    fail_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_meta, site): site for site in to_fetch}
        
        for i, future in enumerate(as_completed(futures), 1):
            try:
                site_id, domain, result = future.result()
                
                if result:
                    results[domain] = result
                    meta_data[domain] = result
                    
                    if result['status'] == 'success':
                        success_count += 1
                    else:
                        fail_count += 1
                
                # 每100个保存一次
                if i % 100 == 0:
                    with open(meta_file, 'w', encoding='utf-8') as f:
                        json.dump(meta_data, f, ensure_ascii=False, indent=2)
                    
                    elapsed = time.time() - start_time
                    speed = i / elapsed if elapsed > 0 else 0
                    eta = (len(to_fetch) - i) / speed if speed > 0 else 0
                    print(f'  进度: {i}/{len(to_fetch)} ({i*100//len(to_fetch)}%) '
                          f'成功: {success_count}, 失败: {fail_count}, '
                          f'速度: {speed:.1f}/秒, 预计剩余: {eta:.0f}秒')
                    
            except Exception as e:
                fail_count += 1
                print(f'  错误: {e}')
    
    # 最终保存
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(meta_data, f, ensure_ascii=False, indent=2)
    
    elapsed = time.time() - start_time
    print('-' * 60)
    print(f'抓取完成！')
    print(f'  总耗时: {elapsed:.0f}秒 ({elapsed/60:.1f}分钟)')
    print(f'  成功: {success_count}')
    print(f'  失败: {fail_count}')
    print(f'  总meta数据: {len(meta_data)} 条')
    print(f'  保存到: {meta_file}')
    
    # 统计失败原因
    fail_reasons = {}
    for domain, meta in meta_data.items():
        status = meta.get('status', '')
        if status != 'success':
            fail_reasons[status] = fail_reasons.get(status, 0) + 1
    
    if fail_reasons:
        print(f'\n失败原因统计:')
        for reason, count in sorted(fail_reasons.items(), key=lambda x: x[1], reverse=True):
            print(f'  {reason}: {count}')

if __name__ == '__main__':
    main()
