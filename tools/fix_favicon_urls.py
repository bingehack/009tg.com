#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复JSON数据文件中的favicon URL格式

用途：
    修复JSON数据文件中错误的faviconextractor.com URL格式

修复内容：
    1. 将 https://www.faviconextractor.com/favicon/{domain}?larger=true
    2. 改为 https://www.faviconextractor.com/api/favicon/{domain}
"""

import json
import re
from urllib.parse import urlparse

def fix_favicon_url(icon_url):
    """修复favicon URL格式"""
    if not icon_url or not isinstance(icon_url, str):
        return icon_url
    
    # 检查是否是faviconextractor.com的URL
    if 'faviconextractor.com' not in icon_url:
        return icon_url
    
    # 提取域名
    # 错误格式：https://www.faviconextractor.com/favicon/invisibleman.dpdns.org?larger=true
    # 正确格式：https://www.faviconextractor.com/api/favicon/invisibleman.dpdns.org
    
    # 使用正则表达式提取域名
    match = re.search(r'faviconextractor\.com/favicon/([^?]+)', icon_url)
    if match:
        domain = match.group(1)
        # 修复URL格式
        fixed_url = f"https://www.faviconextractor.com/api/favicon/{domain}"
        return fixed_url
    
    return icon_url

def fix_json_file(json_file):
    """修复JSON文件中的所有favicon URL"""
    
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    def process_group(group):
        nonlocal fixed_count
        if 'sites' in group:
            for site in group['sites']:
                if 'icon' in site:
                    original_icon = site['icon']
                    fixed_icon = fix_favicon_url(original_icon)
                    if fixed_icon != original_icon:
                        print(f"修复: {site.get('name', 'Unknown')}")
                        print(f"  原始: {original_icon}")
                        print(f"  修复: {fixed_icon}")
                        site['icon'] = fixed_icon
                        fixed_count += 1
        if 'children' in group:
            for child in group['children']:
                process_group(child)
    
    # 处理所有分组
    for group in data.get('groups', []):
        process_group(group)
    
    # 保存修复后的JSON文件
    backup_file = json_file + '.backup'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n备份文件已保存: {backup_file}")
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"修复后的JSON文件已保存: {json_file}")
    print(f"共修复了 {fixed_count} 个favicon URL")

if __name__ == "__main__":
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 切换到项目根目录
    os.chdir(project_root)
    
    json_file = "完整版导航.json"
    
    print("开始修复JSON文件中的favicon URL...")
    print("=" * 60)
    
    fix_json_file(json_file)
    
    print("=" * 60)
    print("所有操作完成!")
