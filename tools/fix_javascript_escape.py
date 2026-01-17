#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复JavaScript转义变量脚本

用途：
    修复动态生成的img标签中的转义变量问题。

功能概述：
    修复JavaScript模板字符串中的转义变量（如\${site.icon}），确保变量能够正确插值到动态生成的HTML中

使用方法：
    python fix_javascript_escape.py

主要特性：
    - 移除错误的反斜杠转义
    - 支持多个HTML文件（index.html, cn/index.html, en/index.html）
"""

import os

# 获取脚本所在目录的父目录（项目根目录）
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# 切换到项目根目录
os.chdir(project_root)

html_files = ['index.html', 'cn/index.html', 'en/index.html']

for file_name in html_files:
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复JavaScript中的动态生成的img标签，移除错误的反斜杠
    # 直接使用字符串替换
    old_str = '<img src="\\${site.icon}" class="img-circle" width="40">'
    new_str = '<img src="${site.icon}" class="img-circle" width="40">'
    
    count = content.count(old_str)
    content = content.replace(old_str, new_str)
    
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已更新 {file_name}，修复了 {count} 处')
