#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Favicon缓存脚本

用途：
    批量下载并缓存网站的favicon图标到本地。

功能概述：
    1. 从JSON数据中提取所有网站URL
    2. 使用多个favicon源（Google、Yandex、Statvoo、FaviconExtractor）尝试下载
    3. 使用MD5哈希生成唯一的文件名
    4. 生成域名到图标的映射关系文件
    5. 支持断点续传（已存在的文件跳过下载）

使用方法：
    python cache_favicons.py

主要特性：
    - 支持多个favicon源，提高成功率
    - 自动重试机制
    - 生成映射文件便于HTML生成脚本使用
    - 支持自定义超时时间
    - 详细的下载日志记录
"""

import json
import os
import requests
import hashlib
from urllib.parse import urlparse
import time

def get_domain_from_url(url):
    """从URL中提取域名"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return None

def get_favicon_sources(domain):
    """获取多个favicon源"""
    return [
        f"https://www.google.com/s2/favicons?domain={domain}&sz=64",
        f"https://favicon.yandex.net/favicon/{domain}",
        f"https://api.statvoo.com/favicon/{domain}",
        f"https://www.faviconextractor.com/favicon/{domain}?larger=true"
    ]

def download_favicon(url, save_path, timeout=10):
    """下载favicon图片"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code == 200 and len(response.content) > 100:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"下载失败: {url} - {e}")
    return False

def get_cache_filename(domain):
    """生成缓存文件名（使用MD5哈希避免文件名过长或特殊字符）"""
    domain_hash = hashlib.md5(domain.encode()).hexdigest()
    return f"{domain_hash}.png"

def load_json_data(json_file):
    """加载JSON数据"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_all_sites(data):
    """提取所有网站信息"""
    sites = []
    
    def process_group(group):
        if 'sites' in group:
            for site in group['sites']:
                if 'url' in site and site['url']:
                    sites.append({
                        'name': site.get('name', ''),
                        'url': site['url'],
                        'icon': site.get('icon', '')
                    })
        if 'children' in group:
            for child in group['children']:
                process_group(child)
    
    for group in data.get('groups', []):
        process_group(group)
    
    return sites

def cache_favicons(json_file, cache_dir):
    """缓存所有网站的favicon"""
    
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    data = load_json_data(json_file)
    sites = extract_all_sites(data)
    
    print(f"找到 {len(sites)} 个网站")
    print(f"缓存目录: {cache_dir}")
    print("-" * 60)
    
    success_count = 0
    failed_count = 0
    cached_domains = {}
    
    for i, site in enumerate(sites, 1):
        domain = get_domain_from_url(site['url'])
        if not domain:
            print(f"[{i}/{len(sites)}] 跳过: {site['name']} (无效URL)")
            failed_count += 1
            continue
        
        cache_filename = get_cache_filename(domain)
        cache_path = os.path.join(cache_dir, cache_filename)
        
        if os.path.exists(cache_path):
            print(f"[{i}/{len(sites)}] 已存在: {domain}")
            cached_domains[domain] = f"assets/favicons/{cache_filename}"
            success_count += 1
            continue
        
        print(f"[{i}/{len(sites)}] 处理: {domain} - {site['name']}")
        
        favicon_sources = get_favicon_sources(domain)
        downloaded = False
        
        for source_url in favicon_sources:
            if download_favicon(source_url, cache_path):
                print(f"  ✓ 下载成功: {source_url}")
                cached_domains[domain] = f"assets/favicons/{cache_filename}"
                downloaded = True
                success_count += 1
                break
            else:
                print(f"  ✗ 失败: {source_url}")
        
        if not downloaded:
            print(f"  ✗ 所有源都失败")
            failed_count += 1
        
        time.sleep(0.2)
    
    print("-" * 60)
    print(f"完成! 成功: {success_count}, 失败: {failed_count}")
    
    return cached_domains

def save_cache_mapping(mapping, mapping_file):
    """保存域名到favicon的映射关系"""
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"映射关系已保存到: {mapping_file}")

if __name__ == "__main__":
    json_file = "完整版导航.json"
    cache_dir = "assets/favicons"
    mapping_file = "favicon_mapping.json"
    
    print("开始缓存favicon...")
    print("=" * 60)
    
    mapping = cache_favicons(json_file, cache_dir)
    save_cache_mapping(mapping, mapping_file)
    
    print("=" * 60)
    print("所有操作完成!")
