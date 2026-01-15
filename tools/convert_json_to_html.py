#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON转HTML脚本

用途：
    将JSON格式的导航数据转换为HTML页面。

功能概述：
    1. 读取JSON数据
    2. 读取HTML模板
    3. 生成导航菜单
    4. 生成内容区域
    5. 替换HTML模板中的占位符

使用方法：
    python convert_json_to_html.py

主要特性：
    - 支持完整的JSON数据转换
    - 保持HTML模板结构
    - 生成导航和内容区域
"""

import json
import re

def convert_json_to_html():
    """将JSON数据转换为HTML页面"""
    
    # 1. 读取JSON数据
    print("读取JSON数据...")
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 读取HTML模板
    print("读取HTML模板...")
    with open('cn/index.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 3. 生成导航菜单
    print("生成导航菜单...")
    nav_menu = generate_nav_menu(data['groups'])
    
    # 4. 生成内容区域
    print("生成内容区域...")
    content = generate_content(data['groups'])
    
    # 5. 更新HTML模板
    print("更新HTML模板...")
    new_html = update_template(template, nav_menu, content)
    
    # 6. 保存新的HTML文件
    print("保存新的HTML文件...")
    with open('index_new.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("转换完成！新文件：index_new.html")

def generate_nav_menu(groups):
    """生成导航菜单HTML"""
    nav_html = ''
    
    for group in groups:
        nav_html += f'''<li>
            <a href="#{group["name"]}" class="smooth">
                <i class="linecons-star"></i>
                <span class="title">{group["name"]}</span>
            </a>
        </li>'''
    
    return nav_html

def generate_content(groups):
    """生成内容区域HTML"""
    content_html = ''
    
    for group in groups:
        # 添加分类标题
        content_html += f'''<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="{group["name"]}"></i>{group["name"]}</h4>
        <div class="row">'''
        
        # 添加该分类下的网站卡片
        for site in group['sites']:
            # 确保必要字段存在
            site_name = site.get('name', '未知网站')
            site_url = site.get('url', '#')
            site_description = site.get('description', '')
            site_icon = site.get('icon', '../assets/images/logos/default.png')
            
            content_html += f'''<div class="col-sm-3">
                <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('{site_url}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="{site_url}">
                    <div class="xe-comment-entry">
                        <a class="xe-user-img">
                            <img data-src="{site_icon}" class="lozad img-circle" width="40">
                        </a>
                        <div class="xe-comment">
                            <a href="#" class="xe-user-name overflowClip_1">
                                <strong>{site_name}</strong>
                            </a>
                            <p class="overflowClip_2">{site_description}</p>
                        </div>
                    </div>
                </div>
            </div>'''
        
        # 关闭行容器
        content_html += '</div><br />'
    
    return content_html

def update_template(template, nav_menu, content):
    """更新HTML模板"""
    
    # 更新标题和元信息
    template = template.replace('WebStack.cc - 设计师网址导航', '我的导航 - 跨境电商工具导航')
    template = template.replace('WebStack - 收集国内外优秀设计网站', '我的导航 - 跨境电商工具导航')
    template = template.replace('UI设计,UI设计素材,设计导航', '跨境电商,营销工具,AI工具,社交媒体,独立站')
    
    # 更新导航菜单
    # 找到导航菜单的位置，替换整个ul#main-menu
    menu_pattern = re.compile(r'<ul id="main-menu" class="main-menu">.*?</ul>', re.DOTALL)
    new_menu = f'<ul id="main-menu" class="main-menu">{nav_menu}</ul>'
    template = menu_pattern.sub(new_menu, template)
    
    # 更新内容区域
    # 找到内容区域的位置，替换从第一个h4到JavaScript部分之前的内容
    content_start = template.find('<h4 class="text-gray">')
    
    # 找到JavaScript部分的起始位置，即第一个<script>标签在内容区域之后的位置
    js_start = template.find('        $(function() {', content_start)
    
    if content_start != -1 and js_start != -1:
        new_template = template[:content_start] + content + template[js_start:]
        return new_template
    else:
        print(f"警告：未找到内容区域，content_start={content_start}, js_start={js_start}")
        return template

if __name__ == '__main__':
    convert_json_to_html()
