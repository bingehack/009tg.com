#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML生成脚本

用途：
    从JSON数据生成HTML导航页面，支持多语言和favicon缓存。

功能概述：
    1. 读取JSON格式的导航数据
    2. 构建分类树结构
    3. 生成导航菜单HTML
    4. 生成内容区域HTML（包含分页功能）
    5. 支持加载本地缓存的favicon
    6. 生成中文、英文版本HTML

使用方法：
    python final_fix.py

主要特性：
    - 支持响应式布局和分页功能
    - 优先使用本地缓存的favicon
    - 自动生成多语言版本
    - 支持自定义主题和样式
"""

import json
import os
from urllib.parse import urlparse
import hashlib

def load_favicon_mapping():
    """加载favicon映射关系"""
    mapping_file = 'favicon_mapping.json'
    if os.path.exists(mapping_file):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_domain_from_url(url):
    """从URL中提取域名"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if ':' in domain:
            domain = domain.split(':')[0]
        return domain
    except:
        return None

def final_fix():
    """最终修复"""
    
    # 1. 读取JSON数据
    print("读取JSON数据...")
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 加载favicon映射
    print("加载favicon映射...")
    favicon_mapping = load_favicon_mapping()
    print(f"已加载 {len(favicon_mapping)} 个favicon映射")
    
    # 3. 构建分类树结构
    category_tree, category_map = build_category_tree(data['groups'])
    
    # 生成HTML内容
    print("生成HTML内容...")
    
    # 生成导航菜单
    nav_html = generate_nav_menu(category_tree)
    
    # 生成内容区域和网站数据
    content_html, sites_data_json = generate_content(data['groups'], category_map, favicon_mapping)
    
    # 4. 读取干净的HTML模板
    template = '''<!DOCTYPE html>
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
    <style>
        /* 分页行容器 */
        .category-row {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        /* 左侧翻页按钮 */
        .pagination-left {
            display: flex;
            align-items: center;
            padding-right: 15px;
            flex-shrink: 0;
            width: 40px;
        }
        
        /* 右侧翻页按钮 */
        .pagination-right {
            display: flex;
            align-items: center;
            padding-left: 15px;
            flex-shrink: 0;
            width: 40px;
        }
        
        /* 内容区域 */
        .category-content {
            flex-grow: 1;
            transition: opacity 0.3s ease;
            display: flex;
            flex-wrap: wrap;
            gap: 0;
        }
        
        /* 网站项 - 响应式网格布局 */
        .site-item {
            flex: 0 0 calc(16.666% - 15px);
            max-width: calc(16.666% - 15px);
            margin: 0 15px 15px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        /* 翻页按钮样式 */
        .pagination-left .btn,
        .pagination-right .btn {
            padding: 8px 12px;
            min-width: 40px;
            transition: all 0.3s ease;
            border-radius: 4px;
            background: #f5f5f5;
            border: 1px solid #ddd;
        }
        
        .pagination-left .btn:hover:not(:disabled),
        .pagination-right .btn:hover:not(:disabled) {
            background: #e0e0e0;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        }
        
        .pagination-left .btn:disabled,
        .pagination-right .btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
            background: #f0f0f0;
        }
        
        /* 响应式设计 */
        @media (max-width: 1400px) {
            .site-item {
                flex: 0 0 calc(25% - 15px);
                max-width: calc(25% - 15px);
            }
        }
        
        @media (max-width: 1200px) {
            .site-item {
                flex: 0 0 calc(33.333% - 15px);
                max-width: calc(33.333% - 15px);
            }
        }
        
        @media (max-width: 992px) {
            .site-item {
                flex: 0 0 calc(50% - 15px);
                max-width: calc(50% - 15px);
            }
        }
        
        @media (max-width: 768px) {
            .category-row {
                flex-direction: column;
                gap: 10px;
            }
            
            .pagination-left,
            .pagination-right {
                width: 100%;
                justify-content: center;
                padding: 0;
                height: auto;
            }
            
            .pagination-left .btn,
            .pagination-right .btn {
                width: 100%;
                min-width: auto;
            }
            
            .category-content {
                width: 100%;
            }
            
            .site-item {
                flex: 0 0 calc(50% - 15px);
                max-width: calc(50% - 15px);
            }
        }
        
        @media (max-width: 480px) {
            .site-item {
                flex: 0 0 100%;
                max-width: 100%;
                margin: 0 0 15px 0;
            }
            
            .pagination-left .btn,
            .pagination-right .btn {
                padding: 6px 10px;
                font-size: 12px;
            }
        }
        
        /* 网站项悬停效果 */
        .site-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
    </style>
    <script src="assets/js/jquery-1.11.1.min.js"></script>
    <script src="assets/js/lozad.js"></script>
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
                    {nav_menu}
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
            <script>
                // 存储所有分类的网站数据
                var allSitesData = {sites_data};
            </script>
            {content}
        </div>
    </div>
    <script>
        $(document).ready(function() {
            $('.smooth').click(function(e) {
                var href = $(this).attr("href");
                var pos = $(href).position().top - 30;
                $(this).parent("li").addClass("active");
                e.preventDefault();
                $("html,body").animate({
                    scrollTop: pos
                }, 1000);
            });
            
            const observer = lozad();
            observer.observe();
            
            // 分页功能
            var categoryData = {};
            var currentPage = {};
            var itemsPerPage = 15;
            
            // 根据屏幕宽度计算每页显示数量
            function calculateItemsPerPage() {
                var windowWidth = $(window).width();
                if (windowWidth > 1400) {
                    return 18; // 6列 × 3行
                } else if (windowWidth > 1200) {
                    return 12; // 4列 × 3行
                } else if (windowWidth > 992) {
                    return 9;  // 3列 × 3行
                } else if (windowWidth > 768) {
                    return 6;  // 2列 × 3行
                } else if (windowWidth > 480) {
                    return 6;  // 2列 × 3行
                } else {
                    return 3;  // 1列 × 3行
                }
            }
            
            // 窗口大小改变时重新计算每页显示数量
            $(window).resize(function() {
                var newItemsPerPage = calculateItemsPerPage();
                if (newItemsPerPage !== itemsPerPage) {
                    itemsPerPage = newItemsPerPage;
                    // 重新加载所有分类的第一页
                    $('.category-row').each(function() {
                        var categoryName = $(this).data('category');
                        currentPage[categoryName] = 1;
                        changePage(categoryName, 1);
                    });
                }
            });
            
            // 初始化分类数据
            $('.category-row').each(function() {
                var categoryName = $(this).data('category');
                var totalItems = $(this).data('total');
                categoryData[categoryName] = totalItems;
                currentPage[categoryName] = 1;
            });
            
            // 初始计算每页显示数量
            itemsPerPage = calculateItemsPerPage();
            
            // 初始化所有分类，显示第一页
            $('.category-row').each(function() {
                var categoryName = $(this).data('category');
                var categoryRow = $(this);
                var contentDiv = categoryRow.find('.category-content');
                var leftPagination = categoryRow.find('.pagination-left');
                var rightPagination = categoryRow.find('.pagination-right');
                
                // 获取该分类的所有网站数据
                var sites = allSitesData[categoryName] || [];
                
                // 清空当前内容
                contentDiv.empty();
                
                // 计算当前页的起始和结束索引
                var startIndex = 0;
                var endIndex = Math.min(itemsPerPage, sites.length);
                
                // 添加当前页的网站项
                for (var i = startIndex; i < endIndex; i++) {
                    var site = sites[i];
                    if (site) {
                        var siteHtml = `<div class="site-item" data-index="${i}">
                            <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('${site.url}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="${site.url}">
                                <div class="xe-comment-entry">
                                    <a class="xe-user-img">
                                        <img data-src="${site.icon}" class="lozad img-circle" width="40">
                                    </a>
                                    <div class="xe-comment">
                                        <a href="#" class="xe-user-name overflowClip_1">
                                            <strong>${site.name}</strong>
                                        </a>
                                        <p class="overflowClip_2">${site.description}</p>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                        contentDiv.append(siteHtml);
                    }
                }
                
                // 更新按钮状态（如果存在翻页按钮）
                if (leftPagination.length > 0) {
                    var totalPages = Math.ceil(sites.length / itemsPerPage);
                    leftPagination.find('.prev-page').prop('disabled', true);
                    rightPagination.find('.next-page').prop('disabled', totalPages <= 1);
                }
            });
            
            // 重新初始化懒加载
            observer.observe();
            
            // 上一页按钮点击事件
            $('.prev-page').click(function() {
                var categoryName = $(this).data('category');
                var currentPageNum = currentPage[categoryName];
                
                if (currentPageNum > 1) {
                    changePage(categoryName, currentPageNum - 1);
                }
            });
            
            // 下一页按钮点击事件
            $('.next-page').click(function() {
                var categoryName = $(this).data('category');
                var currentPageNum = currentPage[categoryName];
                var totalPages = Math.ceil(categoryData[categoryName] / itemsPerPage);
                
                if (currentPageNum < totalPages) {
                    changePage(categoryName, currentPageNum + 1);
                }
            });
            
            // 切换页面函数
            function changePage(categoryName, pageNum) {
                var categoryRow = $('.category-row[data-category="' + categoryName + '"]');
                var contentDiv = categoryRow.find('.category-content');
                var leftPagination = categoryRow.find('.pagination-left');
                var rightPagination = categoryRow.find('.pagination-right');
                
                // 显示加载状态
                contentDiv.css('opacity', '0.5');
                if (leftPagination.length > 0) {
                    leftPagination.find('button').prop('disabled', true);
                    rightPagination.find('button').prop('disabled', true);
                }
                
                // 模拟加载延迟
                setTimeout(function() {
                    // 获取该分类的所有网站数据
                    var sites = allSitesData[categoryName] || [];
                    
                    // 清空当前内容
                    contentDiv.empty();
                    
                    // 计算当前页的起始和结束索引
                    var startIndex = (pageNum - 1) * itemsPerPage;
                    var endIndex = Math.min(startIndex + itemsPerPage, sites.length);
                    
                    // 添加当前页的网站项
                    for (var i = startIndex; i < endIndex; i++) {
                        var site = sites[i];
                        if (site) {
                            var siteHtml = `<div class="site-item" data-index="${i}">
                                <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('${site.url}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="${site.url}">
                                    <div class="xe-comment-entry">
                                        <a class="xe-user-img">
                                            <img data-src="${site.icon}" class="lozad img-circle" width="40">
                                        </a>
                                        <div class="xe-comment">
                                            <a href="#" class="xe-user-name overflowClip_1">
                                                <strong>${site.name}</strong>
                                            </a>
                                            <p class="overflowClip_2">${site.description}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                            contentDiv.append(siteHtml);
                        }
                    }
                    
                    // 更新当前页码
                    currentPage[categoryName] = pageNum;
                    var totalPages = Math.ceil(sites.length / itemsPerPage);
                    
                    // 更新按钮状态（如果存在翻页按钮）
                    if (leftPagination.length > 0) {
                        leftPagination.find('.prev-page').prop('disabled', pageNum === 1);
                        rightPagination.find('.next-page').prop('disabled', pageNum === totalPages);
                    }
                    
                    // 恢复显示状态
                    contentDiv.css('opacity', '1');
                    
                    // 重新初始化懒加载
                    observer.observe();
                    
                    // 添加过渡动画
                    contentDiv.find('.site-item').hide().fadeIn(300);
                }, 300);
            }
            
            // Favicon加载失败时的fallback机制
            function getFallbackFavicon(domain) {
                // 尝试多个favicon服务
                const services = [
                    `https://www.google.com/s2/favicons?domain=${domain}&sz=64`,
                    `https://favicon.yandex.net/favicon/${domain}`,
                    `https://api.statvoo.com/favicon/${domain}`,
                    `https://www.faviconextractor.com/favicon/${domain}?larger=true`
                ];
                return services;
            }
            
            // 为所有favicon图片添加错误处理
            $(document).on('error', 'img.lozad', function() {
                const img = $(this);
                const currentSrc = img.attr('src');
                
                // 尝试从URL中提取域名
                let domain = '';
                if (currentSrc.includes('domain=')) {
                    const match = currentSrc.match(/domain=([^&]+)/);
                    if (match) {
                        domain = match[1];
                    }
                }
                
                // 如果是Google favicon服务失败，尝试其他服务
                if (currentSrc.includes('google.com/s2/favicons')) {
                    const fallbackServices = getFallbackFavicon(domain);
                    const currentServiceIndex = fallbackServices.indexOf(currentSrc);
                    
                    if (currentServiceIndex < fallbackServices.length - 1) {
                        // 尝试下一个服务
                        img.attr('src', fallbackServices[currentServiceIndex + 1]);
                    } else {
                        // 所有服务都失败，使用默认图标
                        img.attr('src', 'assets/images/logos/default.png');
                    }
                } else if (currentSrc.includes('faviconextractor.com') || 
                           currentSrc.includes('yandex.net') || 
                           currentSrc.includes('statvoo.com')) {
                    // 其他服务失败，使用默认图标
                    img.attr('src', 'assets/images/logos/default.png');
                }
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
</body>

</html>'''
    
    # 替换模板中的占位符
    html = template.replace('{nav_menu}', nav_html)
    html = html.replace('{content}', content_html)
    html = html.replace('{sites_data}', sites_data_json)
    
    # 5. 保存新的HTML文件
    print("保存新的HTML文件...")
    
    # 保存到根目录
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 保存到cn目录
    with open('cn/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 保存到en目录
    with open('en/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("最终修复完成！文件：index.html, cn/index.html 和 en/index.html")

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

def generate_nav_menu(category_tree):
    """生成导航菜单"""
    nav_html = ''
    
    # 图标映射字典
    icon_map = {
        '实用工具': 'fa-wrench',
        'AI工具': 'fa-microphone',
        '跨境推广': 'fa-globe',
        '跨境资讯': 'fa-file-text-o',
        '社媒资源': 'fa-share',
        '全球网络': 'fa-cloud',
        '全球接码': 'fa-phone',
        '数字货币': 'fa-credit-card',
        '全球支付': 'fa-money',
        'Facebook': 'fa-thumbs-up',
        'Google': 'fa-search',
        '广告工具': 'fa-bullhorn',
        '全球APP下载': 'fa-download',
        '内容制作': 'fa-camera',
        '技术交流': 'fa-comment',
        '引流工具': 'fa-fire',
        '跨境电商': 'fa-shopping-cart',
        '跨境服务': 'fa-life-ring',
        '营销推广': 'fa-bullhorn',
        '独立站': 'fa-desktop',
        '广告投放': 'fa-fire',
        '社交媒体': 'fa-share',
        '内容创作': 'fa-camera',
        '数据分析': 'fa-bar-chart',
        '学习资源': 'fa-book',
        '其他工具': 'fa-cog'
    }
    
    # 遍历所有分类
    for group in category_tree.values():
        children = group['children']
        category_name = group['name']
        
        # 根据分类名称获取图标，如果没有则使用默认图标
        icon_class = icon_map.get(category_name, 'linecons-thumbs-up')
        
        if children:
            # 大类，生成嵌套菜单
            nav_html += f'''<li>
                <a>
                    <i class="{icon_class}"></i>
                    <span class="title">{category_name}</span>
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
                <a href="#{category_name}" class="smooth">
                    <i class="linecons-star"></i>
                    <span class="title">{category_name}</span>
                </a>
            </li>'''
    
    return nav_html

def get_favicon_url(url, favicon_mapping=None):
    """获取网站favicon URL，优先使用本地缓存"""
    if not url or url == '#':
        return 'assets/images/logos/default.png'
    
    # 如果已经是本地路径，直接返回
    if url.startswith('assets/'):
        return url
    
    # 提取域名
    domain = get_domain_from_url(url)
    if not domain:
        return 'assets/images/logos/default.png'
    
    # 优先使用本地缓存的favicon
    if favicon_mapping and domain in favicon_mapping:
        return favicon_mapping[domain]
    
    # 如果没有缓存，使用Google favicon服务
    return f'https://www.google.com/s2/favicons?domain={domain}&sz=64'

def generate_content(groups, category_map, favicon_mapping=None):
    """生成内容区域"""
    content_html = ''
    sites_data = {}
    
    for group in groups:
        # 检查是否为小类（有父类或者没有子分类且有网站）
        group_info = category_map[group['id']]
        
        # 如果是大类且没有网站，则跳过
        if group_info['is_parent'] and not group_info['sites']:
            continue
        
        # 生成内容
        group_name = group['name']
        group_sites = group['sites']
        total_sites = len(group_sites)
        
        # 存储网站数据到JavaScript对象
        sites_data[group_name] = []
        for site in group_sites:
            sites_data[group_name].append({
                'name': site.get('name', '未知网站'),
                'url': site.get('url', '#'),
                'description': site.get('description', ''),
                'icon': get_favicon_url(site.get('url', '#'), favicon_mapping)
            })
        
        # 添加分页控制按钮（如果有超过18个网站）
        pagination_controls = ''
        has_pagination = False
        if total_sites > 18:
            has_pagination = True
            pagination_controls = f'''<button class="btn btn-sm btn-default prev-page" data-category="{group_name}" disabled>
                    <i class="fa fa-chevron-left"></i>
                </button>
                <button class="btn btn-sm btn-default next-page" data-category="{group_name}">
                    <i class="fa fa-chevron-right"></i>
                </button>'''
        
        # 生成左侧翻页按钮HTML（无论是否有翻页按钮都生成容器）
        if has_pagination:
            left_pagination_html = f'<div class="pagination-left">{pagination_controls[:pagination_controls.find("</button>") + 9]}</div>'
            right_pagination_html = f'<div class="pagination-right">{pagination_controls[pagination_controls.find("</button>") + 9:]}</div>'
        else:
            left_pagination_html = '<div class="pagination-left"></div>'
            right_pagination_html = '<div class="pagination-right"></div>'
        
        content_html += f'''<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="{group_name}"></i>{group_name}</h4>
        <div class="row category-row" data-category="{group_name}" data-total="{total_sites}" data-pagination="{has_pagination}">
            {left_pagination_html}
            <div class="category-content">'''
        
        # 添加网站卡片 - 显示所有网站，通过JavaScript控制分页
        for i, site in enumerate(group_sites):
            site_name = site.get('name', '未知网站')
            site_url = site.get('url', '#')
            site_description = site.get('description', '')
            site_icon = get_favicon_url(site_url, favicon_mapping)
            
            content_html += f'''<div class="site-item" data-index="{i}">
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
            {right_pagination_html}
        </div>
        <br />
        <!--END {group_name} -->
        '''
    
    # 将sites_data转换为JavaScript对象字符串
    import json
    sites_data_json = json.dumps(sites_data, ensure_ascii=False)
    
    return content_html, sites_data_json

if __name__ == '__main__':
    final_fix()
