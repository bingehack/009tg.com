#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速下载新增站点的favicon
只下载 raw/zvcard深度抓取_新增站点.json 中的站点
"""

import json
import requests
import hashlib
import os
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

FAVICON_DIR = 'assets/favicons'
MAPPING_FILE = 'favicon_mapping.json'

def get_domain(url):
    """提取域名"""
    try:
        return urlparse(url).netloc.lower()
    except:
        return ''

def download_favicon(site):
    """下载单个站点的favicon"""
    url = site['url']
    domain = get_domain(url)
    
    if not domain:
        return None, 'invalid_domain'
    
    # 检查是否已存在
    md5 = hashlib.md5(domain.encode()).hexdigest()
    favicon_path = os.path.join(FAVICON_DIR, f'{md5}.png')
    
    if os.path.exists(favicon_path) and os.path.getsize(favicon_path) > 0:
        return domain, 'exists'
    
    # 尝试多种favicon URL
    favicon_urls = [
        f'https://www.google.com/s2/favicons?domain={domain}&sz=64',
        f'https://favicon.im/{domain}',
        f'https://{domain}/favicon.ico',
    ]
    
    for fav_url in favicon_urls:
        try:
            resp = requests.get(fav_url, headers=headers, timeout=10, stream=True)
            if resp.status_code == 200:
                content = resp.content
                if len(content) > 100:  # 有效图片
                    with open(favicon_path, 'wb') as f:
                        f.write(content)
                    return domain, 'downloaded'
        except:
            continue
    
    return domain, 'failed'

def main():
    print('=' * 60)
    print('快速下载新增站点favicon')
    print('=' * 60)
    
    # 加载新增站点
    with open('raw/zvcard深度抓取_新增站点.json', 'r', encoding='utf-8') as f:
        new_sites = json.load(f)
    
    print(f'新增站点数: {len(new_sites)}')
    
    # 确保目录存在
    os.makedirs(FAVICON_DIR, exist_ok=True)
    
    # 加载现有映射
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
    else:
        mapping = {}
    
    # 多线程下载
    results = {'downloaded': 0, 'exists': 0, 'failed': 0}
    failed_domains = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_favicon, site): site for site in new_sites}
        
        for i, future in enumerate(as_completed(futures), 1):
            try:
                domain, status = future.result()
                results[status] = results.get(status, 0) + 1
                
                if status == 'downloaded':
                    md5 = hashlib.md5(domain.encode()).hexdigest()
                    mapping[domain] = f'assets/favicons/{md5}.png'
                elif status == 'failed':
                    failed_domains.append(domain)
                
                if i % 50 == 0:
                    print(f'  进度: {i}/{len(new_sites)}, 下载: {results["downloaded"]}, 已存在: {results["exists"]}, 失败: {results["failed"]}')
                    
            except Exception as e:
                print(f'  错误: {e}')
    
    print(f'\n下载完成:')
    print(f'  新下载: {results["downloaded"]}')
    print(f'  已存在: {results["exists"]}')
    print(f'  失败: {results["failed"]}')
    
    if failed_domains:
        print(f'\n失败的域名（前20个）:')
        for d in failed_domains[:20]:
            print(f'  {d}')
    
    # 保存映射
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f'\n映射文件已更新: {MAPPING_FILE}')
    print(f'总映射数: {len(mapping)}')

if __name__ == '__main__':
    main()
