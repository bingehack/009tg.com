#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复JavaScript动态生成的img标签脚本

用途：
    为JavaScript动态生成的img标签添加src属性。

功能概述：
    修改JavaScript代码中动态生成的img标签，添加src属性以确保图片正确显示

使用方法：
    python fix_javascript_img.py

主要特性：
    - 为懒加载图片添加src属性
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
    
    # 修改JavaScript中的动态生成的img标签，添加src属性
    pattern = r'<img data-src="\$\{site\.icon\}" class="lozad img-circle" width="40">'
    replacement = r'<img src="\${site.icon}" data-src="\${site.icon}" class="lozad img-circle" width="40">'
    
    content = re.sub(pattern, replacement, content)
    
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已更新 {file_name}')