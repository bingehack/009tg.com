#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查特定站点脚本

用途：
    检查JSON数据中是否包含特定名称或URL的站点。

功能概述：
    读取JSON数据，查找包含特定关键词（如"金色财经"、"Dwz3"）的站点

使用方法：
    python check_sites.py

主要特性：
    - 按名称和URL搜索站点
    - 支持多个关键词匹配
"""

import json
import os

# 获取脚本所在目录的父目录的父目录（项目根目录）
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))

# 切换到项目根目录
os.chdir(project_root)

data = json.load(open('完整版导航.json', 'r', encoding='utf-8'))
sites = []

def process_group(group):
    if 'sites' in group:
        sites.extend(group['sites'])
    if 'children' in group:
        for child in group['children']:
            process_group(child)

for group in data.get('groups', []):
    process_group(group)

for s in sites:
    name = s.get('name', '')
    url = s.get('url', '')
    if '金色财经' in name or 'Dwz3' in name or 'dwz3' in url:
        print(f"{name}: {url}")
