#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有HTML文件脚本

用途：
    为所有HTML文件中的懒加载图片添加src属性。

功能概述：
    扫描所有HTML文件，为使用data-src的img标签添加src属性

使用方法：
    python fix_all_html.py

主要特性：
    - 批量处理多个HTML文件
    - 为懒加载图片添加src属性
"""

import os
import re

# 获取脚本所在目录的父目录的父目录（项目根目录）
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))

# 切换到项目根目录
os.chdir(project_root)

html_files = ['index.html', 'cn/index.html', 'en/index.html']

for file_name in html_files:
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 为所有使用data-src的img标签添加src属性
    pattern = r'<img data-src="(assets/favicons/[^"]+)" class="lozad img-circle" width="40">'
    replacement = r'<img src="\1" data-src="\1" class="lozad img-circle" width="40">'
    
    content = re.sub(pattern, replacement, content)
    
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已更新 {file_name}')