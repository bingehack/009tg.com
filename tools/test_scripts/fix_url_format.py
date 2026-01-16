#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复JSON数据文件中的URL格式

用途：
    修复JSON数据文件中错误的URL格式，去掉路径部分，只保留域名

修复内容：
    1. 将 https://echodata.work/home.html
    2. 改为 https://echodata.work
"""

import json
from urllib.parse import urlparse

def fix_url(url):
    """修复URL格式，去掉路径部分"""
    if not url or not isinstance(url, str):
        return url
    
    try:
        parsed = urlparse(url)
        # 只保留协议和域名，去掉路径
        fixed_url = f"{parsed.scheme}://{parsed.netloc}"
        return fixed_url
    except:
        return url

def fix_json_file(json_file):
    """修复JSON文件中的所有URL"""
    
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    def process_group(group):
        nonlocal fixed_count
        if 'sites' in group:
            for site in group['sites']:
                if 'url' in site:
                    original_url = site['url']
                    fixed_url = fix_url(original_url)
                    if fixed_url != original_url:
                        print(f"修复URL: {site.get('name', 'Unknown')}")
                        print(f"  原始: {original_url}")
                        print(f"  修复: {fixed_url}")
                        site['url'] = fixed_url
                        fixed_count += 1
        if 'children' in group:
            for child in group['children']:
                process_group(child)
    
    # 处理所有分组
    for group in data.get('groups', []):
        process_group(group)
    
    # 保存修复后的JSON文件
    backup_file = json_file + '.backup2'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n备份文件已保存: {backup_file}")
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"修复后的JSON文件已保存: {json_file}")
    print(f"共修复了 {fixed_count} 个URL")

if __name__ == "__main__":
    json_file = "../完整版导航.json"
    
    print("开始修复JSON文件中的URL格式...")
    print("=" * 60)
    
    fix_json_file(json_file)
    
    print("=" * 60)
    print("所有操作完成!")
