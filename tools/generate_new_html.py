#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新HTML生成脚本 - 支持多级分类、翻页功能和中英文双语

用途：
    生成导航网站HTML文件，支持多级分类、翻页功能和中英文双语。

功能概述：
    1. 读取JSON数据
    2. 生成嵌套的导航菜单
    3. 生成内容区域（支持翻页）
    4. 生成中文和英文两个版本
    5. 保存为HTML文件

使用方法：
    python generate_new_html.py
    python generate_new_html.py --lang cn  # 只生成中文
    python generate_new_html.py --lang en  # 只生成英文

主要特性：
    - 生成完整的HTML结构
    - 支持多级分类导航菜单
    - 生成内容区域（支持翻页）
    - 使用本地缓存的favicon
    - 支持中英文双语（英文使用description_en字段）
    - 自动生成cn/和en/目录下的页面
"""

import json
import os
import shutil
import argparse
from urllib.parse import urlparse

# ============================================================
# 分类名中英文翻译映射
# ============================================================
CATEGORY_TRANSLATION = {
    # 一级分类
    "下海推荐": "Featured",
    "AI工具": "AI Tools",
    "跨境资讯": "Cross-border News",
    "跨境推广": "Cross-border Marketing",
    "社媒资源": "Social Media",
    "全球网络": "Global Network",
    "全球接码": "SMS Verification",
    "数字货币": "Crypto",
    "全球支付": "Global Payment",
    "Facebook": "Facebook",
    "Google": "Google",
    "广告工具": "Ad Tools",
    "指纹浏览器": "Antidetect Browser",
    "全球APP下载": "Global Apps",
    "内容制作": "Content Creation",
    "技术交流": "Tech Community",
    "引流工具": "Traffic Tools",
    "跨境电商": "E-commerce",
    "跨境服务": "Cross-border Services",
    # 二级分类 - 下海推荐
    "教程福利": "Tutorials & Benefits",
    "常用工具": "Common Tools",
    "推荐工具": "Recommended Tools",
    "常用网址": "Common URLs",
    "效率工具": "Efficiency Tools",
    "短链生成工具": "Short Link Tools",
    "指纹检测": "Fingerprint Detection",
    "筛号工具": "Number Screening Tools",
    # 二级分类 - AI工具
    "AI常用工具": "AI Common Tools",
    "AI办公工具": "AI Office Tools",
    "AI写作工具": "AI Writing Tools",
    "AI视频工具": "AI Video Tools",
    "AI Agent智能体": "AI Agents",
    "AI内容检测": "AI Content Detection",
    "AI图像工具": "AI Image Tools",
    "AI学习资源": "AI Learning Resources",
    "AI开发平台": "AI Development Platform",
    "AI搜索": "AI Search",
    "AI翻译": "AI Translation",
    "AI资讯": "AI News",
    "AI音频": "AI Audio",
    "AI编程工具": "AI Programming Tools",
    "AI设计工具": "AI Design Tools",
    # 二级分类 - 跨境资讯
    "全球新闻": "Global News",
    "中国论坛": "China Forums",
    "国外论坛": "Foreign Forums",
    "行业媒体": "Industry Media",
    # 二级分类 - 跨境推广
    "广告联盟": "Ad Networks",
    "SEO工具": "SEO Tools",
    "流量交换": "Traffic Exchange",
    "邮件营销": "Email Marketing",
    # 二级分类 - 社媒资源
    "社媒工具": "Social Media Tools",
    "社媒导航": "Social Media Navigation",
    # 二级分类 - 全球网络
    "中国VPS": "China VPS",
    "国外VPS": "Foreign VPS",
    "域名注册": "Domain Registration",
    "CDN加速": "CDN Acceleration",
    "DNS服务": "DNS Services",
    # 二级分类 - 全球接码
    "接码平台": "SMS Platforms",
    "虚拟号码": "Virtual Numbers",
    # 二级分类 - 数字货币
    "交易所": "Exchanges",
    "钱包": "Wallets",
    "行情工具": "Market Tools",
    # 二级分类 - 全球支付
    "支付平台": "Payment Platforms",
    "收款工具": "Collection Tools",
    # 二级分类 - Facebook
    "Facebook工具": "Facebook Tools",
    "Facebook导航": "Facebook Navigation",
    # 二级分类 - Google
    "Google常用": "Google Common",
    "谷歌插件": "Chrome Extensions",
    # 二级分类 - 广告工具
    "广告平台": "Ad Platforms",
    "广告检测": "Ad Detection",
    # 二级分类 - 指纹浏览器
    "指纹浏览器软件": "Antidetect Browsers",
    # 二级分类 - 全球APP下载
    "电商app": "E-commerce Apps",
    "常用app": "Common Apps",
    # 二级分类 - 内容制作
    "软件开发": "Software Development",
    "脚本工具": "Script Tools",
    "素材编辑": "Media Editing",
    "图库网站": "Image Libraries",
    # 二级分类 - 技术交流
    "技术论坛": "Tech Forums",
    "开发资源": "Dev Resources",
    # 二级分类 - 引流工具
    "引流平台": "Traffic Platforms",
    "群发工具": "Bulk Messaging",
    # 二级分类 - 跨境电商
    "电商平台": "E-commerce Platforms",
    "选品工具": "Product Research",
    "ERP系统": "ERP Systems",
    # 二级分类 - 跨境服务
    "物流服务": "Logistics",
    "仓储服务": "Warehousing",
    "代运营": "Agency Operations",
}


def translate_category(name, lang='cn'):
    """翻译分类名"""
    if lang == 'cn':
        return name
    return CATEGORY_TRANSLATION.get(name, name)


def get_icon_for_category(category_name):
    """根据分类名称获取对应的图标"""
    icon_mapping = {
        "下海推荐": "fa-wrench",
        "AI工具": "fa-microphone",
        "跨境资讯": "fa-file-text-o",
        "跨境推广": "fa-globe",
        "社媒资源": "fa-share",
        "全球网络": "fa-cloud",
        "全球接码": "fa-phone",
        "数字货币": "fa-credit-card",
        "全球支付": "fa-credit-card",
        "Facebook": "fa-facebook",
        "Google": "fa-google",
        "广告工具": "fa-bar-chart",
        "指纹浏览器": "fa-globe",
        "全球APP下载": "fa-download",
        "内容制作": "fa-pencil",
        "技术交流": "fa-comments",
        "引流工具": "fa-share-alt",
        "跨境电商": "fa-shopping-cart",
        "跨境服务": "fa-briefcase"
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


def generate_nav_menu(groups, lang='cn'):
    """生成导航菜单HTML"""
    def generate_menu_item(group, level=0):
        icon_class = get_icon_for_category(group['name']) if level == 0 else None
        display_name = translate_category(group['name'], lang)

        has_children = 'children' in group and len(group['children']) > 0

        if has_children:
            children_html = ''.join([generate_menu_item(child, level + 1) for child in group['children']])
            if icon_class:
                return f'''<li>
                <a>
                    <i class="{icon_class}"></i>
                    <span class="title">{display_name}</span>
                </a>
                <ul>{children_html}</ul>
            </li>'''
            else:
                return f'''<li>
                <a>
                    <span class="title">{display_name}</span>
                </a>
                <ul>{children_html}</ul>
            </li>'''
        else:
            return f'''<li>
                <a href="#{group['name']}" class="smooth">
                    <span class="title">{display_name}</span>
                </a>
            </li>'''

    return ''.join([generate_menu_item(group) for group in groups])


def generate_site_data(group, favicon_mapping, lang='cn', asset_prefix=''):
    """生成网站数据JavaScript"""
    sites_data = []

    for site in group.get('sites', []):
        site_name = site.get('name', '未知网站')
        site_url = site.get('url', '#')
        # 英文使用description_en，中文使用description
        if lang == 'en':
            site_description = site.get('description_en') or site.get('description', '')
        else:
            site_description = site.get('description', '')
        site_icon = site.get('icon', f'{asset_prefix}assets/images/logos/default.png')

        try:
            parsed_url = urlparse(site_url)
            domain = parsed_url.netloc
            if domain in favicon_mapping:
                site_icon = asset_prefix + favicon_mapping[domain]
        except:
            pass

        sites_data.append({
            'id': site.get('id', 0),
            'name': site_name,
            'url': site_url,
            'description': site_description,
            'icon': site_icon
        })

    return sites_data


def generate_all_sites_data(groups, favicon_mapping, lang='cn', asset_prefix=''):
    """生成所有网站数据JavaScript"""
    sites_data_js = []

    def process_group(group):
        if group.get('sites'):
            category_name = group['name']  # JS中用原始分类名作为key
            sites = generate_site_data(group, favicon_mapping, lang, asset_prefix)
            sites_json = json.dumps(sites, ensure_ascii=False)
            sites_data_js.append(f"allSitesData['{category_name}'] = {sites_json};")
        if 'children' in group:
            for child in group['children']:
                process_group(child)

    for group in groups:
        process_group(group)

    return '\n        '.join(sites_data_js)


def generate_content_section(group, favicon_mapping, lang='cn', is_root=False):
    """生成内容区域HTML"""
    sites = group.get('sites', [])
    total_sites = len(sites)
    category_name = group['name']  # data-category用原始名，JS查找用
    category_id = group.get('id', 0)
    display_name = translate_category(group['name'], lang)

    # 查看更多链接文本（大类显示"更多分类"，子分类显示"更多内容"）
    if lang == 'cn':
        if is_root:
            view_more_text = '更多分类'
        else:
            view_more_text = '更多内容'
        arrow = '→'
    else:
        if is_root:
            view_more_text = 'More Categories'
        else:
            view_more_text = 'More Content'
        arrow = '→'

    # 标题行：分类名（可点击）+ 查看更多（最右侧）
    title_html = f'''<h4 class="text-gray category-title">
    <i class="linecons-tag" style="margin-right: 7px;" id="{category_name}"></i>
    <a href="category/{category_id}.html" class="category-name-link">{display_name}</a>
    <a href="category/{category_id}.html" class="view-more-link">{view_more_text} {arrow}</a>
</h4>'''

    # 一级分类没有直接站点时，只显示标题行
    if is_root and total_sites == 0:
        return title_html + '<br />'

    # 根据网站数量决定是否启用分页（超过18个才分页）
    enable_pagination = total_sites > 18

    if enable_pagination:
        return f'''{title_html}
<div class="row category-row" data-category="{category_name}" data-total="{total_sites}" data-pagination="true">
    <div class="pagination-left"><button class="btn btn-sm btn-default prev-page" data-category="{category_name}" disabled>
        <i class="fa fa-chevron-left"></i>
    </button></div>
    <div class="category-content"></div>
    <div class="pagination-right">
        <button class="btn btn-sm btn-default next-page" data-category="{category_name}">
            <i class="fa fa-chevron-right"></i>
        </button>
    </div>
</div>
<br />'''
    else:
        return f'''{title_html}
<div class="row category-row" data-category="{category_name}" data-total="{total_sites}" data-pagination="false">
    <div class="pagination-left"></div>
    <div class="category-content"></div>
    <div class="pagination-right"></div>
</div>
<br />'''


def generate_all_content(groups, favicon_mapping, lang='cn'):
    """生成所有内容区域"""
    content_sections = []

    def process_group(group, is_root=False):
        # 一级分类始终显示（即使没有直接站点，因为有子分类）
        # 子分类只有有站点时才显示
        if is_root or group.get('sites'):
            content_sections.append(generate_content_section(group, favicon_mapping, lang, is_root))
        if 'children' in group:
            for child in group['children']:
                process_group(child, is_root=False)

    for group in groups:
        process_group(group, is_root=True)

    return ''.join(content_sections)


def generate_recent_and_hot(groups, favicon_mapping, lang='cn', asset_prefix='../'):
    """生成最新收录和热门分类榜板块"""
    from urllib.parse import urlparse
    
    # 收集所有站点
    all_sites = []
    def collect_sites(group):
        for site in group.get('sites', []):
            site['_group_name'] = group.get('name', '')
            site['_group_id'] = group.get('id', 0)
            all_sites.append(site)
        for child in group.get('children', []):
            collect_sites(child)
    for g in groups:
        collect_sites(g)
    
    # 最新收录（按created_at降序，取12个）
    recent_sites = sorted(all_sites, key=lambda s: s.get('created_at', ''), reverse=True)[:12]
    
    # 热门分类（按站点数降序，取10个一级分类）
    cat_counts = []
    for g in groups:
        count = len(g.get('sites', []))
        for child in g.get('children', []):
            count += len(child.get('sites', []))
        if count > 0:
            cat_counts.append((g, count))
    cat_counts.sort(key=lambda x: x[1], reverse=True)
    hot_cats = cat_counts[:10]
    
    # 加载分类翻译
    try:
        trans_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools/category_translation.json')
        with open(trans_path, 'r', encoding='utf-8') as f:
            cat_trans = json.load(f)
    except:
        cat_trans = {}
    
    if lang == 'cn':
        recent_title = '最新收录'
        recent_subtitle = '最近添加的优质站点'
        hot_title = '热门分类'
        hot_subtitle = '站点数量最多的分类'
    else:
        recent_title = 'Recently Added'
        recent_subtitle = 'Latest quality sites added'
        hot_title = 'Popular Categories'
        hot_subtitle = 'Categories with most sites'
    
    # 生成最新收录HTML
    recent_html = '''
            <!-- 最新收录 -->
            <div class="row" style="margin-bottom: 30px;">
                <div class="col-md-12">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h3 class="panel-title" style="font-size: 18px; font-weight: 600;">
                                <i class="fa-clock-o" style="margin-right: 8px; color: #337ab7;"></i>''' + recent_title + '''
                                <small style="color: #999; margin-left: 10px; font-size: 13px;">''' + recent_subtitle + '''</small>
                            </h3>
                        </div>
                        <div class="panel-body" style="padding: 15px;">
                            <div class="row">
    '''
    
    for site in recent_sites:
        name = site.get('name', '')
        url = site.get('url', '')
        icon = site.get('icon', '')
        domain = ''
        try:
            domain = urlparse(url).netloc
        except:
            pass
        
        favicon_path = icon
        if domain and domain in favicon_mapping:
            favicon_path = favicon_mapping[domain]
        if not favicon_path:
            favicon_path = asset_prefix + 'assets/images/logos/default.png'
        elif favicon_path.startswith('assets/'):
            favicon_path = asset_prefix + favicon_path
        
        created = site.get('created_at', '')
        
        recent_html += '''
                                <div class="col-md-2 col-sm-3 col-xs-4" style="margin-bottom: 12px;">
                                    <a href="site/''' + str(site.get('id', 0)) + '''.html" 
                                       style="display: block; padding: 10px; border: 1px solid #eee; border-radius: 6px; text-decoration: none; transition: all 0.2s; height: 100%;"
                                       onmouseover="this.style.borderColor='#337ab7';this.style.boxShadow='0 2px 8px rgba(0,0,0,0.1)'"
                                       onmouseout="this.style.borderColor='#eee';this.style.boxShadow='none'">
                                        <div style="text-align: center;">
                                            <img src="''' + favicon_path + '''" alt="''' + name + '''" style="width: 32px; height: 32px; border-radius: 4px; margin-bottom: 6px;" onerror="this.src=''' + "'" + asset_prefix + 'assets/images/logos/default.png' + "'" + '''">
                                            <div style="font-size: 12px; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500;">''' + name + '''</div>
                                            <div style="font-size: 11px; color: #999; margin-top: 2px;">''' + created + '''</div>
                                        </div>
                                    </a>
                                </div>
        '''
    
    recent_html += '''
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    '''
    
    # 生成热门分类HTML
    hot_html = '''
            <!-- 热门分类榜 -->
            <div class="row" style="margin-bottom: 30px;">
                <div class="col-md-12">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h3 class="panel-title" style="font-size: 18px; font-weight: 600;">
                                <i class="fa-fire" style="margin-right: 8px; color: #e74c3c;"></i>''' + hot_title + '''
                                <small style="color: #999; margin-left: 10px; font-size: 13px;">''' + hot_subtitle + '''</small>
                            </h3>
                        </div>
                        <div class="panel-body" style="padding: 15px;">
                            <div class="row">
    '''
    
    for i, (cat, count) in enumerate(hot_cats, 1):
        cat_id = cat.get('id', 0)
        cat_name = cat.get('name', '')
        if lang == 'en' and cat_name in cat_trans:
            display_name = cat_trans[cat_name]
        else:
            display_name = cat_name
        
        if i <= 3:
            rank_color = '#e74c3c'
        elif i <= 6:
            rank_color = '#f39c12'
        else:
            rank_color = '#999'
        
        hot_html += '''
                                <div class="col-md-6" style="margin-bottom: 10px;">
                                    <a href="category/''' + str(cat_id) + '''.html" style="display: flex; align-items: center; padding: 8px 12px; border: 1px solid #eee; border-radius: 6px; text-decoration: none; transition: all 0.2s;"
                                       onmouseover="this.style.borderColor='#337ab7';this.style.backgroundColor='#f8f9fa'"
                                       onmouseout="this.style.borderColor='#eee';this.style.backgroundColor='transparent'">
                                        <span style="display: inline-block; width: 24px; height: 24px; line-height: 24px; text-align: center; background: ''' + rank_color + '''; color: #fff; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 10px;">''' + str(i) + '''</span>
                                        <span style="flex: 1; font-size: 14px; color: #333; font-weight: 500;">''' + display_name + '''</span>
                                        <span style="font-size: 12px; color: #999;">''' + str(count) + ''' sites</span>
                                    </a>
                                </div>
        '''
    
    hot_html += '''
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    '''
    
    # 生成站长工具板块
    if lang == 'cn':
        tools_title = '站长工具'
        tools_subtitle = '免费在线工具集合，提升工作效率'
        tools_view_all = '查看全部'
        tools_categories = [
            ('网络工具', [
                ('IP查询', 'ip.html'),
                ('DNS查询', 'dns.html'),
                ('WHOIS查询', 'whois.html'),
                ('HTTP检测', 'http.html'),
                ('端口扫描', 'port.html'),
            ]),
            ('编码转换', [
                ('Base64编解码', 'base64.html'),
                ('URL编解码', 'url.html'),
                ('时间戳转换', 'timestamp.html'),
                ('图片转Base64', 'img-base64.html'),
            ]),
            ('开发工具', [
                ('JSON格式化', 'json.html'),
                ('正则表达式', 'regex.html'),
                ('JWT解析', 'jwt.html'),
                ('UUID/哈希', 'uuid-hash.html'),
            ]),
            ('计算工具', [
                ('房贷计算', 'mortgage.html'),
                ('个税计算', 'tax.html'),
                ('单位换算', 'unit.html'),
                ('日期计算', 'date-calc.html'),
            ]),
            ('文本/图片', [
                ('密码生成器', 'password.html'),
                ('二维码生成', 'qrcode.html'),
                ('颜色工具', 'color.html'),
                ('CSS渐变', 'css-gradient.html'),
            ]),
        ]
    else:
        tools_title = 'Webmaster Tools'
        tools_subtitle = 'Free online tools to boost your productivity'
        tools_view_all = 'View All'
        tools_categories = [
            ('Network', [
                ('IP Lookup', 'ip.html'),
                ('DNS Lookup', 'dns.html'),
                ('WHOIS Lookup', 'whois.html'),
                ('HTTP Check', 'http.html'),
                ('Port Scan', 'port.html'),
            ]),
            ('Encoding', [
                ('Base64', 'base64.html'),
                ('URL Encode', 'url.html'),
                ('Timestamp', 'timestamp.html'),
                ('Img to Base64', 'img-base64.html'),
            ]),
            ('Developer', [
                ('JSON Formatter', 'json.html'),
                ('Regex Tester', 'regex.html'),
                ('JWT Decoder', 'jwt.html'),
                ('UUID/Hash', 'uuid-hash.html'),
            ]),
            ('Calculator', [
                ('Mortgage', 'mortgage.html'),
                ('Income Tax', 'tax.html'),
                ('Unit Converter', 'unit.html'),
                ('Date Calculator', 'date-calc.html'),
            ]),
            ('Text/Image', [
                ('Password Gen', 'password.html'),
                ('QR Code', 'qrcode.html'),
                ('Color Picker', 'color.html'),
                ('CSS Gradient', 'css-gradient.html'),
            ]),
        ]
    
    tools_html = '''
            <!-- 站长工具 -->
            <div class="row" style="margin-bottom: 30px;">
                <div class="col-md-12">
                    <div class="panel panel-default">
                        <div class="panel-heading" style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 class="panel-title" style="font-size: 18px; font-weight: 600;">
                                <i class="fa-wrench" style="margin-right: 8px; color: #27ae60;"></i>''' + tools_title + '''
                                <small style="color: #999; margin-left: 10px; font-size: 13px;">''' + tools_subtitle + '''</small>
                            </h3>
                            <a href="../tools/index.html" style="font-size: 13px; color: #337ab7; text-decoration: none;">''' + tools_view_all + ''' <i class="fa-angle-right"></i></a>
                        </div>
                        <div class="panel-body" style="padding: 15px;">
                            <div class="row">
    '''
    
    for cat_name, tools in tools_categories:
        tools_html += '''
                                <div class="col-md-15 col-sm-3 col-xs-6" style="margin-bottom: 15px;">
                                    <div style="font-size: 13px; font-weight: 600; color: #333; margin-bottom: 8px; padding-bottom: 5px; border-bottom: 1px solid #eee;">''' + cat_name + '''</div>
                                    <ul style="list-style: none; padding: 0; margin: 0;">
        '''
        for tool_name, tool_file in tools:
            tools_html += '''
                                        <li style="margin-bottom: 5px;">
                                            <a href="../tools/''' + tool_file + '''" style="font-size: 12px; color: #666; text-decoration: none; display: block; padding: 3px 0; transition: color 0.2s;"
                                               onmouseover="this.style.color='#337ab7'" onmouseout="this.style.color='#666'">''' + tool_name + '''</a>
                                        </li>
            '''
        tools_html += '''
                                    </ul>
                                </div>
        '''
    
    tools_html += '''
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    '''
    
    return recent_html + hot_html + tools_html


def generate_language_switcher(lang='cn'):
    """生成语言切换器HTML"""
    if lang == 'cn':
        return '''
                    <li class="dropdown hover-line language-switcher">
                        <a href="index.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="../assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                        </a>
                        <ul class="dropdown-menu languages">
                            <li>
                                <a href="../en/index.html">
                                    <img src="../assets/images/flags/flag-us.png" alt="flag-us" /> English
                                </a>
                            </li>
                            <li class="active">
                                <a href="../cn/index.html">
                                    <img src="../assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                                </a>
                            </li>
                        </ul>
                    </li>'''
    else:
        return '''
                    <li class="dropdown hover-line language-switcher">
                        <a href="index.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="../assets/images/flags/flag-us.png" alt="flag-us" /> English
                        </a>
                        <ul class="dropdown-menu languages">
                            <li class="active">
                                <a href="../en/index.html">
                                    <img src="../assets/images/flags/flag-us.png" alt="flag-us" /> English
                                </a>
                            </li>
                            <li>
                                <a href="../cn/index.html">
                                    <img src="../assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                                </a>
                            </li>
                        </ul>
                    </li>'''


def generate_html(lang='cn'):
    """生成HTML文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    print(f"读取JSON数据...")
    json_path = os.path.join(project_root, '完整版导航.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("读取favicon映射...")
    favicon_mapping_path = os.path.join(project_root, 'favicon_mapping.json')
    with open(favicon_mapping_path, 'r', encoding='utf-8') as f:
        favicon_mapping = json.load(f)

    print("构建分类树...")
    root_groups = build_category_tree(data['groups'])

    # cn/和en/目录下的页面，资源引用用../前缀
    asset_prefix = '../'

    print(f"生成导航菜单 ({lang})...")
    nav_html = generate_nav_menu(root_groups, lang)

    print(f"生成网站数据 ({lang})...")
    sites_data_js = generate_all_sites_data(root_groups, favicon_mapping, lang, asset_prefix)

    print(f"生成内容区域 ({lang})...")
    content_html = generate_all_content(root_groups, favicon_mapping, lang)

    print(f"生成最新收录和热门榜 ({lang})...")
    recent_hot_html = generate_recent_and_hot(root_groups, favicon_mapping, lang, asset_prefix)

    lang_switcher = generate_language_switcher(lang)

    # 页面元信息
    if lang == 'cn':
        html_lang = 'zh'
        title = '009tg下海导航 - Invisible Man'
        keywords = '009tg下海导航,网址导航,上网导航,网址大全,网址目录,创业工具,副业赚钱,投资理财,跨境电商,营销工具,AI工具,社交媒体,独立站,广告投放'
        description = '009tg下海导航致力于打造国内最好的互联网上优质网站网址大全，收录了全网好用强大的网站网址和软件包括创业、副业、投资、跨境电商、营销工具、AI工具、社交媒体、独立站、广告投放、生活、休闲、办公、工具、资源等超全面的网址和职业技巧内容，让您的上网体验更便捷更放心，努力成为全民级人人都在用的网址导航。'
        about_text = '关于本站'
        articles_text = '文章资讯'
        search_placeholder = '搜索站点...'
        search_no_result = '未找到相关站点'
        search_result_count = '找到 {count} 个站点'
        nav_articles = '文章资讯'
        nav_about = '关于我们'
        nav_contact = '联系我们'
    else:
        html_lang = 'en'
        title = '009tg Navigation - Invisible Man'
        keywords = '009tg navigation, url directory, web directory, startup tools, side hustle, investment, cross-border e-commerce, marketing tools, AI tools, social media, advertising'
        description = '009tg Navigation is a comprehensive web directory featuring the best websites and tools for entrepreneurship, side hustles, investment, cross-border e-commerce, marketing, AI tools, social media, and more. Your ultimate resource for discovering powerful online tools and professional tips.'
        about_text = 'About Us'
        articles_text = 'Articles'
        search_placeholder = 'Search sites...'
        search_no_result = 'No sites found'
        search_result_count = '{count} sites found'
        nav_articles = 'Articles'
        nav_about = 'About'
        nav_contact = 'Contact'

    # 底部footer内容
    if lang == 'cn':
        footer_html = f'''<footer class="site-footer">
        <div class="footer-container">
            <div class="footer-links">
                <a href="{asset_prefix}cn/about.html">关于我们</a>
                <a href="{asset_prefix}cn/articles.html">文章资讯</a>
                <a href="{asset_prefix}cn/privacy.html">隐私政策</a>
                <a href="{asset_prefix}cn/terms.html">服务条款</a>
                <a href="{asset_prefix}cn/disclaimer.html">免责声明</a>
                <a href="{asset_prefix}cn/contact.html">联系我们</a>
                <a href="{asset_prefix}cn/sitemap.html">网站地图</a>
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
                <a href="{asset_prefix}en/about.html">About</a>
                <a href="{asset_prefix}en/articles.html">Articles</a>
                <a href="{asset_prefix}en/privacy.html">Privacy</a>
                <a href="{asset_prefix}en/terms.html">Terms</a>
                <a href="{asset_prefix}en/disclaimer.html">Disclaimer</a>
                <a href="{asset_prefix}en/contact.html">Contact</a>
                <a href="{asset_prefix}en/sitemap.html">Sitemap</a>
            </div>
            <div class="footer-copyright">
                © 2024-2026 009tg.com All Rights Reserved | Invisible Man
            </div>
            <div class="footer-disclaimer">
                For learning purposes only, all content from the internet, contact us for removal if infringement
            </div>
        </div>
    </footer>'''

    # 回到顶部浮动按钮（原生JS实现，不依赖框架）
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

    print(f"生成完整HTML ({lang})...")
    html = f'''<!DOCTYPE html>
<html lang="{html_lang}">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="author" content="Invisible man" />
    <title>{title}</title>
    <meta name="theme-color" content="#f9f9f9"/>
    <meta name="keywords" content="{keywords}"/>
    <meta name="description" content="{description}"/>
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
    <style>
        /* ========== 深色模式主题变量 ========== */
        :root {{
            --bg-main: #f4f4f4;
            --bg-content: #ffffff;
            --bg-sidebar: #303641;
            --bg-card: #ffffff;
            --bg-card-hover: #f8f9fa;
            --bg-navbar: #ffffff;
            --bg-input: #ffffff;
            --text-primary: #373e4a;
            --text-secondary: #6c757d;
            --text-muted: #979898;
            --text-sidebar: #979898;
            --text-sidebar-hover: #ffffff;
            --border-color: #e4e6e9;
            --border-card: #e4e6e9;
            --link-color: #337ab7;
            --link-hover: #23527c;
            --shadow-card: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.15);
        }}
        [data-theme="dark"] {{
            --bg-main: #1a1d23;
            --bg-content: #22262e;
            --bg-sidebar: #16181d;
            --bg-card: #2a2f38;
            --bg-card-hover: #333945;
            --bg-navbar: #22262e;
            --bg-input: #2a2f38;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --text-muted: #707070;
            --text-sidebar: #979898;
            --text-sidebar-hover: #ffffff;
            --border-color: #3a3f48;
            --border-card: #3a3f48;
            --link-color: #5dade2;
            --link-hover: #85c1e9;
            --shadow-card: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.5);
        }}
        /* 深色模式全局覆盖 */
        [data-theme="dark"] body {{
            background-color: var(--bg-main) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .main-content {{
            background-color: var(--bg-content) !important;
        }}
        [data-theme="dark"] .navbar.user-info-navbar {{
            background-color: var(--bg-navbar) !important;
            border-bottom-color: var(--border-color) !important;
        }}
        [data-theme="dark"] .user-info-menu a {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .user-info-menu a:hover {{
            color: var(--link-color) !important;
        }}
        [data-theme="dark"] .panel {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-card) !important;
        }}
        [data-theme="dark"] .panel-heading {{
            background-color: var(--bg-card) !important;
            border-bottom-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .panel-title {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .site-item .panel {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-card) !important;
            box-shadow: var(--shadow-card) !important;
        }}
        [data-theme="dark"] .site-item .panel:hover {{
            background-color: var(--bg-card-hover) !important;
            box-shadow: var(--shadow-card-hover) !important;
        }}
        [data-theme="dark"] .site-item .panel-body {{
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .site-item .panel-title a {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .site-item .panel-title a:hover {{
            color: var(--link-color) !important;
        }}
        [data-theme="dark"] .breadcrumb {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
        }}
        [data-theme="dark"] .breadcrumb a {{
            color: var(--link-color) !important;
        }}
        [data-theme="dark"] .pagination .btn {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .pagination .btn:hover:not(:disabled) {{
            background-color: var(--bg-card-hover) !important;
        }}
        [data-theme="dark"] .footer {{
            background-color: var(--bg-sidebar) !important;
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .footer a {{
            color: var(--link-color) !important;
        }}
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
        [data-theme="dark"] .form-control,
        [data-theme="dark"] input,
        [data-theme="dark"] select,
        [data-theme="dark"] textarea {{
            background-color: var(--bg-input) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .table {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .table td,
        [data-theme="dark"] .table th {{
            border-color: var(--border-color) !important;
        }}
        [data-theme="dark"] .well {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .alert-info {{
            background-color: #1e3a5f !important;
            border-color: #2c5282 !important;
            color: #90cdf4 !important;
        }}
        [data-theme="dark"] .alert-warning {{
            background-color: #5f4a1e !important;
            border-color: #82682c !important;
            color: #f6e05e !important;
        }}
        [data-theme="dark"] .alert-success {{
            background-color: #1e5f3a !important;
            border-color: #2c8252 !important;
            color: #9ae6b4 !important;
        }}
        [data-theme="dark"] .alert-danger {{
            background-color: #5f1e1e !important;
            border-color: #822c2c !important;
            color: #feb2b2 !important;
        }}
        /* 搜索结果深色模式 */
        [data-theme="dark"] #search-results {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        }}
        [data-theme="dark"] #search-results .search-result-item {{
            border-bottom-color: var(--border-color) !important;
        }}
        [data-theme="dark"] #search-results .search-result-item:hover {{
            background-color: var(--bg-card-hover) !important;
        }}
        [data-theme="dark"] #site-search-input {{
            background-color: var(--bg-input) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] #site-search-input::placeholder {{
            color: var(--text-muted) !important;
        }}
        /* 主题切换按钮 */
        .theme-toggle-btn {{
            cursor: pointer;
            padding: 8px 12px;
            border-radius: 4px;
            transition: all 0.3s ease;
            background: transparent;
            border: none;
            font-size: 16px;
        }}
        .theme-toggle-btn:hover {{
            background-color: rgba(0,0,0,0.05);
        }}
        [data-theme="dark"] .theme-toggle-btn:hover {{
            background-color: rgba(255,255,255,0.1);
        }}
        /* 顶部导航链接 */
        .user-info-menu .nav-link {{
            transition: color 0.3s ease;
        }}
        .user-info-menu .nav-link:hover {{
            color: #337ab7 !important;
        }}
        [data-theme="dark"] .user-info-menu .nav-link:hover {{
            color: #5dade2 !important;
        }}
        /* 分类标题行：分类名 + 查看更多 */
        .category-title {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .category-title .linecons-tag {{
            margin-right: 7px;
        }}
        /* 分类名链接 */
        .category-name-link {{
            color: inherit;
            text-decoration: none;
            flex-grow: 1;
        }}
        .category-name-link:hover {{
            color: #337ab7;
            text-decoration: underline;
        }}
        /* 查看更多链接 */
        .view-more-link {{
            font-size: 13px;
            color: #337ab7;
            text-decoration: none;
            flex-shrink: 0;
            margin-left: 15px;
            white-space: nowrap;
        }}
        .view-more-link:hover {{
            text-decoration: underline;
            color: #23527c;
        }}

        /* 分页行容器 */
        .category-row {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}

        /* 左侧翻页按钮 */
        .pagination-left {{
            display: flex;
            align-items: center;
            padding-right: 15px;
            flex-shrink: 0;
            width: 40px;
        }}

        /* 右侧翻页按钮 */
        .pagination-right {{
            display: flex;
            align-items: center;
            padding-left: 15px;
            flex-shrink: 0;
            width: 40px;
        }}

        /* 内容区域 */
        .category-content {{
            flex-grow: 1;
            transition: opacity 0.3s ease;
            display: flex;
            flex-wrap: wrap;
            gap: 0;
        }}

        /* 网站项 - 响应式网格布局 */
        .site-item {{
            flex: 0 0 calc(16.666% - 15px);
            max-width: calc(16.666% - 15px);
            margin: 0 15px 15px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        /* 翻页按钮样式 */
        .pagination-left .btn,
        .pagination-right .btn {{
            padding: 8px 12px;
            min-width: 40px;
            transition: all 0.3s ease;
            border-radius: 4px;
            background: #f5f5f5;
            border: 1px solid #ddd;
        }}

        .pagination-left .btn:hover:not(:disabled),
        .pagination-right .btn:hover:not(:disabled) {{
            background: #e0e0e0;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        }}

        .pagination-left .btn:disabled,
        .pagination-right .btn:disabled {{
            opacity: 0.3;
            cursor: not-allowed;
            background: #f0f0f0;
        }}

        /* 响应式设计 */
        @media (max-width: 1400px) {{
            .site-item {{
                flex: 0 0 calc(25% - 15px);
                max-width: calc(25% - 15px);
            }}
        }}

        @media (max-width: 1200px) {{
            .site-item {{
                flex: 0 0 calc(33.333% - 15px);
                max-width: calc(33.333% - 15px);
            }}
        }}

        @media (max-width: 992px) {{
            .site-item {{
                flex: 0 0 calc(50% - 15px);
                max-width: calc(50% - 15px);
            }}
        }}

        @media (max-width: 768px) {{
            .category-row {{
                flex-direction: column;
                gap: 10px;
            }}

            .pagination-left,
            .pagination-right {{
                width: 100%;
                justify-content: center;
                padding: 0;
                height: auto;
            }}

            .pagination-left .btn,
            .pagination-right .btn {{
                width: 100%;
                min-width: auto;
            }}

            .category-content {{
                width: 100%;
            }}

            .site-item {{
                flex: 0 0 calc(50% - 15px);
                max-width: calc(50% - 15px);
            }}
        }}

        @media (max-width: 480px) {{
            .site-item {{
                flex: 0 0 100%;
                max-width: 100%;
                margin: 0 0 15px 0;
            }}

            .pagination-left .btn,
            .pagination-right .btn {{
                padding: 6px 10px;
                font-size: 12px;
            }}
        }}

        /* 网站项悬停效果 */
        .site-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
    </style>
    <script src="{asset_prefix}assets/js/jquery-1.11.1.min.js"></script>
    <script src="{asset_prefix}assets/js/lozad.js"></script>
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
                            <img src="{asset_prefix}assets/images/logo@2x.png" width="100%" alt="" />
                        </a>
                        <a href="index.html" class="logo-collapsed">
                            <img src="{asset_prefix}assets/images/logo-collapsed@2x.png" width="40" alt="" />
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
                        <a href="articles.html">
                            <i class="linecons-note"></i>
                            <span class="tooltip-blue">{articles_text}</span>
                            <span class="label label-Primary pull-right hidden-collapsed">NEW</span>
                        </a>
                    </li>
                    <li>
                        <a href="about.html">
                            <i class="linecons-heart"></i>
                            <span class="tooltip-blue">{about_text}</span>
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
                    {lang_switcher}
                    <li class="hidden-sm hidden-xs" style="margin-left: 10px;">
                        <div class="search-box-wrapper" style="position: relative;">
                            <input type="text" id="site-search-input" class="form-control" 
                                   placeholder="{search_placeholder}" 
                                   style="width: 200px; height: 32px; font-size: 13px; border-radius: 16px; padding-left: 32px;"
                                   autocomplete="off">
                            <i class="fa-search" style="position: absolute; left: 12px; top: 9px; color: #999; font-size: 13px;"></i>
                            <div id="search-results" style="display: none; position: absolute; top: 38px; left: 0; width: 350px; max-height: 400px; overflow-y: auto; background: #fff; border: 1px solid #ddd; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 9999;"></div>
                        </div>
                    </li>
                    <li class="hidden-sm hidden-xs" style="margin-left: 15px;">
                        <a href="articles.html" style="font-size: 13px; color: inherit; text-decoration: none;">
                            <i class="fa-newspaper-o" style="margin-right: 4px;"></i>{nav_articles}
                        </a>
                    </li>
                    <li class="hidden-sm hidden-xs" style="margin-left: 15px;">
                        <a href="about.html" style="font-size: 13px; color: inherit; text-decoration: none;">
                            <i class="fa-info-circle" style="margin-right: 4px;"></i>{nav_about}
                        </a>
                    </li>
                    <li class="hidden-sm hidden-xs" style="margin-left: 15px;">
                        <a href="contact.html" style="font-size: 13px; color: inherit; text-decoration: none;">
                            <i class="fa-envelope" style="margin-right: 4px;"></i>{nav_contact}
                        </a>
                    </li>
                </ul>
                <ul class="user-info-menu right-links list-inline list-unstyled">
                    <li class="hidden-sm hidden-xs">
                        <button class="theme-toggle-btn" onclick="toggleTheme()" title="切换深色/浅色模式">
                            <i class="fa-moon-o" id="theme-icon"></i>
                        </button>
                    </li>
                    <li class="hidden-sm hidden-xs" style="display: none;">
                        <a href="https://github.com/bingehack/0009tg.com" target="_blank">
                            <i class="fa-github"></i>  GitHub
                        </a>
                    </li>
                </ul>
            </nav>
            {recent_hot_html}
            {content_html}
        </div>
    </div>
    <script>
        var allSitesData = {{}};
        var currentPage = {{}};
        var categoryData = {{}};
        var itemsPerPage = 15;

        function calculateItemsPerPage() {{
            var windowWidth = $(window).width();
            if (windowWidth > 1400) {{
                return 18; // 6列 × 3行
            }} else if (windowWidth > 1200) {{
                return 12; // 4列 × 3行
            }} else if (windowWidth > 992) {{
                return 9;  // 3列 × 3行
            }} else if (windowWidth > 768) {{
                return 6;  // 2列 × 3行
            }} else if (windowWidth > 480) {{
                return 6;  // 2列 × 3行
            }} else {{
                return 3;  // 1列 × 3行
            }}
        }}

        $(window).resize(function() {{
            var newItemsPerPage = calculateItemsPerPage();
            if (newItemsPerPage !== itemsPerPage) {{
                itemsPerPage = newItemsPerPage;
                $('.category-row').each(function() {{
                    var categoryName = $(this).data('category');
                    currentPage[categoryName] = 1;
                    changePage(categoryName, 1);
                }});
            }}
        }});

        {sites_data_js}

        $(document).ready(function() {{
            var observer = lozad();

            // 初始化分类数据和当前页码
            $('.category-row').each(function() {{
                var categoryName = $(this).data('category');
                var totalItems = $(this).data('total');
                categoryData[categoryName] = totalItems;
                currentPage[categoryName] = 1;
            }});

            // 计算每页显示数量
            itemsPerPage = calculateItemsPerPage();

            // 渲染分类内容
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
                            var siteHtml = `<div class="site-item" data-index="${{i}}">
                                <div class="xe-widget xe-conversations box2 label-info" onclick="window.location.href='{asset_prefix}site/${{site.id}}.html'" data-toggle="tooltip" data-placement="bottom" title="${{site.url}}">
                                    <div class="xe-comment-entry">
                                        <a class="xe-user-img">
                                            <img src="${{site.icon}}" data-src="${{site.icon}}" class="lozad img-circle" width="40" onerror="this.onerror=null;this.src='{asset_prefix}assets/images/logos/default.png'">
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
                            var siteHtml = `<div class="site-item" data-index="${{i}}">
                                <div class="xe-widget xe-conversations box2 label-info" onclick="window.location.href='{asset_prefix}site/${{site.id}}.html'" data-toggle="tooltip" data-placement="bottom" title="${{site.url}}">
                                    <div class="xe-comment-entry">
                                        <a class="xe-user-img">
                                            <img src="${{site.icon}}" data-src="${{site.icon}}" class="lozad img-circle" width="40" onerror="this.onerror=null;this.src='{asset_prefix}assets/images/logos/default.png'">
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
                    var totalPages = Math.ceil(categoryData[categoryName] / itemsPerPage);

                    if (totalPages > 1) {{
                        leftPagination.find('.prev-page').prop('disabled', true);
                        rightPagination.find('.next-page').prop('disabled', totalPages <= 1);
                    }}
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
                    var totalPages = Math.ceil(categoryData[categoryName] / itemsPerPage);

                    contentDiv.empty();

                    if (sites.length > 0 && enablePagination) {{
                        var startIndex = (pageNum - 1) * itemsPerPage;
                        var endIndex = Math.min(startIndex + itemsPerPage, sites.length);

                        for (var i = startIndex; i < endIndex; i++) {{
                            var site = sites[i];
                            var siteHtml = `<div class="site-item" data-index="${{i}}">
                                <div class="xe-widget xe-conversations box2 label-info" onclick="window.location.href='{asset_prefix}site/${{site.id}}.html'" data-toggle="tooltip" data-placement="bottom" title="${{site.url}}">
                                    <div class="xe-comment-entry">
                                        <a class="xe-user-img">
                                            <img src="${{site.icon}}" data-src="${{site.icon}}" class="lozad img-circle" width="40" onerror="this.onerror=null;this.src='{asset_prefix}assets/images/logos/default.png'">
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

            // 分页按钮点击事件委托
            $(document).on('click', '.prev-page', function(e) {{
                e.preventDefault();
                var categoryName = $(this).data('category');
                var currentPageNum = currentPage[categoryName] || 1;
                if (currentPageNum > 1) {{
                    changePage(categoryName, currentPageNum - 1);
                }}
            }});

            $(document).on('click', '.next-page', function(e) {{
                e.preventDefault();
                var categoryName = $(this).data('category');
                var categoryRow = $('.category-row[data-category="' + categoryName + '"]');
                var sites = allSitesData[categoryName] || [];
                var totalPages = Math.ceil(categoryData[categoryName] / itemsPerPage);
                var currentPageNum = currentPage[categoryName] || 1;
                if (currentPageNum < totalPages) {{
                    changePage(categoryName, currentPageNum + 1);
                }}
            }});
        }});

        // ========== 站内搜索功能 ==========
        var allSitesFlat = [];
        // 把所有分类的站点合并成扁平数组
        for (var catName in allSitesData) {{
            var sites = allSitesData[catName] || [];
            for (var i = 0; i < sites.length; i++) {{
                allSitesFlat.push({{
                    name: sites[i].name,
                    url: sites[i].url,
                    description: sites[i].description || '',
                    icon: sites[i].icon || '',
                    category: catName
                }});
            }}
        }}

        var searchInput = document.getElementById('site-search-input');
        var searchResults = document.getElementById('search-results');
        var searchTimer = null;

        if (searchInput && searchResults) {{
            searchInput.addEventListener('input', function() {{
                clearTimeout(searchTimer);
                var query = this.value.trim().toLowerCase();
                if (query.length < 2) {{
                    searchResults.style.display = 'none';
                    searchResults.innerHTML = '';
                    return;
                }}
                // 防抖
                searchTimer = setTimeout(function() {{
                    performSearch(query);
                }}, 200);
            }});

            // 按Enter跳转到第一个结果
            searchInput.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter') {{
                    e.preventDefault();
                    var firstLink = searchResults.querySelector('.search-result-item a');
                    if (firstLink) {{
                        window.open(firstLink.getAttribute('href'), '_blank');
                        searchResults.style.display = 'none';
                    }}
                }}
                if (e.key === 'Escape') {{
                    searchResults.style.display = 'none';
                    searchInput.blur();
                }}
            }});

            // 点击页面其他地方关闭搜索结果
            document.addEventListener('click', function(e) {{
                if (!e.target.closest('.search-box-wrapper')) {{
                    searchResults.style.display = 'none';
                }}
            }});
        }}

        function performSearch(query) {{
            var results = [];
            var queryLower = query.toLowerCase();

            for (var i = 0; i < allSitesFlat.length; i++) {{
                var site = allSitesFlat[i];
                var nameMatch = site.name.toLowerCase().indexOf(queryLower) !== -1;
                var descMatch = site.description.toLowerCase().indexOf(queryLower) !== -1;
                var urlMatch = site.url.toLowerCase().indexOf(queryLower) !== -1;
                var catMatch = site.category.toLowerCase().indexOf(queryLower) !== -1;

                if (nameMatch || descMatch || urlMatch || catMatch) {{
                    // 计算匹配分数，名称匹配权重最高
                    var score = 0;
                    if (nameMatch) score += 10;
                    if (catMatch) score += 5;
                    if (descMatch) score += 3;
                    if (urlMatch) score += 1;
                    results.push({{ site: site, score: score, nameMatch: nameMatch }});
                }}
            }}

            // 按分数排序
            results.sort(function(a, b) {{ return b.score - a.score; }});

            // 最多显示20个结果
            results = results.slice(0, 20);

            if (results.length === 0) {{
                searchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">{search_no_result}</div>';
            }} else {{
                var countText = '{search_result_count}'.replace('{{count}}', results.length);
                var html = '<div style="padding: 8px 15px; font-size: 12px; color: #999; border-bottom: 1px solid #f0f0f0;">' + countText + '</div>';
                for (var j = 0; j < results.length; j++) {{
                    var s = results[j].site;
                    var detailUrl = '{asset_prefix}site/' + s.id + '.html';
                    html += '<div class="search-result-item" style="padding: 10px 15px; border-bottom: 1px solid #f5f5f5; cursor: pointer;" onmouseover="this.style.background=\\'#f9f9f9\\'" onmouseout="this.style.background=\\'#fff\\'">' +
                        '<a href="' + detailUrl + '" style="text-decoration: none; color: inherit; display: block;">' +
                        '<div style="display: flex; align-items: center;">' +
                        '<img src="' + s.icon + '" width="24" height="24" style="border-radius: 50%; margin-right: 10px; flex-shrink: 0;" onerror="this.src=\\'{asset_prefix}assets/images/logos/default.png\\'">' +
                        '<div style="flex-grow: 1; min-width: 0;">' +
                        '<div style="font-size: 14px; font-weight: 600; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">' + highlightText(s.name, query) + '</div>' +
                        '<div style="font-size: 12px; color: #999; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">' + (s.description ? s.description.substring(0, 60) : s.url) + '</div>' +
                        '</div>' +
                        '<span style="font-size: 11px; color: #337ab7; background: #e8f4fd; padding: 2px 8px; border-radius: 10px; margin-left: 10px; flex-shrink: 0;">' + s.category + '</span>' +
                        '</div>' +
                        '</a>' +
                        '</div>';
                }}
                searchResults.innerHTML = html;
            }}
            searchResults.style.display = 'block';
        }}

        function highlightText(text, query) {{
            if (!query) return text;
            var regex = new RegExp('(' + query.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
            return text.replace(regex, '<span style="color: #337ab7; font-weight: 700;">$1</span>');
        }}

        // ========== 深色模式主题切换 ==========
        function initTheme() {{
            var savedTheme = localStorage.getItem('theme');
            if (savedTheme) {{
                document.documentElement.setAttribute('data-theme', savedTheme);
                updateThemeIcon(savedTheme);
            }} else {{
                // 跟随系统偏好
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
                    document.documentElement.setAttribute('data-theme', 'dark');
                    updateThemeIcon('dark');
                }}
            }}
        }}

        function toggleTheme() {{
            var currentTheme = document.documentElement.getAttribute('data-theme');
            var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        }}

        function updateThemeIcon(theme) {{
            var icon = document.getElementById('theme-icon');
            if (icon) {{
                if (theme === 'dark') {{
                    icon.className = 'fa-sun-o';
                    icon.parentElement.title = '切换到浅色模式';
                }} else {{
                    icon.className = 'fa-moon-o';
                    icon.parentElement.title = '切换到深色模式';
                }}
            }}
        }}

        // 页面加载时初始化主题
        initTheme();

        // 监听系统主题变化
        if (window.matchMedia) {{
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {{
                if (!localStorage.getItem('theme')) {{
                    if (e.matches) {{
                        document.documentElement.setAttribute('data-theme', 'dark');
                        updateThemeIcon('dark');
                    }} else {{
                        document.documentElement.removeAttribute('data-theme');
                        updateThemeIcon('light');
                    }}
                }}
            }});
        }}
    </script>
    <!-- Bottom Scripts -->
    <script src="{asset_prefix}assets/js/bootstrap.min.js"></script>
    <script src="{asset_prefix}assets/js/TweenMax.min.js"></script>
    <script src="{asset_prefix}assets/js/resizeable.js"></script>
    <script src="{asset_prefix}assets/js/joinable.js"></script>
    <script src="{asset_prefix}assets/js/xenon-api.js"></script>
    <script src="{asset_prefix}assets/js/xenon-toggles.js"></script>
    <!-- JavaScripts initializations and stuff -->
    <script src="{asset_prefix}assets/js/xenon-custom.js"></script>
    {footer_html}
    {back_to_top_html}
</body>

</html>
'''

    # 保存到对应语言目录
    output_dir = os.path.join(project_root, lang)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'index.html')

    # 备份
    if os.path.exists(output_path):
        backup_path = output_path + '.backup'
        shutil.copy2(output_path, backup_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"生成完成！文件：{lang}/index.html ({len(html)} bytes)")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='生成导航站HTML（支持中英文）')
    parser.add_argument('--lang', choices=['cn', 'en', 'all'], default='all',
                        help='生成语言版本（默认all）')
    args = parser.parse_args()

    print("=" * 60)
    print("生成导航站HTML（中英文双语）")
    print("=" * 60)

    if args.lang in ('cn', 'all'):
        print()
        generate_html('cn')

    if args.lang in ('en', 'all'):
        print()
        generate_html('en')

    print()
    print("=" * 60)
    print("全部生成完成！")
    print("  - cn/index.html (中文)")
    print("  - en/index.html (英文)")
    print("=" * 60)


if __name__ == '__main__':
    main()
