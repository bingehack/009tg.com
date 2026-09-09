#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成站点详情页（中英文）
每个站点一个详情页，包含：
- 站点名称、logo、URL
- 个性化介绍（优先用meta description，其次用已有description）
- 关键词标签
- 所属分类
- 相关站点推荐
- 深色模式支持
"""

import json
import os
import hashlib
from urllib.parse import urlparse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_domain(url):
    """提取域名"""
    try:
        return urlparse(url).netloc.lower()
    except:
        return ''

def get_favicon_path(site, favicon_mapping, asset_prefix='../../'):
    """获取站点favicon路径"""
    url = site.get('url', '')
    domain = get_domain(url)
    icon = site.get('icon', '')
    
    if domain and domain in favicon_mapping:
        path = favicon_mapping[domain]
        if path.startswith('assets/'):
            return asset_prefix + path
        return path
    
    if icon:
        if icon.startswith('assets/'):
            return asset_prefix + icon
        return icon
    
    return asset_prefix + 'assets/images/logos/default.png'

def generate_site_detail_page(site, category, related_sites, favicon_mapping, meta_data, lang='cn'):
    """生成单个站点详情页"""
    site_id = site.get('id', 0)
    name = site.get('name', '')
    url = site.get('url', '')
    domain = get_domain(url)
    description = site.get('description', '')
    description_en = site.get('description_en', '')
    created_at = site.get('created_at', '')
    
    # 获取meta信息
    meta = meta_data.get(domain, {}) if domain else {}
    meta_title = meta.get('title', '')
    meta_desc = meta.get('description', '')
    meta_keywords = meta.get('keywords', '')
    meta_status = meta.get('status', '')
    
    # 个性化介绍：优先用meta description，其次用已有description
    if lang == 'cn':
        if meta_desc and len(meta_desc) > 20:
            intro = meta_desc
        elif description:
            intro = description
        else:
            intro = f'{name}是一个专业的在线工具和服务平台，致力于为用户提供高质量的产品和服务。访问官网了解更多详情。'
        
        page_title = f'{name} - 009tg下海导航'
        page_keywords = f'{name}, {domain}, {description[:50] if description else ""}, 009tg导航'
        page_description = intro[:150] if intro else f'{name}官网地址和详细介绍，009tg下海导航收录。'
        
        # 页面文本
        visit_btn = '访问官网'
        copy_url = '复制链接'
        copied = '已复制'
        intro_title = '站点介绍'
        keywords_title = '关键词标签'
        category_title = '所属分类'
        related_title = '相关站点推荐'
        site_info_title = '站点信息'
        domain_label = '域名'
        added_label = '收录日期'
        back_to_cat = '返回分类'
        no_desc = '暂无详细介绍，访问官网了解更多。'
        no_keywords = '暂无关键词标签'
        no_related = '暂无相关站点推荐'
    else:
        if meta_desc and len(meta_desc) > 20:
            intro = meta_desc
        elif description_en:
            intro = description_en
        elif description:
            intro = description
        else:
            intro = f'{name} is a professional online tool and service platform dedicated to providing high-quality products and services. Visit the official website for more details.'
        
        page_title = f'{name} - 009tg Navigation'
        page_keywords = f'{name}, {domain}, {description_en[:50] if description_en else ""}, 009tg navigation'
        page_description = intro[:150] if intro else f'{name} official website and detailed introduction, curated by 009tg Navigation.'
        
        visit_btn = 'Visit Website'
        copy_url = 'Copy URL'
        copied = 'Copied'
        intro_title = 'About'
        keywords_title = 'Keywords'
        category_title = 'Category'
        related_title = 'Related Sites'
        site_info_title = 'Site Info'
        domain_label = 'Domain'
        added_label = 'Added'
        back_to_cat = 'Back to Category'
        no_desc = 'No detailed description available. Visit the official website for more.'
        no_keywords = 'No keywords available'
        no_related = 'No related sites'

    # 底部footer内容
    if lang == 'cn':
        footer_html = f'''<footer class="site-footer">
        <div class="footer-container">
            <div class="footer-links">
                <a href="../index.html">首页</a>
                <a href="../about.html">关于我们</a>
                <a href="../articles.html">文章资讯</a>
                <a href="../privacy.html">隐私政策</a>
                <a href="../terms.html">服务条款</a>
                <a href="../disclaimer.html">免责声明</a>
                <a href="../contact.html">联系我们</a>
                <a href="../sitemap.html">网站地图</a>
            </div>
            <div class="footer-copyright">
                © 2024-2026 009tg.com 版权所有 | Invisible Man
            </div>
            <div class="footer-disclaimer">
                本站仅供学习交流使用，所有内容均来自互联网，如有侵权请联系删除
            </div>
        </div>
    </footer>'''
    else:
        footer_html = f'''<footer class="site-footer">
        <div class="footer-container">
            <div class="footer-links">
                <a href="../index.html">Home</a>
                <a href="../about.html">About</a>
                <a href="../articles.html">Articles</a>
                <a href="../privacy.html">Privacy</a>
                <a href="../terms.html">Terms</a>
                <a href="../disclaimer.html">Disclaimer</a>
                <a href="../contact.html">Contact</a>
                <a href="../sitemap.html">Sitemap</a>
            </div>
            <div class="footer-copyright">
                © 2024-2026 009tg.com All Rights Reserved | Invisible Man
            </div>
            <div class="footer-disclaimer">
                For learning purposes only, all content from the internet, contact us for removal if infringement
            </div>
        </div>
    </footer>'''

    # 回到顶部浮动按钮（原生JS实现，详情页无jQuery）
    back_to_top_html = '''
    <style>
        .back-to-top {position:fixed;bottom:30px;right:30px;width:44px;height:44px;background-color:#337ab7;color:#fff;border:none;border-radius:50%;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,0.25);z-index:9999;display:none;align-items:center;justify-content:center;transition:all .3s;}
        .back-to-top.show{display:flex;}
        .back-to-top:hover{background-color:#286090;transform:translateY(-2px);}
        .back-to-top svg{width:20px;height:20px;fill:#fff;}
        [data-theme="dark"] .back-to-top{background-color:#4a90d9;}
        @media (max-width:768px){.back-to-top{bottom:20px;right:20px;width:40px;height:40px;}}
    </style>
    <button class="back-to-top" onclick="backToTop()" title="''' + ('回到顶部' if lang == 'cn' else 'Back to Top') + '''">
        <svg viewBox="0 0 24 24"><path d="M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z"/></svg>
    </button>
    <script>
        function backToTop(){var s={p:window.scrollY||document.documentElement.scrollTop},t=performance.now();function a(n){var e=Math.min((n-t)/300,1);window.scrollTo(0,s.p*(1-Math.pow(1-e,3)));e<1&&requestAnimationFrame(a)}requestAnimationFrame(a)}
        window.addEventListener('scroll',function(){var b=document.querySelector('.back-to-top');if(b){window.scrollY>300?b.classList.add('show'):b.classList.remove('show')}});
    </script>'''

    # favicon路径（用绝对路径，避免相对路径在URL重写后解析错误）
    favicon = get_favicon_path(site, favicon_mapping, asset_prefix='/')
    
    # 分类信息
    cat_id = category.get('id', 0) if category else 0
    cat_name = category.get('name', '') if category else ''
    cat_name_display = cat_name  # 翻译在调用处处理
    
    # 关键词标签HTML
    if meta_keywords:
        keywords_list = [k.strip() for k in re.split(r'[,，]', meta_keywords) if k.strip()][:10]
    else:
        # 自动从名称、域名、分类中提取关键词（不从中文描述中简单分词，避免产生无用标签）
        keywords_list = []
        # 站点名称
        if name:
            keywords_list.append(name)
        # 域名（去掉后缀）
        if domain:
            domain_main = re.sub(r'\.(com|cn|net|org|io|co|me|tv|cc|info|biz|xyz|top|club|site|online|store|tech|design|app|dev|cloud|ai|pro)$', '', domain)
            if domain_main and domain_main != domain:
                keywords_list.append(domain_main)
        # 分类名称
        if cat_name:
            keywords_list.append(cat_name)
        # 从描述中提取英文单词（英文单词空格分隔，提取较准确；中文不做简单分词）
        if description and len(description) > 10:
            en_words = re.findall(r'[a-zA-Z]{3,}', description)
            # 过滤常见无意义词
            stop_words = {'the', 'and', 'for', 'with', 'that', 'this', 'from', 'your', 'you', 'are', 'was', 'were', 'but', 'not', 'all', 'can', 'has', 'have', 'had', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'its', 'our', 'their', 'them', 'they', 'then', 'than', 'into', 'out', 'off', 'over', 'under', 'again', 'further', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'because', 'as', 'until', 'while', 'about', 'between', 'through', 'during', 'before', 'after', 'above', 'below', 'up', 'down', 'in', 'on', 'at', 'by', 'an', 'a', 'is', 'am', 'are', 'be', 'been', 'being', 'do', 'does', 'did', 'doing', 'have', 'has', 'had', 'having', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just'}
            for w in en_words[:5]:
                w_lower = w.lower()
                if w_lower not in stop_words and w_lower not in [k.lower() for k in keywords_list]:
                    keywords_list.append(w)
        # 去重并限制数量
        seen = set()
        unique_keywords = []
        for k in keywords_list:
            k_lower = k.lower()
            if k_lower not in seen and len(k) <= 20:
                seen.add(k_lower)
                unique_keywords.append(k)
        keywords_list = unique_keywords[:10]
    
    if keywords_list:
        keywords_html = ' '.join([f'<span class="keyword-tag">{k}</span>' for k in keywords_list])
    else:
        keywords_html = f'<span style="color: #999;">{no_keywords}</span>'
    
    # 相关站点HTML
    related_html = ''
    if related_sites:
        for rs in related_sites[:8]:
            rs_name = rs.get('name', '')
            rs_url = rs.get('url', '')
            rs_id = rs.get('id', 0)
            rs_favicon = get_favicon_path(rs, favicon_mapping)
            related_html += f'''
                        <a href="{rs_id}.html" class="related-site-card">
                            <img src="{rs_favicon}" alt="{rs_name}" class="related-favicon" onerror="this.src='/assets/images/logos/default.png'">
                            <span class="related-name">{rs_name}</span>
                        </a>
            '''
    else:
        related_html = f'<span style="color: #999;">{no_related}</span>'
    
    html = f'''<!DOCTYPE html>
<html lang="{'zh' if lang == 'cn' else 'en'}">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{page_title}</title>
    <meta name="keywords" content="{page_keywords}"/>
    <meta name="description" content="{page_description}"/>
    <link rel="shortcut icon" href="/assets/images/favicon.png">
    <link rel="stylesheet" href="/assets/css/fonts/linecons/css/linecons.css">
    <link rel="stylesheet" href="/assets/css/fonts/fontawesome/css/font-awesome.min.css">
    <link rel="stylesheet" href="/assets/css/bootstrap.css">
    <style>
        :root {{
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --text-primary: #333333;
            --text-secondary: #666666;
            --border-color: #e0e0e0;
            --accent-color: #337ab7;
        }}
        [data-theme="dark"] {{
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --border-color: #2a2a4a;
            --accent-color: #5dade2;
        }}
        body {{
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            transition: background 0.3s, color 0.3s;
        }}
        .site-detail-container {{
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        .site-header {{
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 30px;
            background: var(--bg-secondary);
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid var(--border-color);
        }}
        .site-logo {{
            width: 80px;
            height: 80px;
            border-radius: 12px;
            object-fit: contain;
            background: #f5f5f5;
            padding: 8px;
            border: 1px solid #e8e8e8;
            display: block;
            box-sizing: border-box;
        }}
        [data-theme="dark"] .site-logo {{
            background: #2a2a4a;
            border-color: #3a3a5a;
        }}
        .site-info h1 {{
            margin: 0 0 8px 0;
            font-size: 28px;
            font-weight: 700;
        }}
        .site-domain {{
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 12px;
        }}
        .site-actions {{
            display: flex;
            gap: 12px;
        }}
        .btn-primary {{
            background: var(--accent-color);
            color: #fff;
            border: none;
            padding: 10px 24px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: opacity 0.2s;
        }}
        .btn-primary:hover {{ opacity: 0.9; color: #fff; text-decoration: none; }}
        .btn-secondary {{
            background: transparent;
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            padding: 10px 24px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-secondary:hover {{ border-color: var(--accent-color); color: var(--accent-color); }}
        .section {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid var(--border-color);
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin: 0 0 16px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .section-title i {{ color: var(--accent-color); }}
        .intro-text {{
            font-size: 15px;
            line-height: 1.8;
            color: var(--text-primary);
        }}
        .keyword-tag {{
            display: inline-block;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 12px;
            color: var(--text-secondary);
            margin: 4px 6px 4px 0;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }}
        .info-item {{
            font-size: 14px;
        }}
        .info-label {{
            color: var(--text-secondary);
            font-size: 12px;
            margin-bottom: 4px;
        }}
        .info-value {{
            color: var(--text-primary);
            font-weight: 500;
            word-break: break-all;
        }}
        .related-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 12px;
        }}
        .related-site-card {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.2s;
        }}
        .related-site-card:hover {{
            border-color: var(--accent-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-decoration: none;
        }}
        .related-favicon {{
            width: 32px;
            height: 32px;
            border-radius: 6px;
            object-fit: contain;
            background: #fff;
            padding: 2px;
        }}
        .related-name {{
            font-size: 13px;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
        }}
        .breadcrumb {{
            margin-bottom: 20px;
            font-size: 14px;
            color: var(--text-secondary);
        }}
        .breadcrumb a {{
            color: var(--accent-color);
            text-decoration: none;
        }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .theme-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            color: var(--text-primary);
            transition: all 0.3s;
        }}
        .theme-toggle:hover {{ border-color: var(--accent-color); }}
        .site-footer {{
            background-color: #f8f9fa;
            border-top: 1px solid #e9ecef;
            padding: 30px 0 20px;
            margin-top: 40px;
        }}
        [data-theme="dark"] .site-footer {{
            background-color: var(--bg-sidebar) !important;
            border-top-color: var(--border-color) !important;
        }}
        .site-footer .footer-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        .site-footer .footer-links {{
            text-align: center;
            margin-bottom: 15px;
        }}
        .site-footer .footer-links a {{
            color: #666;
            text-decoration: none;
            margin: 0 12px;
            font-size: 14px;
            transition: color 0.2s;
        }}
        .site-footer .footer-links a:hover {{
            color: #007bff;
        }}
        [data-theme="dark"] .site-footer .footer-links a {{
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .site-footer .footer-links a:hover {{
            color: var(--link-color) !important;
        }}
        .site-footer .footer-copyright {{
            text-align: center;
            color: #999;
            font-size: 13px;
            margin-bottom: 8px;
        }}
        [data-theme="dark"] .site-footer .footer-copyright {{
            color: var(--text-muted) !important;
        }}
        .site-footer .footer-disclaimer {{
            text-align: center;
            color: #aaa;
            font-size: 12px;
        }}
        [data-theme="dark"] .site-footer .footer-disclaimer {{
            color: var(--text-muted) !important;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
        <i class="fa-moon-o" id="theme-icon"></i>
    </button>
    
    <div class="site-detail-container">
        <div class="breadcrumb">
            <a href="../index.html">{'首页' if lang == 'cn' else 'Home'}</a> / 
            <a href="../category/{cat_id}.html">{cat_name_display}</a> / 
            <span>{name}</span>
        </div>
        
        <div class="site-header">
            <img src="{favicon}" alt="{name}" class="site-logo" onerror="this.src='/assets/images/logos/default.png'">
            <div class="site-info">
                <h1>{name}</h1>
                <div class="site-domain"><i class="fa-globe" style="margin-right: 6px;"></i>{domain}</div>
                <div class="site-actions">
                    <a href="../redirect.html?url={url}&name={name}" target="_blank" class="btn-primary">
                        <i class="fa-external-link" style="margin-right: 6px;"></i>{visit_btn}
                    </a>
                    <button class="btn-secondary" onclick="copyUrl()">
                        <i class="fa-copy" style="margin-right: 6px;"></i>{copy_url}
                    </button>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fa-info-circle"></i>{intro_title}</h2>
            <div class="intro-text">{intro if intro else no_desc}</div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fa-tags"></i>{keywords_title}</h2>
            <div>{keywords_html}</div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fa-list-alt"></i>{site_info_title}</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">{domain_label}</div>
                    <div class="info-value">{domain}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">{category_title}</div>
                    <div class="info-value"><a href="../category/{cat_id}.html" style="color: var(--accent-color);">{cat_name_display}</a></div>
                </div>
                <div class="info-item">
                    <div class="info-label">{added_label}</div>
                    <div class="info-value">{created_at}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title"><i class="fa-thumbs-up"></i>{related_title}</h2>
            <div class="related-grid">
                {related_html}
            </div>
        </div>
    </div>
    
    <script>
        // 深色模式
        function toggleTheme() {{
            var current = document.documentElement.getAttribute('data-theme');
            var newTheme = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            document.getElementById('theme-icon').className = newTheme === 'dark' ? 'fa-sun-o' : 'fa-moon-o';
        }}
        (function() {{
            var saved = localStorage.getItem('theme');
            if (saved) {{
                document.documentElement.setAttribute('data-theme', saved);
                document.getElementById('theme-icon').className = saved === 'dark' ? 'fa-sun-o' : 'fa-moon-o';
            }}
        }})();
        
        // 复制URL
        function copyUrl() {{
            navigator.clipboard.writeText('{url}').then(function() {{
                var btn = event.target.closest('button');
                var original = btn.innerHTML;
                btn.innerHTML = '<i class="fa-check" style="margin-right: 6px;"></i>{copied}';
                setTimeout(function() {{ btn.innerHTML = original; }}, 2000);
            }});
        }}
    </script>
    {footer_html}
    {back_to_top_html}
</body>
</html>'''
    
    return html

import re

def main():
    print('=' * 60)
    print('生成站点详情页（中英文）')
    print('=' * 60)
    
    # 加载数据
    with open(os.path.join(PROJECT_ROOT, '完整版导航.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(os.path.join(PROJECT_ROOT, 'favicon_mapping.json'), 'r', encoding='utf-8') as f:
        favicon_mapping = json.load(f)
    
    meta_file = os.path.join(PROJECT_ROOT, 'data/sites_meta.json')
    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta_data = json.load(f)
        print(f'加载meta数据: {len(meta_data)} 条')
    else:
        meta_data = {}
        print('未找到meta数据，使用默认介绍')
    
    # 加载分类翻译
    try:
        with open(os.path.join(PROJECT_ROOT, 'tools/category_translation.json'), 'r', encoding='utf-8') as f:
            cat_trans = json.load(f)
    except:
        cat_trans = {}
    
    # 构建分类映射和站点->分类映射
    site_category_map = {}
    category_map = {}
    all_sites = []
    
    def process_group(group, parent=None):
        category_map[group['id']] = group
        for site in group.get('sites', []):
            site_category_map[site['id']] = group
            all_sites.append(site)
        for child in group.get('children', []):
            process_group(child, group)
    
    for g in data['groups']:
        process_group(g)
    
    print(f'总站点数: {len(all_sites)}')
    print(f'分类数: {len(category_map)}')
    
    # 创建输出目录
    cn_dir = os.path.join(PROJECT_ROOT, 'cn', 'site')
    en_dir = os.path.join(PROJECT_ROOT, 'en', 'site')
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    # 生成每个站点的详情页
    cn_count = 0
    en_count = 0
    
    for site in all_sites:
        site_id = site.get('id', 0)
        category = site_category_map.get(site_id, None)
        
        # 相关站点（同分类的其他站点）
        related_sites = []
        if category:
            related_sites = [s for s in category.get('sites', []) if s.get('id') != site_id][:8]
        
        # 分类名（翻译）
        cat_name = category.get('name', '') if category else ''
        cat_name_en = cat_trans.get(cat_name, cat_name) if cat_name else ''
        
        # 中文页面
        html_cn = generate_site_detail_page(site, category, related_sites, favicon_mapping, meta_data, lang='cn')
        # 替换分类名为中文
        html_cn = html_cn.replace('{cat_name_display}', cat_name)
        
        with open(os.path.join(cn_dir, f'{site_id}.html'), 'w', encoding='utf-8') as f:
            f.write(html_cn)
        cn_count += 1
        
        # 英文页面
        html_en = generate_site_detail_page(site, category, related_sites, favicon_mapping, meta_data, lang='en')
        # 替换分类名为英文
        html_en = html_en.replace('{cat_name_display}', cat_name_en)
        
        with open(os.path.join(en_dir, f'{site_id}.html'), 'w', encoding='utf-8') as f:
            f.write(html_en)
        en_count += 1
        
        if (cn_count) % 500 == 0:
            print(f'  进度: {cn_count}/{len(all_sites)}')
    
    print('-' * 60)
    print(f'生成完成！')
    print(f'  中文详情页: {cn_count} 个 (cn/site/)')
    print(f'  英文详情页: {en_count} 个 (en/site/)')
    print(f'  总计: {cn_count + en_count} 个页面')

if __name__ == '__main__':
    main()
