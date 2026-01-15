#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保持原有风格生成新的导航网站
"""

import json
import re

def keep_style_generate():
    """保持原有风格生成新的HTML"""
    
    # 1. 读取JSON数据
    print("读取JSON数据...")
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 读取原有HTML模板
    print("读取原有HTML模板...")
    with open('cn/index.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 3. 生成新的导航菜单
    print("生成新的导航菜单...")
    nav_html = generate_nav_menu(data['groups'])
    
    # 4. 生成新的内容区域
    print("生成新的内容区域...")
    content_html = generate_content(data['groups'])
    
    # 5. 替换导航菜单
    print("替换导航菜单...")
    # 使用正则表达式替换导航菜单
    template = re.sub(r'<ul id="main-menu" class="main-menu">.*?</ul>', 
                     f'<ul id="main-menu" class="main-menu">{nav_html}</ul>', 
                     template, flags=re.DOTALL)
    
    # 6. 替换内容区域
    print("替换内容区域...")
    # 先找到内容区域的起始和结束位置
    content_start = template.find('<h4 class="text-gray">')
    if content_start != -1:
        # 找到最后一个内容区块的结束位置
        content_end = template.rfind('</div>\n            <br />')
        if content_end != -1:
            # 再找到对应的</div>来结束主内容区域
            main_content_end = template.find('</div>', content_end + 1)
            if main_content_end != -1:
                # 替换内容区域
                new_template = template[:content_start] + content_html + template[main_content_end:]
                template = new_template
    
    # 7. 保存新的HTML文件
    print("保存新的HTML文件...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("生成完成！文件：index.html")

def generate_nav_menu(groups):
    """生成新的导航菜单，保持原有样式"""
    nav_html = ''
    
    # 添加各分类到导航菜单
    for group in groups:
        nav_html += f'''<li>
            <a href="#{group['name']}" class="smooth">
                <i class="linecons-star"></i>
                <span class="title">{group['name']}</span>
            </a>
        </li>'''
    
    # 添加关于本站链接
    nav_html += '''<li>
        <a href="about.html">
            <i class="linecons-heart"></i>
            <span class="tooltip-blue">关于本站</span>
            <span class="label label-Primary pull-right hidden-collapsed">♥︎</span>
        </a>
    </li>'''
    
    return nav_html

def generate_content(groups):
    """生成新的内容区域，保持原有样式"""
    content_html = ''
    
    for group in groups:
        # 添加分类标题
        content_html += f'''<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="{group['name']}"></i>{group['name']}</h4>
        <div class="row">'''
        
        # 添加网站卡片
        for site in group['sites']:
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
        content_html += '</div>\n        <br />\n        <!--END ' + group['name'] + ' -->\n        '
    
    return content_html

if __name__ == '__main__':
    keep_style_generate()
