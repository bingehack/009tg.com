#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复导航网站的三个问题
"""

import json
import re

def fix_issues():
    """修复三个问题"""
    
    # 1. 读取JSON数据
    print("读取JSON数据...")
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 构建分类树结构
    print("构建分类树结构...")
    category_tree, category_map = build_category_tree(data['groups'])
    
    # 3. 读取原有HTML模板
    print("读取原有HTML模板...")
    with open('cn/index.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 4. 生成新的导航菜单 - 只包含JSON中的数据
    print("生成新的导航菜单...")
    nav_html = generate_nav_menu(category_tree, category_map)
    
    # 5. 生成新的内容区域 - 只生成小类的内容
    print("生成新的内容区域...")
    content_html = generate_content(data['groups'], category_map)
    
    # 6. 替换导航菜单 - 完全替换，清除旧数据
    print("替换导航菜单...")
    # 使用正则表达式替换导航菜单
    template = re.sub(r'<ul id="main-menu" class="main-menu">.*?</ul>', 
                     f'<ul id="main-menu" class="main-menu">{nav_html}</ul>', 
                     template, flags=re.DOTALL)
    
    # 7. 替换内容区域
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
    
    # 8. 修复资源引用路径
    print("修复资源引用路径...")
    template = template.replace('../assets/', 'assets/')
    
    # 9. 更新网站标题和描述
    print("更新网站标题和描述...")
    template = template.replace('WebStack.cc - 设计师网址导航', '我的导航 - 跨境电商工具导航')
    template = template.replace('UI设计,UI设计素材,设计导航,网址导航,设计资源,创意导航,创意网站导航,设计师网址大全,设计素材大全,设计师导航,UI设计资源,优秀UI设计欣赏,设计师导航,设计师网址大全,设计师网址导航,产品经理网址导航,交互设计师网址导航,www.webstack.cc', '跨境电商,营销工具,AI工具,社交媒体,独立站,广告投放')
    template = template.replace('WebStack - 收集国内外优秀设计网站、UI设计资源网站、灵感创意网站、素材资源网站，定时更新分享优质产品设计书签。www.webstack.cc', '我的导航 - 收集国内外优秀的跨境电商工具、营销资源、AI工具、社交媒体平台等。')
    
    # 10. 保存新的HTML文件
    print("保存新的HTML文件...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("修复完成！文件：index.html")

def build_category_tree(groups):
    """构建分类树结构"""
    category_tree = {}
    category_map = {}
    
    # 首先创建所有分类的映射
    for group in groups:
        category_map[group['id']] = {
            'name': group['name'],
            'parent_id': group['parent_id'],
            'sites': group['sites'],
            'is_parent': False,
            'children': []
        }
    
    # 然后构建父子关系
    for group in groups:
        parent_id = group['parent_id']
        if parent_id is None:
            # 大类，直接添加到树中
            category_tree[group['id']] = category_map[group['id']]
            category_map[group['id']]['is_parent'] = True
        else:
            # 小类，添加到父类的children中
            if parent_id in category_map:
                category_map[parent_id]['children'].append(category_map[group['id']])
    
    return category_tree, category_map

def generate_nav_menu(category_tree, category_map):
    """生成导航菜单"""
    nav_html = ''
    
    # 遍历所有分类
    for group in category_tree.values():
        children = group['children']
        
        if children:
            # 大类，生成嵌套菜单
            nav_html += f'''<li>
                <a>
                    <i class="linecons-thumbs-up"></i>
                    <span class="title">{group['name']}</span>
                </a>
                <ul>'''
            
            # 添加子分类
            for child in children:
                nav_html += f'''<li>
                    <a href="#{child['name']}" class="smooth">
                        <span class="title">{child['name']}</span>
                    </a>
                </li>'''
            
            nav_html += '''</ul>
            </li>'''
        else:
            # 没有子分类，直接作为菜单项
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

def generate_content(groups, category_map):
    """生成内容区域，只生成小类的内容"""
    content_html = ''
    
    for group in groups:
        # 检查是否为小类（有父类或者没有子分类且有网站）
        group_info = category_map[group['id']]
        
        # 如果是大类且没有网站，则跳过
        if group_info['is_parent'] and not group_info['sites']:
            continue
        
        # 生成内容
        content_html += f'''<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="{group['name']}"></i>{group['name']}</h4>
        <div class="row">'''
        
        # 添加网站卡片
        for site in group['sites']:
            site_name = site.get('name', '未知网站')
            site_url = site.get('url', '#')
            site_description = site.get('description', '')
            site_icon = site.get('icon', 'assets/images/logos/default.png')
            
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
        content_html += f'''</div>
        <br />
        <!--END {group['name']} -->
        '''
    
    return content_html

if __name__ == '__main__':
    fix_issues()
