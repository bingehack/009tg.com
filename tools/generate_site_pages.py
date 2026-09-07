#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具详情页生成脚本 - 支持中英文双语

用途：
    为站点生成详情页，增加网站内容深度，有利于SEO和AdSense审核。

功能概述：
    1. 读取JSON数据
    2. 为每个站点生成详情页
    3. 详情页包含：工具信息、功能特点、适用场景、相关工具推荐
    4. 支持中英文双语
    5. 支持限制生成数量

使用方法：
    python tools/generate_site_pages.py
    python tools/generate_site_pages.py --limit 100
    python tools/generate_site_pages.py --lang en
    python tools/generate_site_pages.py --site-id 123  # 只生成指定站点

主要特性：
    - 生成完整的工具详情页
    - 支持中英文双语
    - 相关工具推荐（同分类）
    - 自动生成功能特点和适用场景
    - 支持限制生成数量
"""

import json
import os
import shutil
import argparse
from urllib.parse import urlparse

# 导入分类翻译
from generate_new_html import CATEGORY_TRANSLATION, translate_category

# ============================================================
# 分类功能特点模板（中英文）
# ============================================================
CATEGORY_FEATURES = {
    'AI常用工具': {
        'cn': ['智能问答与对话', '内容生成与创作', '多模态交互', 'API接口支持', '云端快速响应'],
        'en': ['Intelligent Q&A and dialogue', 'Content generation and creation', 'Multimodal interaction', 'API interface support', 'Fast cloud response']
    },
    'AI写作工具': {
        'cn': ['文章自动生成', '文案智能润色', '多文体支持', 'SEO优化建议', '批量内容创作'],
        'en': ['Automatic article generation', 'Smart copy polishing', 'Multi-style support', 'SEO optimization suggestions', 'Batch content creation']
    },
    'AI图像工具': {
        'cn': ['文字生成图片', '图像智能编辑', '多种艺术风格', '高清画质输出', '批量图片处理'],
        'en': ['Text-to-image generation', 'Intelligent image editing', 'Multiple art styles', 'HD quality output', 'Batch image processing']
    },
    'AI视频工具': {
        'cn': ['文本生成视频', '智能视频剪辑', '自动字幕生成', '特效一键添加', '多格式导出'],
        'en': ['Text-to-video generation', 'Intelligent video clipping', 'Automatic subtitle generation', 'One-click effects', 'Multi-format export']
    },
    'AI音频工具': {
        'cn': ['文字转语音', '语音克隆合成', '音频智能编辑', '音乐自动生成', '多语言支持'],
        'en': ['Text-to-speech', 'Voice cloning and synthesis', 'Intelligent audio editing', 'Automatic music generation', 'Multi-language support']
    },
    'AI办公工具': {
        'cn': ['智能文档处理', '数据分析可视化', '会议纪要自动生成', '任务智能管理', '团队协作支持'],
        'en': ['Intelligent document processing', 'Data analysis and visualization', 'Automatic meeting summaries', 'Smart task management', 'Team collaboration support']
    },
    'AI编程工具': {
        'cn': ['代码自动生成', '智能代码补全', 'Bug自动检测修复', '多语言支持', '代码审查建议'],
        'en': ['Automatic code generation', 'Smart code completion', 'Automatic bug detection and fixing', 'Multi-language support', 'Code review suggestions']
    },
    'AI设计工具': {
        'cn': ['智能排版布局', '配色方案推荐', '模板一键生成', 'UI/UX设计支持', '团队协作设计'],
        'en': ['Intelligent layout', 'Color scheme recommendations', 'One-click template generation', 'UI/UX design support', 'Collaborative design']
    },
    '常用工具': {
        'cn': ['在线即时使用', '无需安装下载', '操作简单直观', '多格式支持', '快速高效处理'],
        'en': ['Instant online use', 'No installation required', 'Simple and intuitive operation', 'Multi-format support', 'Fast and efficient processing']
    },
    '常用网址': {
        'cn': ['知名权威平台', '用户量大稳定', '功能完善全面', '安全可靠可信', '持续更新维护'],
        'en': ['Well-known authoritative platform', 'Large stable user base', 'Comprehensive features', 'Safe and reliable', 'Continuous updates and maintenance']
    },
}

DEFAULT_FEATURES = {
    'cn': ['功能强大实用', '操作简单便捷', '安全可靠稳定', '持续更新优化', '用户体验优秀'],
    'en': ['Powerful and practical features', 'Simple and convenient operation', 'Safe, reliable and stable', 'Continuous updates and optimization', 'Excellent user experience']
}

# 适用场景模板
CATEGORY_SCENARIOS = {
    'AI常用工具': {'cn': '日常办公、学习研究、内容创作、技术开发', 'en': 'Daily office work, learning and research, content creation, tech development'},
    'AI写作工具': {'cn': '自媒体运营、营销文案、学术写作、商务文档', 'en': 'Self-media operation, marketing copy, academic writing, business documents'},
    'AI图像工具': {'cn': '设计创作、营销素材、社交媒体、电商产品图', 'en': 'Design creation, marketing materials, social media, e-commerce product images'},
    'AI视频工具': {'cn': '短视频创作、营销视频、教育培训、产品演示', 'en': 'Short video creation, marketing videos, education and training, product demos'},
    'AI编程工具': {'cn': '软件开发、学习编程、技术研究、代码审查', 'en': 'Software development, learning to code, technical research, code review'},
    '常用工具': {'cn': '日常办公、文件处理、数据转换、学习工作', 'en': 'Daily office work, file processing, data conversion, study and work'},
}

DEFAULT_SCENARIOS = {'cn': '日常工作、学习研究、业务处理、个人使用', 'en': 'Daily work, learning and research, business processing, personal use'}


def get_features(category, lang='cn'):
    """获取分类功能特点"""
    if category in CATEGORY_FEATURES:
        return CATEGORY_FEATURES[category][lang]
    return DEFAULT_FEATURES[lang]


def get_scenarios(category, lang='cn'):
    """获取适用场景"""
    if category in CATEGORY_SCENARIOS:
        return CATEGORY_SCENARIOS[category][lang]
    return DEFAULT_SCENARIOS[lang]


def get_domain(url):
    """提取域名"""
    try:
        return urlparse(url).netloc.lower()
    except:
        return ''


def generate_site_page(site, category, related_sites, favicon_mapping, lang='cn', asset_prefix='../../'):
    """生成单个站点详情页"""
    site_name = site.get('name', '未知网站')
    site_url = site.get('url', '#')
    if lang == 'en':
        site_description = site.get('description_en') or site.get('description', '')
    else:
        site_description = site.get('description', '')
    site_id = site.get('id', 0)
    domain = get_domain(site_url)

    # favicon
    site_icon = f'{asset_prefix}assets/images/logos/default.png'
    if domain in favicon_mapping:
        site_icon = asset_prefix + favicon_mapping[domain]

    # 功能特点
    features = get_features(category, lang)
    features_html = ''.join([f'<li>{f}</li>' for f in features])

    # 适用场景
    scenarios = get_scenarios(category, lang)

    # 相关工具
    related_html = ''
    for rel in related_sites[:6]:
        rel_name = rel.get('name', '')
        rel_url = rel.get('url', '#')
        rel_id = rel.get('id', 0)
        rel_domain = get_domain(rel_url)
        rel_icon = f'{asset_prefix}assets/images/logos/default.png'
        if rel_domain in favicon_mapping:
            rel_icon = asset_prefix + favicon_mapping[rel_domain]
        related_html += f'''
                    <div class="col-sm-4">
                        <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('{asset_prefix}redirect.html?url={rel_url}&name={rel_name}', '_blank')" style="cursor: pointer; margin-bottom: 15px;">
                            <div class="xe-comment-entry">
                                <a class="xe-user-img">
                                    <img src="{rel_icon}" class="img-circle" width="40" alt="{rel_name}">
                                </a>
                                <div class="xe-comment">
                                    <a href="#" class="xe-user-name overflowClip_1">
                                        <strong>{rel_name}</strong>
                                    </a>
                                    <p class="overflowClip_2">{rel.get("description", "")[:50]}</p>
                                </div>
                            </div>
                        </div>
                    </div>'''

    # 页面文本
    if lang == 'cn':
        html_lang = 'zh'
        title = f'{site_name} - 009tg下海导航'
        meta_keywords = f'{site_name},{category},网址导航,工具推荐'
        meta_desc = f'{site_name}详细介绍：{site_description[:100]}。{category}分类下的实用工具，009tg下海导航为您推荐。'
        visit_btn = '访问网站'
        features_title = '功能特点'
        scenarios_title = '适用场景'
        related_title = '相关工具推荐'
        back_text = '返回导航'
        category_text = translate_category(category, 'cn')
        about_text = '关于本站'
    else:
        html_lang = 'en'
        title = f'{site_name} - 009tg Navigation'
        meta_keywords = f'{site_name},{translate_category(category, "en")},url directory,tool recommendation'
        meta_desc = f'{site_name} details: {site_description[:100]}. A practical tool in the {translate_category(category, "en")} category, recommended by 009tg Navigation.'
        visit_btn = 'Visit Website'
        features_title = 'Features'
        scenarios_title = 'Use Cases'
        related_title = 'Related Tools'
        back_text = 'Back to Directory'
        category_text = translate_category(category, 'en')
        about_text = 'About Us'

    # 语言切换
    if lang == 'cn':
        lang_switcher = f'''
                    <li class="dropdown hover-line language-switcher">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="{asset_prefix}assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                        </a>
                        <ul class="dropdown-menu languages">
                            <li><a href="../../en/sites/{site_id}.html"><img src="{asset_prefix}assets/images/flags/flag-us.png" alt="flag-us" /> English</a></li>
                            <li class="active"><a href="../../cn/sites/{site_id}.html"><img src="{asset_prefix}assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese</a></li>
                        </ul>
                    </li>'''
    else:
        lang_switcher = f'''
                    <li class="dropdown hover-line language-switcher">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="{asset_prefix}assets/images/flags/flag-us.png" alt="flag-us" /> English
                        </a>
                        <ul class="dropdown-menu languages">
                            <li class="active"><a href="../../en/sites/{site_id}.html"><img src="{asset_prefix}assets/images/flags/flag-us.png" alt="flag-us" /> English</a></li>
                            <li><a href="../../cn/sites/{site_id}.html"><img src="{asset_prefix}assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese</a></li>
                        </ul>
                    </li>'''

    html = f'''<!DOCTYPE html>
<html lang="{html_lang}">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="author" content="Invisible man" />
    <title>{title}</title>
    <meta name="theme-color" content="#f9f9f9"/>
    <meta name="keywords" content="{meta_keywords}"/>
    <meta name="description" content="{meta_desc}"/>
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
</head>

<body class="page-body">
    <div class="page-container">
        <div class="sidebar-menu toggle-others fixed">
            <div class="sidebar-menu-inner">
                <header class="logo-env">
                    <div class="logo">
                        <a href="../index.html" class="logo-expanded">
                            <img src="{asset_prefix}assets/images/logo@2x.png" width="100%" alt="" />
                        </a>
                        <a href="../index.html" class="logo-collapsed">
                            <img src="{asset_prefix}assets/images/logo-collapsed@2x.png" width="40" alt="" />
                        </a>
                    </div>
                </header>
                <ul id="main-menu" class="main-menu">
                    <li>
                        <a href="../index.html">
                            <i class="linecons-star"></i>
                            <span class="title">{back_text}</span>
                        </a>
                    </li>
                    <li>
                        <a href="../about.html">
                            <i class="linecons-heart"></i>
                            <span class="title">{about_text}</span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        <div class="main-content">
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

            <!-- 工具信息区 -->
            <div class="row">
                <div class="col-md-12">
                    <div class="panel panel-default">
                        <div class="panel-body">
                            <div class="row">
                                <div class="col-sm-2 text-center">
                                    <img src="{site_icon}" class="img-circle" width="80" alt="{site_name}" style="margin-bottom: 15px;" />
                                </div>
                                <div class="col-sm-7">
                                    <h2 style="margin-top: 0;">{site_name}</h2>
                                    <p><span class="label label-primary">{category_text}</span></p>
                                    <p style="font-size: 15px; line-height: 1.8; margin-top: 10px;">{site_description}</p>
                                </div>
                                <div class="col-sm-3 text-center" style="padding-top: 20px;">
                                    <a href="{asset_prefix}redirect.html?url={site_url}&name={site_name}" target="_blank" class="btn btn-primary btn-lg" style="width: 100%;">
                                        <i class="fa-external-link"></i> {visit_btn}
                                    </a>
                                    <p style="margin-top: 10px; color: #999; font-size: 12px;">{domain}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 功能特点 -->
            <div class="row">
                <div class="col-md-6">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title"><i class="fa-check-circle" style="margin-right: 8px;"></i>{features_title}</h4>
                        </div>
                        <div class="panel-body">
                            <ul class="list-group">
                                {features_html}
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title"><i class="fa-users" style="margin-right: 8px;"></i>{scenarios_title}</h4>
                        </div>
                        <div class="panel-body">
                            <p style="font-size: 15px; line-height: 1.8;">{scenarios}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 相关工具推荐 -->
            <div class="row">
                <div class="col-md-12">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title"><i class="fa-thumbs-up" style="margin-right: 8px;"></i>{related_title}</h4>
                        </div>
                        <div class="panel-body">
                            <div class="row">
                                {related_html}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 底部 -->
            <footer class="main-footer sticky footer-type-1">
                <div class="footer-inner">
                    <div class="footer-text">
                        &copy; 2017 - 2026
                        <a href="../index.html"><strong>009tg下海导航</strong></a> design by <a href="https://invisibleman.dpdns.org/" target="_blank"><strong>Invisible Man</strong></a>
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
</body>
</html>
'''
    return html


def main():
    parser = argparse.ArgumentParser(description='生成工具详情页（支持中英文）')
    parser.add_argument('--limit', type=int, default=100, help='生成前N个站点的详情页（默认100）')
    parser.add_argument('--lang', choices=['cn', 'en', 'all'], default='all', help='生成语言版本（默认all）')
    parser.add_argument('--site-id', type=int, help='只生成指定ID的站点详情页')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    print("=" * 60)
    print("生成工具详情页（中英文双语）")
    print("=" * 60)

    # 读取数据
    print("\n读取JSON数据...")
    json_path = os.path.join(project_root, '完整版导航.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("读取favicon映射...")
    favicon_mapping_path = os.path.join(project_root, 'favicon_mapping.json')
    with open(favicon_mapping_path, 'r', encoding='utf-8') as f:
        favicon_mapping = json.load(f)

    # 收集所有站点（带分类信息）
    all_sites = []
    for group in data.get('groups', []):
        category = group.get('name', '')
        for site in group.get('sites', []):
            site['_category'] = category
            all_sites.append(site)

    # 按分类建立相关工具索引
    category_sites = {}
    for site in all_sites:
        cat = site['_category']
        if cat not in category_sites:
            category_sites[cat] = []
        category_sites[cat].append(site)

    # 筛选要生成的站点
    if args.site_id:
        target_sites = [s for s in all_sites if s.get('id') == args.site_id]
        if not target_sites:
            print(f"未找到ID为{args.site_id}的站点")
            return
    else:
        target_sites = all_sites[:args.limit]

    print(f"将生成 {len(target_sites)} 个站点的详情页")

    # 生成
    generated = {'cn': 0, 'en': 0}

    for lang in ['cn', 'en']:
        if args.lang != 'all' and args.lang != lang:
            continue

        output_dir = os.path.join(project_root, lang, 'sites')
        os.makedirs(output_dir, exist_ok=True)

        for site in target_sites:
            site_id = site.get('id', 0)
            category = site['_category']

            # 相关工具（同分类，排除自己）
            related = [s for s in category_sites.get(category, []) if s.get('id') != site_id]

            # 生成页面
            html = generate_site_page(site, category, related, favicon_mapping, lang)

            output_path = os.path.join(output_dir, f'{site_id}.html')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            generated[lang] += 1

        print(f"  {lang}: 生成 {generated[lang]} 个详情页 -> {lang}/sites/")

    print()
    print("=" * 60)
    print("生成完成！")
    print(f"  中文: cn/sites/ ({generated['cn']} 个页面)")
    print(f"  英文: en/sites/ ({generated['en']} 个页面)")
    print("=" * 60)


if __name__ == '__main__':
    main()
