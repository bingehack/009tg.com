#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新HTML生成脚本 - 支持多级分类和翻页功能

用途：
    生成新的导航网站HTML文件，支持多级分类和翻页功能。

功能概述：
    1. 读取JSON数据
    2. 生成嵌套的导航菜单
    3. 生成内容区域（支持翻页）
    4. 保存为HTML文件

使用方法：
    python generate_new_html.py

主要特性：
    - 生成完整的HTML结构
    - 支持多级分类导航菜单
    - 生成内容区域（支持翻页）
    - 使用本地缓存的favicon
"""

import json
from urllib.parse import urlparse

def get_icon_for_category(category_name):
    """根据分类名称获取对应的图标"""
    icon_mapping = {
        "下海推荐": "fa-wrench",
        "AI工具": "fa-microphone",
        "全球资讯": "fa-file-text-o",
        "全球推广": "fa-globe",
        "社媒资源": "fa-share",
        "全球网络": "fa-cloud",
        "Facebook": "fa-facebook",
        "Google": "fa-google",
        "广告工具": "fa-bar-chart",
        "跨境电商": "fa-shopping-cart",
        "投资理财": "fa-briefcase",
        "创业工具": "fa-rocket"
    }
    return icon_mapping.get(category_name, "linecons-star")

def build_category_tree(groups):
    """构建分类树结构"""
    group_dict = {g['id']: g for g in groups}
    root_groups = []
    
    for group in groups:
        if group['parent_id'] is None:
            root_groups.append(group)
        else:
            parent = group_dict.get(group['parent_id'])
            if parent:
                if 'children' not in parent:
                    parent['children'] = []
                parent['children'].append(group)
    
    return root_groups

def generate_nav_menu(groups):
    """生成导航菜单HTML"""
    def generate_menu_item(group, level=0):
        icon_class = get_icon_for_category(group['name']) if level == 0 else None
        
        has_children = 'children' in group and len(group['children']) > 0
        
        if has_children:
            children_html = ''.join([generate_menu_item(child, level + 1) for child in group['children']])
            if icon_class:
                return f'''<li>
                <a>
                    <i class="{icon_class}"></i>
                    <span class="title">{group['name']}</span>
                </a>
                <ul>{children_html}</ul>
            </li>'''
            else:
                return f'''<li>
                <a>
                    <span class="title">{group['name']}</span>
                </a>
                <ul>{children_html}</ul>
            </li>'''
        else:
            return f'''<li>
                <a href="#{group['name']}" class="smooth">
                    <span class="title">{group['name']}</span>
                </a>
            </li>'''
    
    return ''.join([generate_menu_item(group) for group in groups])

def generate_site_data(group, favicon_mapping):
    """生成网站数据JavaScript"""
    sites_data = []
    
    for site in group.get('sites', []):
        site_name = site.get('name', '未知网站')
        site_url = site.get('url', '#')
        site_description = site.get('description', '')
        site_icon = site.get('icon', '../assets/images/logos/default.png')
        
        try:
            parsed_url = urlparse(site_url)
            domain = parsed_url.netloc
            if domain in favicon_mapping:
                site_icon = favicon_mapping[domain]
        except:
            pass
        
        sites_data.append({
            'name': site_name,
            'url': site_url,
            'description': site_description,
            'icon': site_icon
        })
    
    return sites_data

def generate_all_sites_data(groups, favicon_mapping):
    """生成所有网站数据JavaScript"""
    sites_data_js = []
    
    def process_group(group):
        if group.get('sites'):
            category_name = group['name']
            sites = generate_site_data(group, favicon_mapping)
            sites_json = json.dumps(sites, ensure_ascii=False)
            sites_data_js.append(f"allSitesData['{category_name}'] = {sites_json};")
        if 'children' in group:
            for child in group['children']:
                process_group(child)
    
    for group in groups:
        process_group(group)
    
    return '\n        '.join(sites_data_js)

def generate_content_section(group, favicon_mapping):
    """生成内容区域HTML"""
    sites = group.get('sites', [])
    total_sites = len(sites)
    category_name = group['name']
    
    # 根据网站数量决定是否启用分页
    enable_pagination = total_sites > 4
    
    return f'''<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="{category_name}"></i>{category_name}</h4>
<div class="row category-row" data-category="{category_name}" data-total="{total_sites}" data-pagination="{str(enable_pagination).lower()}">
    <div class="pagination-left"></div>
    <div class="category-content"></div>
    <div class="pagination-right"></div>
</div>
<br />'''

def generate_all_content(groups, favicon_mapping):
    """生成所有内容区域"""
    content_sections = []
    
    def process_group(group):
        if group.get('sites'):
            content_sections.append(generate_content_section(group, favicon_mapping))
        if 'children' in group:
            for child in group['children']:
                process_group(child)
    
    for group in groups:
        process_group(group)
    
    return ''.join(content_sections)

def generate_html():
    """生成新的HTML文件"""
    
    import os
    
    print("读取JSON数据...")
    json_path = os.path.join(os.path.dirname(__file__), '..', '完整版导航.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("读取favicon映射...")
    favicon_mapping_path = os.path.join(os.path.dirname(__file__), '..', 'favicon_mapping.json')
    with open(favicon_mapping_path, 'r', encoding='utf-8') as f:
        favicon_mapping = json.load(f)
    
    print("构建分类树...")
    root_groups = build_category_tree(data['groups'])
    
    print("生成导航菜单...")
    nav_html = generate_nav_menu(root_groups)
    
    print("生成网站数据...")
    sites_data_js = generate_all_sites_data(root_groups, favicon_mapping)
    
    print("生成内容区域...")
    content_html = generate_all_content(root_groups, favicon_mapping)
    
    print("生成完整HTML...")
    html = f'''<!DOCTYPE html>
<html lang="zh">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="author" content="Invisible man" />
    <title>009tg下海导航 - Invisible Man</title>
    <meta name="theme-color" content="#f9f9f9"/>
    <meta name="keywords" content="009tg下海导航,网址导航,上网导航,网址大全,网址目录,创业工具,副业赚钱,投资理财,跨境电商,营销工具,AI工具,社交媒体,独立站,广告投放"/>
    <meta name="description" content="009tg下海导航致力于打造国内最好的互联网上优质网站网址大全，收录了全网好用强大的网站网址和软件包括创业、副业、投资、跨境电商、营销工具、AI工具、社交媒体、独立站、广告投放、生活、休闲、办公、工具、资源等超全面的网址和职业技巧内容，让您的上网体验更便捷更放心，努力成为全民级人人都在用的网址导航。"/>
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
                                <a href="../en/index.html">
                                    <img src="assets/images/flags/flag-us.png" alt="flag-us" /> English
                                </a>
                            </li>
                            <li class="active">
                                <a href="../cn/index.html">
                                    <img src="assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
                <ul class="user-info-menu right-links list-inline list-unstyled">
                    <li class="hidden-sm hidden-xs" style="display: none;">
                        <a href="https://github.com/bingehack/0009tg.com" target="_blank">
                            <i class="fa-github"></i>  GitHub
                        </a>
                    </li>
                </ul>
            </nav>
            {content_html}
        </div>
    </div>
    <script>
        var allSitesData = {{}};
        var currentPage = {{}};
        var itemsPerPage = 4;
        
        {sites_data_js}
        
        $(document).ready(function() {{
            var observer = lozad();
            
            $('.category-row').each(function() {{
                var categoryName = $(this).data('category');
                var categoryRow = $(this);
                var contentDiv = categoryRow.find('.category-content');
                var leftPagination = categoryRow.find('.pagination-left');
                var rightPagination = categoryRow.find('.pagination-right');
                var enablePagination = $(this).data('pagination');
                
                var sites = allSitesData[categoryName] || [];
                
                contentDiv.empty();
                
                if (sites.length > 0) {{
                    if (enablePagination) {{
                        var startIndex = 0;
                        var endIndex = Math.min(startIndex + itemsPerPage, sites.length);
                        
                        for (var i = startIndex; i < endIndex; i++) {{
                            var site = sites[i];
                            var siteHtml = `<div class="col-sm-3">
                                <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('redirect.html?url=${{encodeURIComponent(site.url)}}&name=${{encodeURIComponent(site.name)}}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="${{site.url}}">
                                    <div class="xe-comment-entry">
                                        <a class="xe-user-img">
                                            <img src="${{site.icon}}" data-src="${{site.icon}}" class="lozad img-circle" width="40">
                                        </a>
                                        <div class="xe-comment">
                                            <a href="#" class="xe-user-name overflowClip_1">
                                                <strong>${{site.name}}</strong>
                                            </a>
                                            <p class="overflowClip_2">${{site.description}}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                            contentDiv.append(siteHtml);
                        }}
                    }} else {{
                        for (var i = 0; i < sites.length; i++) {{
                            var site = sites[i];
                            var siteHtml = `<div class="col-sm-3">
                                <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('redirect.html?url=${{encodeURIComponent(site.url)}}&name=${{encodeURIComponent(site.name)}}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="${{site.url}}">
                                    <div class="xe-comment-entry">
                                        <a class="xe-user-img">
                                            <img src="${{site.icon}}" data-src="${{site.icon}}" class="lozad img-circle" width="40">
                                        </a>
                                        <div class="xe-comment">
                                            <a href="#" class="xe-user-name overflowClip_1">
                                                <strong>${{site.name}}</strong>
                                            </a>
                                            <p class="overflowClip_2">${{site.description}}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                            contentDiv.append(siteHtml);
                        }}
                    }}
                }}
                
                if (leftPagination.length > 0 && enablePagination) {{
                    var totalPages = Math.ceil(sites.length / itemsPerPage);
                    leftPagination.find('.prev-page').prop('disabled', true);
                    rightPagination.find('.next-page').prop('disabled', totalPages <= 1);
                }}
            }});
            
            observer.observe();
            
            function changePage(categoryName, pageNum) {{
                var categoryRow = $('.category-row[data-category="' + categoryName + '"]');
                var contentDiv = categoryRow.find('.category-content');
                var leftPagination = categoryRow.find('.pagination-left');
                var rightPagination = categoryRow.find('.pagination-right');
                var enablePagination = categoryRow.data('pagination');
                
                contentDiv.css('opacity', '0.5');
                
                if (leftPagination.length > 0 && enablePagination) {{
                    leftPagination.find('button').prop('disabled', true);
                    rightPagination.find('button').prop('disabled', true);
                }}
                
                setTimeout(function() {{
                    var sites = allSitesData[categoryName] || [];
                    
                    currentPage[categoryName] = pageNum;
                    var totalPages = Math.ceil(sites.length / itemsPerPage);
                    
                    contentDiv.empty();
                    
                    if (sites.length > 0 && enablePagination) {{
                        var startIndex = (pageNum - 1) * itemsPerPage;
                        var endIndex = Math.min(startIndex + itemsPerPage, sites.length);
                        
                        for (var i = startIndex; i < endIndex; i++) {{
                            var site = sites[i];
                            var siteHtml = `<div class="col-sm-3">
                                <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('redirect.html?url=${{encodeURIComponent(site.url)}}&name=${{encodeURIComponent(site.name)}}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="${{site.url}}">
                                    <div class="xe-comment-entry">
                                        <a class="xe-user-img">
                                            <img src="${{site.icon}}" data-src="${{site.icon}}" class="lozad img-circle" width="40">
                                        </a>
                                        <div class="xe-comment">
                                            <a href="#" class="xe-user-name overflowClip_1">
                                                <strong>${{site.name}}</strong>
                                            </a>
                                            <p class="overflowClip_2">${{site.description}}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                            contentDiv.append(siteHtml);
                        }}
                    }}
                    
                    if (leftPagination.length > 0 && enablePagination) {{
                        leftPagination.find('.prev-page').prop('disabled', pageNum === 1);
                        rightPagination.find('.next-page').prop('disabled', pageNum === totalPages);
                    }}
                    
                    contentDiv.css('opacity', '1');
                    
                    observer.observe();
                }}, 300);
            }}
            
            $('.smooth').click(function(e) {{
                var href = $(this).attr("href");
                var pos = $(href).position().top - 30;
                $(".sidebar-menu").find("li").removeClass("active");
                $(this).parent("li").addClass("active");
                e.preventDefault();
                $("html,body").animate({{
                    scrollTop: pos
                }}, 1000);
            }});
        }});
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
    
    print("保存HTML文件...")
    output_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("生成完成！文件：index.html")

if __name__ == '__main__':
    generate_html()
