#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加默认src属性脚本

用途：
    为使用Google favicon服务的图片添加默认src属性，避免显示小地球图标。

功能概述：
    扫描HTML文件中的Google favicon服务URL，为这些图片添加默认src属性指向本地默认图片

使用方法：
    python add_default_src.py

主要特性：
    - 修复Google favicon服务超时导致的图标显示问题
    - 为懒加载图片提供fallback
    - 支持多个HTML文件（index.html, cn/index.html, en/index.html）
"""

import os
import re

# 获取脚本所在目录的父目录（项目根目录）
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# 切换到项目根目录
os.chdir(project_root)

html_files = ['index.html', 'cn/index.html', 'en/index.html']

for file_name in html_files:
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 为所有使用Google favicon服务的图片添加默认的src属性
    # 这样在懒加载之前就会有一个fallback图片
    pattern = r'<img data-src="(https://www\.google\.com/s2/favicons\?domain=[^"]+)" class="lozad img-circle" width="40">'
    replacement = r'<img src="assets/images/logos/default.png" data-src="\1" class="lozad img-circle" width="40">'
    
    count = len(re.findall(pattern, content))
    content = re.sub(pattern, replacement, content)
    
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已更新 {file_name}，添加了 {count} 个默认src属性')
