#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单HTML生成脚本

用途：
    生成简单版本的HTML导航文件。

功能概述：
    1. 读取JSON数据
    2. 创建简单的HTML模板
    3. 生成导航菜单和内容区域
    4. 保存为HTML文件

使用方法：
    python simple_generate.py

主要特性：
    - 生成简洁的HTML结构
    - 不依赖复杂的模板
    - 适合快速测试和预览
"""

import json
import os

def simple_generate():
    """生成简单的HTML文件"""
    
    # 获取脚本所在目录的父目录的父目录（项目根目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # 切换到项目根目录
    os.chdir(project_root)
    
    # 1. 读取JSON数据
    print("读取JSON数据...")
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 创建HTML模板
    html_template = '''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的导航 - 跨境电商工具导航</title>
    <meta name="keywords" content="跨境电商,营销工具,AI工具,社交媒体,独立站,广告投放">
    <meta name="description" content="我的导航 - 收集国内外优秀的跨境电商工具、营销资源、AI工具、社交媒体平台等。">
    <link rel="stylesheet" href="cn/assets/css/bootstrap.css">
    <link rel="stylesheet" href="cn/assets/css/xenon-core.css">
    <link rel="stylesheet" href="cn/assets/css/xenon-components.css">
    <link rel="stylesheet" href="cn/assets/css/xenon-skins.css">
    <link rel="stylesheet" href="cn/assets/css/nav.css">
    <script src="cn/assets/js/jquery-1.11.1.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .category {
            margin: 20px 0;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 8px;
        }
        .category h2 {
            margin-top: 0;
            color: #2c3e50;
        }
        .site-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .site-card {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .site-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .site-card h3 {
            margin: 0 0 5px 0;
            font-size: 18px;
        }
        .site-card a {
            color: #3498db;
            text-decoration: none;
        }
        .site-card a:hover {
            text-decoration: underline;
        }
        .site-description {
            color: #666;
            font-size: 14px;
            margin: 5px 0 0 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>我的导航 - 跨境电商工具导航</h1>
        
        {content}
        
    </div>
</body>
</html>'''
    
    # 3. 生成内容
    content = ''
    for group in data['groups']:
        content += f'<div class="category"><h2>{group["name"]}</h2><div class="site-list">'
        
        for site in group['sites']:
            site_name = site.get('name', '未知网站')
            site_url = site.get('url', '#')
            site_description = site.get('description', '')
            
            content += f'''<div class="site-card">
                <h3><a href="{site_url}" target="_blank">{site_name}</a></h3>
                <p class="site-description">{site_description}</p>
            </div>'''
        
        content += '</div></div>'
    
    # 4. 替换模板内容
    html = html_template.replace('{content}', content)
    
    # 5. 保存文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("生成完成！文件：index.html")

if __name__ == '__main__':
    simple_generate()
