#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Favicon缓存脚本（优化版）

优化内容：
    1. 移除cairosvg依赖（SVG直接使用默认图标，避免cairo库错误）
    2. 超时从10秒降到5秒
    3. 10线程并发下载
    4. 域名去重（避免同一域名重复处理）
    5. 优化输出（减少冗余日志）

使用方法：
    python cache_favicons.py
"""

import json
import os
import sys
import requests
import hashlib
from urllib.parse import urlparse
import time
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 配置
TIMEOUT = 5  # 单个请求超时（秒）
MAX_WORKERS = 10  # 并发线程数
SLEEP_BETWEEN = 0  # 并发模式下不需要sleep

def get_domain_from_url(url):
    """从URL中提取域名"""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return None

def get_favicon_sources(domain):
    """获取多个favicon源（优先使用Google）"""
    return [
        f"https://www.google.com/s2/favicons?domain={domain}&sz=64",
        f"https://favicon.yandex.net/favicon/{domain}",
        f"https://api.statvoo.com/favicon/{domain}",
    ]

def is_valid_image(content):
    """检查内容是否是有效的图片"""
    image_signatures = {
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'\xff\xd8\xff': 'JPEG',
        b'GIF87a': 'GIF',
        b'GIF89a': 'GIF',
        b'BM': 'BMP',
        b'RIFF': 'WEBP'
    }
    
    for signature, format_name in image_signatures.items():
        if content.startswith(signature):
            return True, format_name
    
    return False, None

def download_favicon(domain, cache_path):
    """下载单个站点的favicon（尝试多个源）"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for source_url in get_favicon_sources(domain):
        try:
            response = requests.get(source_url, headers=headers, timeout=TIMEOUT)
            if response.status_code == 200 and len(response.content) > 100:
                is_valid, format_name = is_valid_image(response.content)
                
                if is_valid:
                    with open(cache_path, 'wb') as f:
                        f.write(response.content)
                    return True, 'downloaded'
                # 非图片内容（JSON/SVG等）直接跳过，不尝试转换
        except:
            continue
    
    return False, 'failed'

def get_cache_filename(domain):
    """生成缓存文件名（使用MD5哈希）"""
    domain_hash = hashlib.md5(domain.encode()).hexdigest()
    return f"{domain_hash}.png"

def load_json_data(json_file):
    """加载JSON数据"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_all_domains(data):
    """提取所有唯一域名（去重）"""
    domains = set()
    domain_names = {}  # domain -> site name (for logging)
    
    def process_group(group):
        if 'sites' in group:
            for site in group['sites']:
                if 'url' in site and site['url']:
                    domain = get_domain_from_url(site['url'])
                    if domain:
                        domains.add(domain)
                        if domain not in domain_names:
                            domain_names[domain] = site.get('name', '')
        if 'children' in group:
            for child in group['children']:
                process_group(child)
    
    for group in data.get('groups', []):
        process_group(group)
    
    return domains, domain_names

def cache_favicons(json_file, cache_dir):
    """缓存所有网站的favicon（并发版）"""
    
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    data = load_json_data(json_file)
    all_domains, domain_names = extract_all_domains(data)
    
    print(f"找到 {len(all_domains)} 个唯一域名")
    print(f"缓存目录: {cache_dir}")
    print(f"并发线程数: {MAX_WORKERS}")
    print(f"超时: {TIMEOUT}秒/请求")
    print("-" * 60)
    
    # 过滤已存在的
    to_download = []
    exists_count = 0
    for domain in all_domains:
        cache_filename = get_cache_filename(domain)
        cache_path = os.path.join(cache_dir, cache_filename)
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            exists_count += 1
        else:
            to_download.append((domain, cache_path))
    
    print(f"已存在: {exists_count}")
    print(f"需要下载: {len(to_download)}")
    print("-" * 60)
    
    # 默认图标路径
    default_icon_path = "assets/images/logos/default.png"
    
    success_count = exists_count
    failed_count = 0
    cached_domains = {}
    
    # 先把已存在的加入映射
    for domain in all_domains:
        cache_filename = get_cache_filename(domain)
        cache_path = os.path.join(cache_dir, cache_filename)
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            cached_domains[domain] = f"assets/favicons/{cache_filename}"
    
    # 并发下载
    if to_download:
        print(f"开始并发下载 ({MAX_WORKERS}线程)...")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(download_favicon, domain, cache_path): (domain, cache_path)
                for domain, cache_path in to_download
            }
            
            completed = 0
            for future in as_completed(futures):
                domain, cache_path = futures[future]
                completed += 1
                
                try:
                    success, status = future.result()
                    cache_filename = os.path.basename(cache_path)
                    
                    if success:
                        cached_domains[domain] = f"assets/favicons/{cache_filename}"
                        success_count += 1
                    else:
                        # 下载失败，复制默认图标
                        try:
                            if os.path.exists(default_icon_path):
                                shutil.copy(default_icon_path, cache_path)
                                cached_domains[domain] = f"assets/favicons/{cache_filename}"
                                success_count += 1
                            else:
                                failed_count += 1
                        except:
                            failed_count += 1
                    
                    # 每50个打印一次进度
                    if completed % 50 == 0 or completed == len(to_download):
                        elapsed = time.time() - start_time
                        speed = completed / elapsed if elapsed > 0 else 0
                        eta = (len(to_download) - completed) / speed if speed > 0 else 0
                        print(f"  进度: {completed}/{len(to_download)} ({completed*100//len(to_download)}%) "
                              f"成功: {success_count}, 失败: {failed_count}, "
                              f"速度: {speed:.1f}/秒, 预计剩余: {eta:.0f}秒")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"  错误: {domain} - {e}")
    
    print("-" * 60)
    print(f"完成! 成功: {success_count}, 失败: {failed_count}")
    print(f"总映射数: {len(cached_domains)}")
    
    return cached_domains

def save_cache_mapping(mapping, mapping_file):
    """保存域名到favicon的映射关系"""
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"映射关系已保存到: {mapping_file}")

if __name__ == "__main__":
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 切换到项目根目录
    os.chdir(project_root)
    
    json_file = "完整版导航.json"
    cache_dir = "assets/favicons"
    mapping_file = "favicon_mapping.json"
    
    print("开始缓存favicon（优化版）...")
    print("=" * 60)
    
    mapping = cache_favicons(json_file, cache_dir)
    save_cache_mapping(mapping, mapping_file)
    
    print("=" * 60)
    print("所有操作完成!")
