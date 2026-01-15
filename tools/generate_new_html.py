#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新HTML生成脚本

用途：
    生成新的导航网站HTML文件。

功能概述：
    1. 读取JSON数据
    2. 生成导航菜单
    3. 生成内容区域
    4. 保存为HTML文件

使用方法：
    python generate_new_html.py

主要特性：
    - 生成完整的HTML结构
    - 支持自定义导航菜单
    - 生成内容区域
"""

import json

def generate_html():
    """生成新的HTML文件"""
    
    # 1. 读取JSON数据
    print("读取JSON数据...")
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 生成导航菜单
    print("生成导航菜单...")
    nav_menu = []
    for group in data['groups']:
        nav_menu.append(f'''<li>
            <a href="#{group['name']}" class="smooth">
                <i class="linecons-star"></i>
                <span class="title">{group['name']}</span>
            </a>
        </li>''')
    nav_html = ''.join(nav_menu)
    
    # 3. 生成内容区域
    print("生成内容区域...")
    content_sections = []
    for group in data['groups']:
        # 添加分类标题
        section = [f'''<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="{group['name']}"></i>{group['name']}</h4>
        <div class="row">''']
        
        # 添加网站卡片
        for site in group['sites']:
            site_name = site.get('name', '未知网站')
            site_url = site.get('url', '#')
            site_description = site.get('description', '')
            site_icon = site.get('icon', '../assets/images/logos/default.png')
            
            section.append(f'''<div class="col-sm-3">
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
            </div>''')
        
        # 关闭行容器
        section.append('</div><br />')
        content_sections.append(''.join(section))
    
    content_html = ''.join(content_sections)
    
    # 4. 生成完整HTML
    print("生成完整HTML...")
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
    
    # 5. 保存HTML文件
    print("保存HTML文件...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("生成完成！文件：index.html")

if __name__ == '__main__':
    generate_html()
