#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章页面生成脚本
生成文章列表页和文章详情页（中英文双语）

用途：
    读取 data/articles.json，生成文章列表页和详情页
    列表页：cn/articles.html, en/articles.html
    详情页：cn/article/{id}.html, en/article/{id}.html

使用方法：
    python generate_articles.py
"""

import json
import os
import re
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 页面文本翻译
I18N = {
    'cn': {
        'articles': '文章资讯',
        'articles_desc': '跨境电商、AI工具、网络资源等领域的深度文章和实用指南',
        'home': '首页',
        'read_more': '阅读全文',
        'published': '发布于',
        'author': '作者',
        'views': '阅读',
        'tags': '标签',
        'category': '分类',
        'back_to_list': '返回文章列表',
        'no_articles': '暂无文章',
        'page': '第',
        'page_of': '页，共',
        'pages': '页',
        'prev': '上一页',
        'next': '下一页',
        'related_articles': '相关文章',
        'hot_articles': '热门文章',
        'all_categories': '全部分类',
    },
    'en': {
        'articles': 'Articles',
        'articles_desc': 'In-depth articles and practical guides on cross-border e-commerce, AI tools, web resources and more',
        'home': 'Home',
        'read_more': 'Read More',
        'published': 'Published',
        'author': 'Author',
        'views': 'Views',
        'tags': 'Tags',
        'category': 'Category',
        'back_to_list': 'Back to Article List',
        'no_articles': 'No articles yet',
        'page': 'Page',
        'page_of': 'of',
        'pages': '',
        'prev': 'Previous',
        'next': 'Next',
        'related_articles': 'Related Articles',
        'hot_articles': 'Hot Articles',
        'all_categories': 'All Categories',
    }
}

ITEMS_PER_PAGE = 10


def load_articles():
    """加载文章数据"""
    path = os.path.join(PROJECT_ROOT, 'data', 'articles.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [a for a in data.get('articles', []) if a.get('isPublic', True)]


def get_categories(articles, lang='cn'):
    """获取文章分类列表"""
    cats = []
    seen = set()
    for a in articles:
        cat = a.get('category' if lang == 'cn' else 'category_en', '未分类')
        if cat not in seen:
            seen.add(cat)
            cats.append(cat)
    return cats


def generate_dark_mode_css():
    """生成深色模式CSS"""
    return '''
    <style>
        :root {
            --bg-main: #f4f4f4;
            --bg-content: #ffffff;
            --bg-card: #ffffff;
            --bg-card-hover: #f8f9fa;
            --bg-navbar: #ffffff;
            --text-primary: #373e4a;
            --text-secondary: #6c757d;
            --text-muted: #979898;
            --border-color: #e4e6e9;
            --link-color: #337ab7;
            --link-hover: #23527c;
        }
        [data-theme="dark"] {
            --bg-main: #1a1d23;
            --bg-content: #22262e;
            --bg-card: #2a2f38;
            --bg-card-hover: #333945;
            --bg-navbar: #22262e;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --text-muted: #707070;
            --border-color: #3a3f48;
            --link-color: #5dade2;
            --link-hover: #85c1e9;
        }
        [data-theme="dark"] body { background-color: var(--bg-main) !important; color: var(--text-primary) !important; }
        [data-theme="dark"] .main-content { background-color: var(--bg-content) !important; }
        [data-theme="dark"] .navbar.user-info-navbar { background-color: var(--bg-navbar) !important; border-bottom-color: var(--border-color) !important; }
        [data-theme="dark"] .user-info-menu a { color: var(--text-primary) !important; }
        [data-theme="dark"] .user-info-menu a:hover { color: var(--link-color) !important; }
        [data-theme="dark"] .panel { background-color: var(--bg-card) !important; border-color: var(--border-color) !important; }
        [data-theme="dark"] .panel-heading { background-color: var(--bg-card) !important; border-bottom-color: var(--border-color) !important; }
        [data-theme="dark"] .panel-title, [data-theme="dark"] .panel h4 { color: var(--text-primary) !important; }
        [data-theme="dark"] .panel-body { color: var(--text-secondary) !important; }
        [data-theme="dark"] .panel-body p, [data-theme="dark"] .panel-body li { color: var(--text-secondary) !important; }
        [data-theme="dark"] .panel-body a { color: var(--link-color) !important; }
        [data-theme="dark"] .panel-body h1, [data-theme="dark"] .panel-body h2, [data-theme="dark"] .panel-body h3 { color: var(--text-primary) !important; }
        [data-theme="dark"] .text-gray, [data-theme="dark"] .text-muted { color: var(--text-muted) !important; }
        [data-theme="dark"] .breadcrumb { background-color: var(--bg-card) !important; }
        [data-theme="dark"] .breadcrumb a { color: var(--link-color) !important; }
        [data-theme="dark"] .main-footer { background-color: #16181d !important; color: var(--text-secondary) !important; }
        [data-theme="dark"] .main-footer a { color: var(--link-color) !important; }
        [data-theme="dark"] .article-card { background-color: var(--bg-card) !important; border-color: var(--border-color) !important; }
        [data-theme="dark"] .article-card:hover { background-color: var(--bg-card-hover) !important; }
        [data-theme="dark"] .article-title a { color: var(--text-primary) !important; }
        [data-theme="dark"] .article-title a:hover { color: var(--link-color) !important; }
        [data-theme="dark"] .article-meta { color: var(--text-muted) !important; }
        [data-theme="dark"] .article-summary { color: var(--text-secondary) !important; }
        [data-theme="dark"] .tag-badge { background-color: var(--bg-card-hover) !important; color: var(--text-secondary) !important; border-color: var(--border-color) !important; }
        [data-theme="dark"] .category-filter a { color: var(--text-secondary) !important; }
        [data-theme="dark"] .category-filter a.active, [data-theme="dark"] .category-filter a:hover { color: var(--link-color) !important; }
        [data-theme="dark"] .pagination .btn { background-color: var(--bg-card) !important; border-color: var(--border-color) !important; color: var(--text-primary) !important; }
        [data-theme="dark"] .article-content h2 { color: var(--text-primary) !important; border-bottom-color: var(--border-color) !important; }
        [data-theme="dark"] .article-content h3 { color: var(--text-primary) !important; }
        [data-theme="dark"] .article-content blockquote { background-color: var(--bg-card-hover) !important; border-left-color: var(--link-color) !important; }
        [data-theme="dark"] .article-content code { background-color: var(--bg-card-hover) !important; color: var(--text-primary) !important; }
        [data-theme="dark"] .article-content pre { background-color: var(--bg-card-hover) !important; }
        [data-theme="dark"] .horizontal-menu { background-color: #16181d !important; }
        [data-theme="dark"] .navbar-brand .logo img { filter: brightness(1.5); }
        .theme-toggle-btn { cursor: pointer; padding: 8px 12px; border-radius: 4px; transition: all 0.3s ease; background: transparent; border: none; font-size: 16px; color: inherit; }
        .theme-toggle-btn:hover { background-color: rgba(0,0,0,0.05); }
        [data-theme="dark"] .theme-toggle-btn:hover { background-color: rgba(255,255,255,0.1); }

        /* 文章页面自定义样式 */
        .article-card { border: 1px solid #e4e6e9; border-radius: 6px; padding: 20px; margin-bottom: 20px; transition: all 0.3s ease; background: #fff; }
        .article-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); transform: translateY(-2px); }
        .article-title { font-size: 20px; font-weight: 600; margin-bottom: 10px; }
        .article-title a { color: #373e4a; text-decoration: none; }
        .article-title a:hover { color: #337ab7; }
        .article-meta { font-size: 13px; color: #979898; margin-bottom: 12px; }
        .article-meta span { margin-right: 15px; }
        .article-summary { font-size: 14px; color: #6c757d; line-height: 1.7; margin-bottom: 12px; }
        .article-tags { margin-top: 10px; }
        .tag-badge { display: inline-block; padding: 3px 10px; font-size: 12px; background: #f5f5f5; border: 1px solid #e4e6e9; border-radius: 12px; margin-right: 8px; color: #6c757d; text-decoration: none; }
        .tag-badge:hover { background: #337ab7; color: #fff; border-color: #337ab7; }
        .category-filter { margin-bottom: 20px; padding: 15px; background: #f9f9f9; border-radius: 6px; }
        .category-filter a { display: inline-block; padding: 5px 15px; margin-right: 10px; margin-bottom: 5px; color: #6c757d; text-decoration: none; border-radius: 4px; font-size: 13px; }
        .category-filter a.active, .category-filter a:hover { background: #337ab7; color: #fff; }
        .article-content { font-size: 15px; line-height: 1.9; color: #373e4a; }
        .article-content h2 { font-size: 22px; margin-top: 30px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #f0f0f0; color: #373e4a; }
        .article-content h3 { font-size: 18px; margin-top: 25px; margin-bottom: 12px; color: #373e4a; }
        .article-content p { margin-bottom: 15px; }
        .article-content ul, .article-content ol { margin-bottom: 15px; padding-left: 25px; }
        .article-content li { margin-bottom: 8px; line-height: 1.8; }
        .article-content a { color: #337ab7; text-decoration: none; }
        .article-content a:hover { text-decoration: underline; }
        .article-content blockquote { border-left: 4px solid #337ab7; padding: 10px 20px; margin: 15px 0; background: #f9f9f9; color: #6c757d; }
        .article-content code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 13px; }
        .article-content pre { background: #f5f5f5; padding: 15px; border-radius: 6px; overflow-x: auto; }
        .article-content img { max-width: 100%; border-radius: 6px; margin: 15px 0; }
        .article-header { margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #f0f0f0; }
        .article-header h1 { font-size: 28px; margin-bottom: 15px; line-height: 1.4; }
        .sidebar-widget { background: #f9f9f9; border-radius: 6px; padding: 20px; margin-bottom: 20px; }
        .sidebar-widget h4 { font-size: 16px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #337ab7; }
        .sidebar-widget ul { list-style: none; padding: 0; margin: 0; }
        .sidebar-widget li { margin-bottom: 10px; }
        .sidebar-widget li a { color: #6c757d; text-decoration: none; font-size: 13px; display: block; line-height: 1.5; }
        .sidebar-widget li a:hover { color: #337ab7; }
    </style>
'''


def generate_dark_mode_js():
    """生成深色模式JS"""
    return '''
    <script>
        function initTheme() {
            var savedTheme = localStorage.getItem('theme');
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
                updateThemeIcon(savedTheme);
            } else {
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    document.documentElement.setAttribute('data-theme', 'dark');
                    updateThemeIcon('dark');
                }
            }
        }
        function toggleTheme() {
            var currentTheme = document.documentElement.getAttribute('data-theme');
            var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        }
        function updateThemeIcon(theme) {
            var icon = document.getElementById('theme-icon');
            if (icon) {
                icon.className = theme === 'dark' ? 'fa-sun-o' : 'fa-moon-o';
                icon.parentElement.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
            }
        }
        initTheme();
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                if (!localStorage.getItem('theme')) {
                    if (e.matches) {
                        document.documentElement.setAttribute('data-theme', 'dark');
                        updateThemeIcon('dark');
                    } else {
                        document.documentElement.removeAttribute('data-theme');
                        updateThemeIcon('light');
                    }
                }
            });
        }
    </script>
'''


def generate_page_wrapper(content, lang='cn', page_title='', asset_prefix='../'):
    """生成页面外壳（导航栏+页脚）"""
    t = I18N[lang]
    html_lang = 'zh' if lang == 'cn' else 'en'

    # 语言切换
    if lang == 'cn':
        lang_switcher = '''
                    <li class="dropdown hover-line language-switcher">
                        <a href="articles.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="''' + asset_prefix + '''assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                        </a>
                        <ul class="dropdown-menu languages">
                            <li><a href="../en/articles.html"><img src="''' + asset_prefix + '''assets/images/flags/flag-us.png" alt="flag-us" /> English</a></li>
                            <li class="active"><a href="../cn/articles.html"><img src="''' + asset_prefix + '''assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese</a></li>
                        </ul>
                    </li>'''
    else:
        lang_switcher = '''
                    <li class="dropdown hover-line language-switcher">
                        <a href="articles.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="''' + asset_prefix + '''assets/images/flags/flag-us.png" alt="flag-us" /> English
                        </a>
                        <ul class="dropdown-menu languages">
                            <li class="active"><a href="../en/articles.html"><img src="''' + asset_prefix + '''assets/images/flags/flag-us.png" alt="flag-us" /> English</a></li>
                            <li><a href="../cn/articles.html"><img src="''' + asset_prefix + '''assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese</a></li>
                        </ul>
                    </li>'''

    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="author" content="Invisible man" />
    <title>{page_title} - 009tg下海导航</title>
    <meta name="theme-color" content="#f9f9f9"/>
    <meta name="keywords" content="009tg下海导航,文章资讯,跨境电商,AI工具,工具推荐"/>
    <meta name="description" content="{t['articles_desc']}"/>
    <link rel="shortcut icon" href="{asset_prefix}assets/images/favicon.png">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5301924424938934"
         crossorigin="anonymous"></script>
    <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Arimo:400,700,400italic">
    <link rel="stylesheet" href="{asset_prefix}assets/css/fonts/linecons/css/linecons.css">
    <link rel="stylesheet" href="{asset_prefix}assets/css/fonts/fontawesome/css/font-awesome.min.css">
    <link rel="stylesheet" href="{asset_prefix}assets/css/bootstrap.css">
    <link rel="stylesheet" href="{asset_prefix}assets/css/xenon-core.css">
    <link rel="stylesheet" href="{asset_prefix}assets/css/xenon-components.css">
    <link rel="stylesheet" href="{asset_prefix}assets/css/xenon-skins.css">
    <link rel="stylesheet" href="{asset_prefix}assets/css/nav.css">
    <script src="{asset_prefix}assets/js/jquery-1.11.1.min.js"></script>
    {generate_dark_mode_css()}
</head>
<body class="page-body boxed-container">
    <nav class="navbar horizontal-menu navbar-fixed-top">
        <div class="navbar-inner">
            <div class="navbar-brand">
                <a href="{asset_prefix}index.html" class="logo">
                    <img src="{asset_prefix}assets/images/logo_dark_light@2x.png" width="100%" alt="" class="hidden-xs">
                    <img src="{asset_prefix}assets/images/logo@2x.png" width="100%" alt="" class="visible-xs">
                </a>
            </div>
            <ul class="user-info-menu right-links list-inline list-unstyled" style="float: right; margin-top: 15px; margin-right: 20px;">
                <li>
                    <button class="theme-toggle-btn" onclick="toggleTheme()" title="切换深色/浅色模式">
                        <i class="fa-moon-o" id="theme-icon"></i>
                    </button>
                </li>
            </ul>
            <div class="navbar-mobile-clear"></div>
        </div>
    </nav>
    <div class="page-container">
        <div class="main-content" style="">
            <nav class="navbar user-info-navbar" role="navigation">
                <ul class="user-info-menu left-links list-inline list-unstyled">
                    <li class="hidden-sm hidden-xs">
                        <a href="#" data-toggle="sidebar">
                            <i class="fa-bars"></i>
                        </a>
                    </li>
                    {lang_switcher}
                </ul>
            </nav>
            {content}
            <footer class="main-footer sticky footer-type-1 fixed">
                <div class="footer-inner">
                    <div class="footer-text">
                        &copy; 2017 - 2026
                        <a href="{asset_prefix}index.html"><strong>009tg下海导航</strong></a> design by <a href="https://invisibleman.dpdns.org/" target="_blank"><strong>Invisible Man</strong></a>
                    </div>
                    <div class="go-up">
                        <a href="#" rel="go-top"><i class="fa-angle-up"></i></a>
                    </div>
                </div>
            </footer>
        </div>
    </div>
    <script src="{asset_prefix}assets/js/bootstrap.min.js"></script>
    <script src="{asset_prefix}assets/js/TweenMax.min.js"></script>
    <script src="{asset_prefix}assets/js/resizeable.js"></script>
    <script src="{asset_prefix}assets/js/joinable.js"></script>
    <script src="{asset_prefix}assets/js/xenon-api.js"></script>
    <script src="{asset_prefix}assets/js/xenon-toggles.js"></script>
    <script src="{asset_prefix}assets/js/xenon-custom.js"></script>
    {generate_dark_mode_js()}
</body>
</html>'''


def generate_article_list_page(articles, lang='cn', page=1, category=None):
    """生成文章列表页"""
    t = I18N[lang]
    asset_prefix = '../'

    # 按分类筛选
    if category and category != t['all_categories']:
        filtered = [a for a in articles if (a.get('category' if lang == 'cn' else 'category_en') == category)]
    else:
        filtered = articles

    # 按发布时间排序
    filtered.sort(key=lambda x: x.get('publishDate', ''), reverse=True)

    # 分页
    total_pages = max(1, (len(filtered) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    page = max(1, min(page, total_pages))
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_articles = filtered[start:end]

    # 分类筛选
    categories = get_categories(articles, lang)
    category_filter_html = f'<div class="category-filter"><strong>{t["category"]}：</strong>'
    active_class = 'active' if not category or category == t['all_categories'] else ''
    category_filter_html += f'<a href="articles.html" class="{active_class}">{t["all_categories"]}</a>'
    for cat in categories:
        active_class = 'active' if category == cat else ''
        category_filter_html += f'<a href="articles.html?category={cat}" class="{active_class}">{cat}</a>'
    category_filter_html += '</div>'

    # 文章列表
    articles_html = ''
    if not page_articles:
        articles_html = f'<div class="text-center" style="padding: 50px 0; color: #999;">{t["no_articles"]}</div>'
    else:
        for article in page_articles:
            title = article.get('title' if lang == 'cn' else 'title_en', '')
            summary = article.get('summary' if lang == 'cn' else 'summary_en', '')
            cat = article.get('category' if lang == 'cn' else 'category_en', '')
            tags = article.get('tags' if lang == 'cn' else 'tags_en', [])
            tags_html = ''.join([f'<span class="tag-badge">{tag}</span>' for tag in tags])

            articles_html += f'''
            <div class="article-card">
                <div class="article-title"><a href="article/{article["id"]}.html">{title}</a></div>
                <div class="article-meta">
                    <span><i class="fa-calendar"></i> {t["published"]} {article.get("publishDate", "")}</span>
                    <span><i class="fa-user"></i> {article.get("author", "")}</span>
                    <span><i class="fa-folder"></i> {cat}</span>
                    <span><i class="fa-eye"></i> {article.get("views", 0)} {t["views"]}</span>
                </div>
                <div class="article-summary">{summary}</div>
                <div class="article-tags">{tags_html}</div>
                <div style="margin-top: 12px;">
                    <a href="article/{article["id"]}.html" class="btn btn-primary btn-sm">{t["read_more"]} <i class="fa-angle-right"></i></a>
                </div>
            </div>'''

    # 分页
    pagination_html = ''
    if total_pages > 1:
        pagination_html = '<div style="text-align: center; margin-top: 30px;">'
        if page > 1:
            pagination_html += f'<a href="articles.html?page={page-1}" class="btn btn-default" style="margin: 0 5px;"><i class="fa-angle-left"></i> {t["prev"]}</a>'
        pagination_html += f'<span style="margin: 0 15px; color: #666;">{t["page"]} {page} {t["page_of"]} {total_pages} {t["pages"]}</span>'
        if page < total_pages:
            pagination_html += f'<a href="articles.html?page={page+1}" class="btn btn-default" style="margin: 0 5px;">{t["next"]} <i class="fa-angle-right"></i></a>'
        pagination_html += '</div>'

    # 侧边栏（热门文章）
    hot_articles = sorted(articles, key=lambda x: x.get('views', 0), reverse=True)[:5]
    hot_html = '<div class="sidebar-widget"><h4><i class="fa-fire"></i> ' + t['hot_articles'] + '</h4><ul>'
    for a in hot_articles:
        title = a.get('title' if lang == 'cn' else 'title_en', '')
        hot_html += f'<li><a href="article/{a["id"]}.html">{title}</a></li>'
    hot_html += '</ul></div>'

    content = f'''
    <div class="row">
        <div class="col-md-9">
            <div class="breadcrumb">
                <a href="{asset_prefix}index.html">{t["home"]}</a>
                <span> / </span>
                <span>{t["articles"]}</span>
            </div>
            <h2 style="margin-top: 0; margin-bottom: 20px;">
                <i class="fa-newspaper-o"></i> {t["articles"]}
                <small style="color: #999; font-size: 14px;">{t["articles_desc"]}</small>
            </h2>
            {category_filter_html}
            {articles_html}
            {pagination_html}
        </div>
        <div class="col-md-3">
            {hot_html}
        </div>
    </div>
    '''

    return generate_page_wrapper(content, lang, t['articles'], asset_prefix)


def generate_article_detail_page(article, all_articles, lang='cn'):
    """生成文章详情页"""
    t = I18N[lang]
    asset_prefix = '../../'

    title = article.get('title' if lang == 'cn' else 'title_en', '')
    content = article.get('content' if lang == 'cn' else 'content_en', '')
    summary = article.get('summary' if lang == 'cn' else 'summary_en', '')
    cat = article.get('category' if lang == 'cn' else 'category_en', '')
    tags = article.get('tags' if lang == 'cn' else 'tags_en', [])
    tags_html = ''.join([f'<span class="tag-badge">{tag}</span>' for tag in tags])

    # 相关文章（同分类）
    related = [a for a in all_articles if a.get('category' if lang == 'cn' else 'category_en') == cat and a['id'] != article['id']][:5]
    related_html = ''
    if related:
        related_html = '<div class="sidebar-widget"><h4><i class="fa-link"></i> ' + t['related_articles'] + '</h4><ul>'
        for a in related:
            r_title = a.get('title' if lang == 'cn' else 'title_en', '')
            related_html += f'<li><a href="{a["id"]}.html">{r_title}</a></li>'
        related_html += '</ul></div>'

    # 热门文章
    hot_articles = sorted(all_articles, key=lambda x: x.get('views', 0), reverse=True)[:5]
    hot_html = '<div class="sidebar-widget"><h4><i class="fa-fire"></i> ' + t['hot_articles'] + '</h4><ul>'
    for a in hot_articles:
        h_title = a.get('title' if lang == 'cn' else 'title_en', '')
        hot_html += f'<li><a href="{a["id"]}.html">{h_title}</a></li>'
    hot_html += '</ul></div>'

    page_content = f'''
    <div class="row">
        <div class="col-md-9">
            <div class="breadcrumb">
                <a href="{asset_prefix}index.html">{t["home"]}</a>
                <span> / </span>
                <a href="../articles.html">{t["articles"]}</a>
                <span> / </span>
                <span>{title[:30]}{"..." if len(title) > 30 else ""}</span>
            </div>
            <div class="panel panel-default">
                <div class="panel-body">
                    <div class="article-header">
                        <h1>{title}</h1>
                        <div class="article-meta">
                            <span><i class="fa-calendar"></i> {t["published"]} {article.get("publishDate", "")}</span>
                            <span><i class="fa-user"></i> {article.get("author", "")}</span>
                            <span><i class="fa-folder"></i> {cat}</span>
                            <span><i class="fa-eye"></i> {article.get("views", 0)} {t["views"]}</span>
                        </div>
                        <div class="article-tags" style="margin-top: 10px;">{tags_html}</div>
                    </div>
                    <div class="article-content">
                        {content}
                    </div>
                    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #f0f0f0;">
                        <a href="../articles.html" class="btn btn-default"><i class="fa-angle-left"></i> {t["back_to_list"]}</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            {related_html}
            {hot_html}
        </div>
    </div>
    '''

    return generate_page_wrapper(page_content, lang, title, asset_prefix)


def main():
    print("=" * 60)
    print("生成文章页面（中英文双语）")
    print("=" * 60)

    articles = load_articles()
    print(f"\n加载文章: {len(articles)}篇")

    for lang in ['cn', 'en']:
        print(f"\n--- {lang.upper()} ---")

        # 生成文章列表页
        list_html = generate_article_list_page(articles, lang)
        list_path = os.path.join(PROJECT_ROOT, lang, 'articles.html')
        with open(list_path, 'w', encoding='utf-8') as f:
            f.write(list_html)
        print(f"  列表页: {lang}/articles.html ({len(list_html)} bytes)")

        # 生成文章详情页
        article_dir = os.path.join(PROJECT_ROOT, lang, 'article')
        os.makedirs(article_dir, exist_ok=True)

        for article in articles:
            detail_html = generate_article_detail_page(article, articles, lang)
            detail_path = os.path.join(article_dir, f'{article["id"]}.html')
            with open(detail_path, 'w', encoding='utf-8') as f:
                f.write(detail_html)
            print(f"  详情页: {lang}/article/{article['id']}.html ({len(detail_html)} bytes)")

    print("\n" + "=" * 60)
    print(f"生成完成！共 {len(articles)} 篇文章，{len(articles)*2 + 2} 个页面")
    print("=" * 60)


if __name__ == '__main__':
    main()
