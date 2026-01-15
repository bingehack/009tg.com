#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旧数据清理脚本

用途：
    清除HTML文件中的旧数据，重新生成干净的HTML文件。

功能概述：
    1. 读取JSON格式的导航数据
    2. 构建分类树结构
    3. 生成全新的HTML文件（不包含任何旧数据）
    4. 保存到index.html

使用方法：
    python cleanup_old_data.py

主要特性：
    - 完全重新生成HTML，确保无旧数据残留
    - 保持JSON数据结构不变
    - 生成干净的HTML文件
"""

import json

def cleanup_old_data():
    """彻底清除旧数据"""
    
    # 1. 读取JSON数据
    print("读取JSON数据...")
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 构建分类树结构
    print("构建分类树结构...")
    category_tree, category_map = build_category_tree(data['groups'])
    
    # 3. 生成全新的HTML文件
    print("生成全新的HTML文件...")
    html = generate_full_html(category_tree, category_map, data['groups'])
    
    # 4. 保存新的HTML文件
    print("保存新的HTML文件...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("清理完成！文件：index.html")

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

def generate_full_html(category_tree, category_map, groups):
    """生成完整的HTML文件"""
    
    # 生成导航菜单
    nav_html = generate_nav_menu(category_tree)
    
    # 生成内容区域
    content_html = generate_content(groups, category_map)
    
    # 完整的HTML模板
    html = f'''
<!DOCTYPE html>
<html lang="zh">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="author" content="viggo" />
    <title>我的导航 - 跨境电商工具导航</title>
    <meta name="keywords" content="跨境电商,营销工具,AI工具,社交媒体,独立站,广告投放">
    <meta name="description" content="我的导航 - 收集国内外优秀的跨境电商工具、营销资源、AI工具、社交媒体平台等。">
    <link rel="shortcut icon" href="assets/images/favicon.png">
    <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Arimo:400,700,400italic">
    <link rel="stylesheet" href="assets/css/fonts/linecons/css/linecons.css">
    <link rel="stylesheet" href="assets/css/fonts/fontawesome/css/font-awesome.min.css">
    <link rel="stylesheet" href="assets/css/bootstrap.css">
    <link rel="stylesheet" href="assets/css/xenon-core.css">
    <link rel="stylesheet" href="assets/css/xenon-components.css">
    <link rel="stylesheet" href="assets/css/xenon-skins.css">
    <link rel="stylesheet" href="assets/css/nav.css">
    <script src="assets/js/jquery-1.11.1.min.js"></script>
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <!-- / FB Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="http://www.webstack.cc/">
    <meta property="og:title" content="我的导航 - 跨境电商工具导航">
    <meta property="og:description" content="我的导航 - 收集国内外优秀的跨境电商工具、营销资源、AI工具、社交媒体平台等。">
    <meta property="og:image" content="assets/images/webstack_banner_cn.png">
    <meta property="og:site_name" content="我的导航 - 跨境电商工具导航">
    <!-- / Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="我的导航 - 跨境电商工具导航">
    <meta name="twitter:description" content="我的导航 - 收集国内外优秀的跨境电商工具、营销资源、AI工具、社交媒体平台等。">
    <meta name="twitter:image" content="assets/images/webstack_banner_cn.png">
</head>

<body class="page-body">
    <!-- skin-white -->
    <div class="page-container">
        <div class="sidebar-menu toggle-others fixed">
            <div class="sidebar-menu-inner">
                <header class="logo-env">
                    <!-- logo -->
                    <div class="logo">
                        <a href="index.html" class="logo-expanded">
                            <img src="assets/images/logo@2x.png" width="100%" alt="" />
                        </a>
                        <a href="index.html" class="logo-collapsed">
                            <img src="assets/images/logo-collapsed@2x.png" width="40" alt="" />
                        </a>
                    </div>
                    <div class="mobile-menu-toggle visible-xs">
                        <a href="#" data-toggle="user-info-menu">
                            <i class="linecons-cog"></i>
                        </a>
                        <a href="#" data-toggle="mobile-menu">
                            <i class="fa-bars"></i>
                        </a>
                    </div>
                </header>
                <ul id="main-menu" class="main-menu">
                    {nav_html}
                    <li>
                        <a href="about.html">
                            <i class="linecons-heart"></i>
                            <span class="tooltip-blue">关于本站</span>
                            <span class="label label-Primary pull-right hidden-collapsed">♥︎</span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        <div class="main-content">
            <nav class="navbar user-info-navbar" role="navigation">
                <!-- User Info, Notifications and Menu Bar -->
                <!-- Left links for user info navbar -->
                <ul class="user-info-menu left-links list-inline list-unstyled">
                    <li class="hidden-sm hidden-xs">
                        <a href="#" data-toggle="sidebar">
                            <i class="fa-bars"></i>
                        </a>
                    </li>
                    <li class="dropdown hover-line language-switcher">
                        <a href="index.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                        </a>
                        <ul class="dropdown-menu languages">
                            <li>
                                <a href="en/index.html">
                                    <img src="assets/images/flags/flag-us.png" alt="flag-us" /> English
                                </a>
                            </li>
                            <li class="active">
                                <a href="index.html">
                                    <img src="assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
                <ul class="user-info-menu right-links list-inline list-unstyled">
                    <li class="hidden-sm hidden-xs">
                        <a href="https://github.com/WebStackPage/WebStackPage.github.io" target="_blank">
                            <i class="fa-github"></i>  GitHub
                        </a>
                    </li>
                </ul>
            </nav>
            {content_html}
        </div>
    </div>
    <script>
        $(document).ready(function() {
            $('.smooth').click(function(e) {
                var href = $(this).attr("href");
                var pos = $(href).position().top - 30;
                $(".sidebar-menu").find("li").removeClass("active");
                $(this).parent("li").addClass("active");
                e.preventDefault();
                $("html,body").animate({
                    scrollTop: pos
                }, 1000);
            });
        });
    </script>
    <!-- Bottom Scripts -->
    <script src="assets/js/bootstrap.min.js"></script> 
    <script src="assets/js/TweenMax.min.js"></script>  
    <script src="assets/js/resizeable.js"></script>    
    <script src="assets/js/joinable.js"></script>      
    <script src="assets/js/xenon-api.js"></script>     
    <script src="assets/js/xenon-toggles.js"></script> 
    <!-- JavaScripts initializations and stuff -->        
    <script src="assets/js/xenon-custom.js"></script>  
    <script src="assets/js/lozad.js"></script>
</body>

</html>
'''
    
    return html

def generate_nav_menu(category_tree):
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
    
    return nav_html

def generate_content(groups, category_map):
    """生成内容区域"""
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
    cleanup_old_data()
