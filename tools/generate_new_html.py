#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新HTML生成脚本

用途：
    生成新的导航网站HTML文件。

功能概述：
    1. 读取JSON数据
    2. 构建层级结构（大类和小类）
    3. 生成导航菜单（支持层级展开）
    4. 生成内容区域（支持分页）
    5. 保存为HTML文件

使用方法：
    python generate_new_html.py

主要特性：
    - 生成完整的HTML结构
    - 支持大类和小类的层级关系
    - 支持自定义导航菜单
    - 支持分页功能
    - 生成内容区域
"""

import json

def build_hierarchy(groups):
    """构建层级结构"""
    hierarchy = {}
    
    for group in groups:
        group_id = group['id']
        parent_id = group.get('parent_id')
        
        if parent_id is None:
            if group_id not in hierarchy:
                hierarchy[group_id] = {
                    'info': group,
                    'children': []
                }
            else:
                hierarchy[group_id]['info'] = group
        else:
            if parent_id in hierarchy:
                hierarchy[parent_id]['children'].append(group)
            else:
                hierarchy[parent_id] = {
                    'info': None,
                    'children': [group]
                }
    
    return hierarchy

def generate_nav_menu(hierarchy):
    """生成导航菜单HTML（支持层级）"""
    nav_menu = []
    
    for parent_id, parent_data in hierarchy.items():
        parent_info = parent_data['info']
        children = parent_data['children']
        
        if parent_info is None:
            continue
        
        if children:
            nav_menu.append(f'''<li>
            <a href="#" class="has-sub">
                <i class="linecons-star"></i>
                <span class="title">{parent_info['name']}</span>
            </a>
            <ul>''')
            
            for child in children:
                nav_menu.append(f'''<li>
                <a href="#{child['name']}" class="smooth">
                    <span class="title">{child['name']}</span>
                </a>
            </li>''')
            
            nav_menu.append('</ul></li>')
        else:
            nav_menu.append(f'''<li>
            <a href="#{parent_info['name']}" class="smooth">
                <i class="linecons-star"></i>
                <span class="title">{parent_info['name']}</span>
            </a>
        </li>''')
    
    return ''.join(nav_menu)

def generate_content_section(group, favicon_mapping, sites_per_page=12):
    """生成单个内容区域HTML（支持分页）"""
    sites = group.get('sites', [])
    section_name = group['name']
    
    if not sites:
        return ''
    
    result = [f'''<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="{section_name}"></i>{section_name}</h4>''']
    
    total_sites = len(sites)
    total_pages = (total_sites + sites_per_page - 1) // sites_per_page
    
    for page_num in range(total_pages):
        start_idx = page_num * sites_per_page
        end_idx = min(start_idx + sites_per_page, total_sites)
        page_sites = sites[start_idx:end_idx]
        
        result.append(f'<div class="row" data-page="{page_num + 1}" data-total-pages="{total_pages}" data-section="{section_name}">')
        
        for site in page_sites:
            site_name = site.get('name', '未知网站')
            site_url = site.get('url', '#')
            site_description = site.get('description', '')
            site_icon = site.get('icon', 'assets/images/logos/default.png')
            
            from urllib.parse import urlparse
            try:
                parsed_url = urlparse(site_url)
                domain = parsed_url.netloc
                if domain in favicon_mapping:
                    site_icon = favicon_mapping[domain]
            except:
                pass
            
            result.append(f'''<div class="col-sm-3">
                <div class="xe-widget xe-conversations box2 label-info" onclick="redirectToSite('{site_url}', '{site_name}')" data-toggle="tooltip" data-placement="bottom" title="{site_url}">
                    <div class="xe-comment-entry">
                        <a class="xe-user-img">
                            <img src="{site_icon}" data-src="{site_icon}" class="lozad img-circle" width="40">
                        </a>
                        <div class="xe-comment">
                            <a href="#" class="xe-user-name overflowClip_1">
                                <strong>{site_name}</strong>
                            </a>
                            <p class="overflowClip_2">{site_description}</p>
                        </div>
                    </div>
                </div>
            </div>''')
        
        result.append('</div>')
        
        if total_pages > 1:
            result.append(f'''<div class="pagination-container" data-section="{section_name}">
                <ul class="pagination">
                    <li class="prev" data-page="{page_num}"><a href="#">«</a></li>''')
            
            for p in range(total_pages):
                active_class = 'active' if p == page_num else ''
                result.append(f'''<li class="{active_class}" data-page="{p}"><a href="#">{p + 1}</a></li>''')
            
            result.append(f'''<li class="next" data-page="{page_num + 2}"><a href="#">»</a></li>
                </ul>
            </div>''')
        
        result.append('<br />')
    
    return ''.join(result)

def generate_html():
    """生成新的HTML文件"""
    
    # 1. 读取JSON数据
    print("读取JSON数据...")
    import os
    json_path = os.path.join(os.path.dirname(__file__), '..', '完整版导航.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1.5. 读取favicon映射
    print("读取favicon映射...")
    favicon_mapping_path = os.path.join(os.path.dirname(__file__), '..', 'favicon_mapping.json')
    with open(favicon_mapping_path, 'r', encoding='utf-8') as f:
        favicon_mapping = json.load(f)
    
    # 2. 构建层级结构
    print("构建层级结构...")
    hierarchy = build_hierarchy(data['groups'])
    
    # 3. 生成导航菜单
    print("生成导航菜单...")
    nav_html = generate_nav_menu(hierarchy)
    
    # 4. 生成内容区域
    print("生成内容区域...")
    content_sections = []
    
    for group in data['groups']:
        content_section = generate_content_section(group, favicon_mapping)
        if content_section:
            content_sections.append(content_section)
    
    content_html = ''.join(content_sections)
    
    # 5. 生成完整HTML
    print("生成完整HTML...")
    html = f'''
<!DOCTYPE html>
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
        function redirectToSite(url, name) {{
            var redirectUrl = 'redirect.html?url=' + encodeURIComponent(url) + '&name=' + encodeURIComponent(name);
            window.location.href = redirectUrl;
        }}
        
        $(document).ready(function() {{
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
            
            // 分页功能
            $('.pagination a').click(function(e) {{
                e.preventDefault();
                var $li = $(this).parent();
                var page = parseInt($li.data('page'));
                var $container = $li.closest('.pagination-container');
                var section = $container.data('section');
                
                if ($li.hasClass('disabled')) {{
                    return;
                }}
                
                // 隐藏该分类的所有页面
                $('div[data-section="' + section + '"]').hide();
                
                // 显示当前页面
                $('div[data-section="' + section + '"][data-page="' + (page + 1) + '"]').show();
                
                // 更新分页按钮状态
                $container.find('.pagination li').removeClass('active disabled');
                $container.find('.pagination li[data-page="' + page + '"]').addClass('active');
                
                if (page === 0) {{
                    $container.find('.pagination li.prev').addClass('disabled');
                }}
                
                var totalPages = parseInt($('div[data-section="' + section + '"]').first().data('total-pages'));
                if (page === totalPages - 1) {{
                    $container.find('.pagination li.next').addClass('disabled');
                }}
            }});
            
            // 初始化分页：只显示第一页
            $('.row[data-page]').each(function() {{
                var page = parseInt($(this).data('page'));
                var totalPages = parseInt($(this).data('total-pages'));
                var section = $(this).data('section');
                
                if (page > 1) {{
                    $(this).hide();
                }}
                
                // 更新分页按钮状态
                var $container = $(this).next('.pagination-container');
                if ($container.length > 0) {{
                    $container.find('.pagination li.prev').addClass('disabled');
                    if (totalPages === 1) {{
                        $container.find('.pagination li.next').addClass('disabled');
                    }}
                }}
            }});
        }});
        
        // 处理has-sub菜单展开/收起
        $(document).on('click', '.has-sub', function(e) {{
            e.preventDefault();
            var $this = $(this);
            var $parent = $this.parent('li');
            
            if ($parent.hasClass('expanded')) {{
                $parent.removeClass('expanded');
                $this.next('ul').slideUp(200);
            }} else {{
                $parent.addClass('expanded');
                $this.next('ul').slideDown(200);
            }}
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
    
    # 6. 保存HTML文件
    print("保存HTML文件...")
    output_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("生成完成！文件：index.html")

if __name__ == '__main__':
    generate_html()
