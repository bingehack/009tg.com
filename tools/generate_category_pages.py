#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分类详情页生成脚本 - 支持中英文双语

用途：
    为每个分类（一级分类和子分类）生成详情页，增加网站内容深度。

功能概述：
    1. 读取JSON数据，构建分类树
    2. 一级分类详情页：展示子分类入口 + 热门站点
    3. 子分类详情页：展示所有站点（分页，每页32个）
    4. 面包屑导航、分类描述、相关分类推荐
    5. 支持中英文双语
    6. 响应式布局（一行8个，缩小时减少列数）

使用方法：
    python tools/generate_category_pages.py
    python tools/generate_category_pages.py --lang en
    python tools/generate_category_pages.py --category-id 10

主要特性：
    - 一级分类和子分类详情页
    - 每页32个站点（8列×4行），响应式自适应
    - JS翻页功能
    - 面包屑导航
    - 分类描述（基于模板生成）
    - 相关分类推荐
    - 语言切换
    - 站点点击通过redirect.html中转
"""

import json
import os
import shutil
import argparse
from urllib.parse import urlparse

# 导入分类翻译
from generate_new_html import CATEGORY_TRANSLATION, translate_category

# ============================================================
# 分类描述模板（中英文）
# ============================================================
CATEGORY_DESCRIPTIONS = {
    '下海推荐': {
        'cn': '精选互联网上最实用的工具和网址，涵盖日常办公、效率提升、资源获取等多个领域。所有工具均经过严格筛选，确保安全可靠、实用高效，是您上网冲浪的得力助手。',
        'en': 'A curated selection of the most practical tools and websites on the internet, covering daily office work, productivity enhancement, resource acquisition and more. All tools are carefully screened to ensure safety, reliability and practical efficiency.'
    },
    'AI工具': {
        'cn': '汇聚全球最前沿的人工智能工具和平台，涵盖AI写作、图像生成、视频制作、音频处理、编程辅助等多个领域。无论您是创作者、开发者还是企业用户，都能在这里找到适合的AI工具，提升工作效率和创造力。',
        'en': 'A comprehensive collection of cutting-edge AI tools and platforms worldwide, covering AI writing, image generation, video creation, audio processing, programming assistance and more. Whether you are a creator, developer or enterprise user, you will find suitable AI tools here.'
    },
    '跨境资讯': {
        'cn': '聚焦跨境电商行业最新动态和深度资讯，涵盖全球新闻、行业论坛、专业媒体等多个信息来源。帮助跨境从业者及时掌握行业趋势、政策变化和市场动态，做出更明智的商业决策。',
        'en': 'Focus on the latest news and in-depth information in the cross-border e-commerce industry, covering global news, industry forums, professional media and more. Help cross-border practitioners stay updated on industry trends, policy changes and market dynamics.'
    },
    '跨境推广': {
        'cn': '精选海外营销和推广工具，涵盖广告联盟、SEO优化、流量交换、邮件营销等多个领域。帮助跨境卖家和营销人员高效获取海外流量，提升品牌曝光和转化率，实现业务增长。',
        'en': 'A selection of overseas marketing and promotion tools, covering ad networks, SEO optimization, traffic exchange, email marketing and more. Help cross-border sellers and marketers efficiently acquire overseas traffic and improve brand exposure.'
    },
    '社媒资源': {
        'cn': '汇集社交媒体运营必备工具和资源，涵盖内容创作、账号管理、数据分析、粉丝增长等多个方面。帮助社媒运营者提升内容质量和运营效率，在各大社交平台上获得更好的表现。',
        'en': 'A collection of essential tools and resources for social media operations, covering content creation, account management, data analysis, follower growth and more. Help social media operators improve content quality and operational efficiency.'
    },
    '全球网络': {
        'cn': '提供全球网络访问相关工具和服务，涵盖VPS、域名注册、CDN加速、DNS服务等多个领域。帮助用户构建稳定高效的网络基础设施，保障网站和应用的全球访问体验。',
        'en': 'Tools and services for global network access, covering VPS, domain registration, CDN acceleration, DNS services and more. Help users build stable and efficient network infrastructure for global access.'
    },
    '全球接码': {
        'cn': '汇集全球手机号接码和虚拟号码服务，支持多个国家和地区的手机号码接收验证码。适用于账号注册、隐私保护、业务验证等场景，帮助用户保护个人隐私和管理多个账号。',
        'en': 'A collection of global SMS verification and virtual number services, supporting phone numbers from multiple countries and regions to receive verification codes. Suitable for account registration, privacy protection and business verification.'
    },
    '数字货币': {
        'cn': '精选数字货币交易和管理工具，涵盖交易所、钱包、行情分析等多个领域。帮助加密货币投资者安全管理资产，及时掌握市场行情，做出更明智的投资决策。',
        'en': 'A selection of cryptocurrency trading and management tools, covering exchanges, wallets, market analysis and more. Help crypto investors safely manage assets and stay updated on market trends.'
    },
    '全球支付': {
        'cn': '汇集国际支付和收款工具，涵盖支付平台、收款工具、跨境转账等多个领域。帮助跨境卖家和企业用户高效处理全球收付款，降低交易成本，提升资金周转效率。',
        'en': 'A collection of international payment and collection tools, covering payment platforms, collection tools, cross-border transfers and more. Help cross-border sellers and enterprises efficiently handle global payments.'
    },
    'Facebook': {
        'cn': '专注Facebook营销和运营工具，涵盖广告投放、主页管理、粉丝增长、数据分析等多个方面。帮助营销人员在Facebook平台上高效运营，提升广告效果和粉丝 engagement。',
        'en': 'Tools focused on Facebook marketing and operations, covering advertising, page management, follower growth, data analysis and more. Help marketers efficiently operate on the Facebook platform.'
    },
    'Google': {
        'cn': '汇集Google生态相关工具和服务，涵盖搜索、广告、分析、扩展程序等多个领域。帮助用户充分利用Google的强大功能，提升工作效率和营销效果。',
        'en': 'A collection of tools and services related to the Google ecosystem, covering search, advertising, analytics, extensions and more. Help users fully leverage Google\'s powerful features.'
    },
    '广告工具': {
        'cn': '精选广告投放和优化工具，涵盖广告平台、创意制作、效果检测、数据分析等多个领域。帮助广告主和营销人员提升广告投放效果，降低获客成本，实现更高的ROI。',
        'en': 'A selection of ad placement and optimization tools, covering ad platforms, creative production, performance detection, data analysis and more. Help advertisers improve ad performance and reduce acquisition costs.'
    },
    '指纹浏览器': {
        'cn': '提供反检测浏览器和指纹管理工具，帮助用户管理多个账号，防止关联检测。适用于跨境电商、社媒运营、广告投放等需要多账号管理的场景，保障账号安全和业务稳定。',
        'en': 'Anti-detect browsers and fingerprint management tools to help users manage multiple accounts and prevent association detection. Suitable for cross-border e-commerce, social media operations, advertising and other multi-account scenarios.'
    },
    '全球APP下载': {
        'cn': '汇集海外常用应用下载资源，涵盖电商APP、社交APP、工具APP等多个类别。帮助用户快速找到并下载所需的海外应用，拓展全球应用生态。',
        'en': 'A collection of overseas app download resources, covering e-commerce apps, social apps, utility apps and more. Help users quickly find and download the overseas apps they need.'
    },
    '内容制作': {
        'cn': '精选内容创作和制作工具，涵盖软件开发、脚本工具、素材编辑、图库资源等多个领域。帮助创作者高效制作高质量的图文、视频、音频内容，提升创作效率和作品质量。',
        'en': 'A selection of content creation and production tools, covering software development, script tools, media editing, image libraries and more. Help creators efficiently produce high-quality content.'
    },
    '技术交流': {
        'cn': '汇集技术交流和开发资源，涵盖技术论坛、开发社区、编程资源等多个领域。帮助开发者和技术爱好者学习交流、解决问题、提升技术能力。',
        'en': 'A collection of technical communication and development resources, covering tech forums, developer communities, programming resources and more. Help developers learn, communicate and solve problems.'
    },
    '引流工具': {
        'cn': '精选流量获取和转化工具，涵盖引流平台、群发工具、自动化营销等多个领域。帮助营销人员高效获取精准流量，提升转化率和客户留存，实现业务增长。',
        'en': 'A selection of traffic acquisition and conversion tools, covering traffic platforms, bulk messaging, automated marketing and more. Help marketers efficiently acquire targeted traffic and improve conversion rates.'
    },
    '跨境电商': {
        'cn': '汇集跨境电商平台和运营工具，涵盖电商平台、选品工具、ERP系统等多个领域。帮助跨境卖家高效管理店铺，优化运营流程，提升销售业绩和利润空间。',
        'en': 'A collection of cross-border e-commerce platforms and operation tools, covering e-commerce platforms, product research, ERP systems and more. Help cross-border sellers efficiently manage stores and improve sales performance.'
    },
    '跨境服务': {
        'cn': '提供跨境电商配套服务，涵盖物流、仓储、代运营等多个领域。帮助跨境卖家解决后端服务问题，专注于产品和销售，提升整体运营效率和客户满意度。',
        'en': 'Supporting services for cross-border e-commerce, covering logistics, warehousing, agency operations and more. Help cross-border sellers solve back-end service issues and focus on products and sales.'
    },
}

DEFAULT_CATEGORY_DESC = {
    'cn': '精选该分类下的优质工具和资源，所有站点均经过严格筛选，确保安全可靠、实用高效。帮助用户快速找到所需工具，提升工作效率和使用体验。',
    'en': 'A curated selection of quality tools and resources in this category, all carefully screened to ensure safety, reliability and practical efficiency. Help users quickly find the tools they need.'
}


def get_category_description(category_name, lang='cn'):
    """获取分类描述"""
    if category_name in CATEGORY_DESCRIPTIONS:
        return CATEGORY_DESCRIPTIONS[category_name][lang]
    return DEFAULT_CATEGORY_DESC[lang]


def generate_category_intro(category_name, parent_name, total_sites, sample_sites, lang='cn'):
    """动态生成200-300字的分类导读文字
    基于基础描述 + 站点数量 + 热门站点 + 使用建议
    """
    base_desc = get_category_description(category_name, lang)
    
    # 取前3-5个热门站点名称
    hot_names = []
    for s in sample_sites[:5]:
        name = s.get('name', '')
        if name and len(name) < 30:
            hot_names.append(name)
        if len(hot_names) >= 4:
            break
    
    if lang == 'cn':
        # 中文导读
        parts = [base_desc]
        
        # 站点数量说明
        if total_sites > 0:
            parts.append(f'本分类目前收录了{total_sites}个优质站点，')
            if hot_names:
                parts.append(f'包括{"、".join(hot_names)}等知名工具，')
            parts.append('覆盖了该领域的主流需求和应用场景。')
        
        # 父分类关联
        if parent_name and parent_name != category_name:
            parts.append(f'作为{parent_name}领域的重要组成部分，')
        
        # 使用建议
        parts.append('建议您根据自身需求选择合适的工具，多数工具提供免费试用或基础免费版本，可先体验后再决定是否升级付费。')
        parts.append('如发现失效链接或有更好的工具推荐，欢迎通过联系我们页面告知，我们会及时更新维护。')
        
        intro = ''.join(parts)
        # 确保长度在200-350字之间
        if len(intro) < 200:
            intro += '我们致力于为用户提供最全面、最实用的工具导航服务，持续更新和优化收录内容，帮助用户提升工作效率和使用体验。'
    else:
        # 英文导读
        parts = [base_desc]
        
        if total_sites > 0:
            parts.append(f' This category currently features {total_sites} quality sites,')
            if hot_names:
                parts.append(f' including well-known tools such as {", ".join(hot_names)},')
            parts.append(' covering the mainstream needs and application scenarios in this field.')
        
        if parent_name and parent_name != category_name:
            parts.append(f' As an important part of the {parent_name} field,')
        
        parts.append(' We recommend choosing the right tool based on your needs. Most tools offer free trials or basic free versions, so you can try before upgrading.')
        parts.append(' If you find broken links or have better tool recommendations, please let us know through the Contact Us page, and we will update promptly.')
        
        intro = ''.join(parts)
        if len(intro) < 200:
            intro += ' We are committed to providing users with the most comprehensive and practical tool navigation service, continuously updating and optimizing our content to help users improve productivity and user experience.'
    
    return intro


# ============================================================
# 分类功能特点（中英文）
# ============================================================
CATEGORY_FEATURES = {
    'AI工具': {
        'cn': ['支持多种AI模型', '在线使用无需安装', '免费试用额度', 'API接口支持', '持续更新迭代'],
        'en': ['Supports multiple AI models', 'Online use, no installation', 'Free trial quota', 'API interface support', 'Continuous updates']
    },
    '跨境资讯': {
        'cn': ['实时行业动态', '多语种信息源', '深度分析报告', '政策法规解读', '市场趋势预测'],
        'en': ['Real-time industry news', 'Multi-language sources', 'In-depth analysis', 'Policy interpretation', 'Market trend forecast']
    },
    '跨境推广': {
        'cn': ['多平台广告投放', '精准受众定位', '实时数据监控', 'ROI优化工具', '自动化营销'],
        'en': ['Multi-platform advertising', 'Precise audience targeting', 'Real-time monitoring', 'ROI optimization', 'Automated marketing']
    },
    '社媒资源': {
        'cn': ['多平台账号管理', '内容批量发布', '数据分析报表', '粉丝增长工具', '竞品监控'],
        'en': ['Multi-platform management', 'Bulk content publishing', 'Data analytics', 'Follower growth tools', 'Competitor monitoring']
    },
    '全球网络': {
        'cn': ['全球节点覆盖', '高带宽低延迟', '弹性扩容', 'DDoS防护', '7x24技术支持'],
        'en': ['Global node coverage', 'High bandwidth low latency', 'Elastic scaling', 'DDoS protection', '24/7 technical support']
    },
    '全球接码': {
        'cn': ['支持200+国家', '实时接收验证码', '号码隐私保护', '批量号码管理', 'API接口对接'],
        'en': ['200+ countries supported', 'Real-time SMS reception', 'Number privacy protection', 'Bulk number management', 'API integration']
    },
    '数字货币': {
        'cn': ['支持主流币种', '实时行情数据', '安全钱包存储', '多交易所对接', '量化交易工具'],
        'en': ['Major coins supported', 'Real-time market data', 'Secure wallet storage', 'Multi-exchange integration', 'Quant trading tools']
    },
    '全球支付': {
        'cn': ['支持多币种结算', '低手续费率', '快速到账', '防欺诈系统', '多平台收款'],
        'en': ['Multi-currency settlement', 'Low transaction fees', 'Fast payout', 'Anti-fraud system', 'Multi-platform collection']
    },
    '指纹浏览器': {
        'cn': ['浏览器指纹隔离', '多账号防关联', '代理IP集成', '团队协作管理', '自动化操作'],
        'en': ['Browser fingerprint isolation', 'Multi-account anti-association', 'Proxy IP integration', 'Team collaboration', 'Automated operations']
    },
    '广告工具': {
        'cn': ['多广告平台支持', '创意素材库', 'A/B测试功能', '转化追踪', '智能出价优化'],
        'en': ['Multi-ad platform support', 'Creative asset library', 'A/B testing', 'Conversion tracking', 'Smart bid optimization']
    },
    '内容制作': {
        'cn': ['多格式支持', '批量处理', '模板素材库', '云端协作', '高质量输出'],
        'en': ['Multi-format support', 'Batch processing', 'Template library', 'Cloud collaboration', 'High-quality output']
    },
    '引流工具': {
        'cn': ['多渠道引流', '自动化群发', '精准用户触达', '转化漏斗分析', '客户管理系统'],
        'en': ['Multi-channel traffic', 'Automated messaging', 'Precise user reach', 'Conversion funnel analysis', 'CRM system']
    },
    '跨境电商': {
        'cn': ['多平台店铺管理', '智能选品分析', '库存同步', '订单自动化', '利润核算'],
        'en': ['Multi-platform store management', 'Smart product research', 'Inventory sync', 'Order automation', 'Profit calculation']
    },
    '跨境服务': {
        'cn': ['全球物流网络', '仓储配送一体', '专业代运营', '合规咨询服务', '售后保障'],
        'en': ['Global logistics network', 'Warehousing & delivery', 'Professional agency ops', 'Compliance consulting', 'After-sales support']
    },
}

DEFAULT_FEATURES = {
    'cn': ['精选优质工具', '安全可靠验证', '持续更新维护', '分类清晰易找', '免费使用为主'],
    'en': ['Curated quality tools', 'Safe and verified', 'Continuous updates', 'Clear categorization', 'Mostly free to use']
}


def get_features(category_name, lang='cn'):
    """获取分类功能特点"""
    if category_name in CATEGORY_FEATURES:
        return CATEGORY_FEATURES[category_name][lang]
    return DEFAULT_FEATURES[lang]


# ============================================================
# 分类适用场景（中英文）
# ============================================================
CATEGORY_SCENARIOS = {
    'AI工具': {
        'cn': '适用于内容创作者、开发者、企业用户等需要提升工作效率的人群。可用于文章写作、图片设计、视频制作、代码编写、数据分析等多种场景，帮助用户快速完成创意工作和重复性任务。',
        'en': 'Suitable for content creators, developers, and enterprise users who need to improve productivity. Can be used for article writing, image design, video creation, coding, data analysis and more, helping users quickly complete creative work and repetitive tasks.'
    },
    '跨境资讯': {
        'cn': '适用于跨境电商卖家、外贸从业者、海外营销人员等需要及时了解行业动态的人群。可用于市场调研、竞品分析、政策研究、趋势预判等场景，帮助用户做出更明智的商业决策。',
        'en': 'Suitable for cross-border sellers, foreign trade practitioners, and overseas marketers who need timely industry updates. Can be used for market research, competitor analysis, policy research, trend forecasting and more.'
    },
    '跨境推广': {
        'cn': '适用于跨境电商卖家、独立站运营者、海外营销人员等需要获取海外流量的人群。可用于广告投放、SEO优化、社媒营销、邮件营销、联盟营销等场景，帮助用户提升品牌曝光和转化率。',
        'en': 'Suitable for cross-border sellers, independent site operators, and overseas marketers who need overseas traffic. Can be used for advertising, SEO, social media marketing, email marketing, affiliate marketing and more.'
    },
    '指纹浏览器': {
        'cn': '适用于跨境电商卖家、社媒运营者、广告投放人员等需要管理多个账号的人群。可用于多账号登录、防关联检测、团队协作、自动化操作等场景，保障账号安全和业务稳定运行。',
        'en': 'Suitable for cross-border sellers, social media operators, and advertisers who need to manage multiple accounts. Can be used for multi-account login, anti-association detection, team collaboration, automated operations and more.'
    },
    '跨境电商': {
        'cn': '适用于跨境电商卖家、外贸企业、供应链管理者等需要高效运营店铺的人群。可用于店铺管理、选品分析、库存管理、订单处理、财务核算等场景，帮助用户提升运营效率和利润空间。',
        'en': 'Suitable for cross-border sellers, foreign trade enterprises, and supply chain managers who need efficient store operations. Can be used for store management, product research, inventory management, order processing, financial accounting and more.'
    },
}

DEFAULT_SCENARIOS = {
    'cn': '适用于需要该类工具和资源的各类用户，包括个人开发者、企业运营者、自由职业者等。可用于日常工作、学习研究、项目开发、业务运营等多种场景，帮助用户提升效率、降低成本、快速达成目标。',
    'en': 'Suitable for various users who need these tools and resources, including individual developers, enterprise operators, freelancers and more. Can be used for daily work, learning and research, project development, business operations and more, helping users improve efficiency, reduce costs, and quickly achieve goals.'
}


def get_scenarios(category_name, lang='cn'):
    """获取分类适用场景"""
    if category_name in CATEGORY_SCENARIOS:
        return CATEGORY_SCENARIOS[category_name][lang]
    return DEFAULT_SCENARIOS[lang]


def get_domain(url):
    """提取域名"""
    try:
        return urlparse(url).netloc.lower()
    except:
        return ''


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

    return root_groups, group_dict


def generate_site_card(site, favicon_mapping, asset_prefix, lang='cn'):
    """生成单个站点卡片HTML"""
    site_name = site.get('name', '')
    site_url = site.get('url', '#')
    if lang == 'en':
        site_description = site.get('description_en') or site.get('description', '')
    else:
        site_description = site.get('description', '')

    domain = get_domain(site_url)
    site_icon = f'{asset_prefix}assets/images/logos/default.png'
    if domain in favicon_mapping:
        site_icon = asset_prefix + favicon_mapping[domain]

    return f'''
                    <div class="site-item">
                        <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('{asset_prefix}redirect.html?url={site_url}&name={site_name}', '_blank')" data-toggle="tooltip" data-placement="bottom" title="{site_url}">
                            <div class="xe-comment-entry">
                                <a class="xe-user-img">
                                    <img src="{site_icon}" class="lozad img-circle" width="40" alt="{site_name}">
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


def generate_sites_js(sites, favicon_mapping, asset_prefix, lang='cn'):
    """生成站点数据JS（用于翻页）"""
    sites_data = []
    for site in sites:
        site_name = site.get('name', '')
        site_url = site.get('url', '#')
        if lang == 'en':
            site_description = site.get('description_en') or site.get('description', '')
        else:
            site_description = site.get('description', '')
        domain = get_domain(site_url)
        site_icon = f'{asset_prefix}assets/images/logos/default.png'
        if domain in favicon_mapping:
            site_icon = asset_prefix + favicon_mapping[domain]
        sites_data.append({
            'name': site_name,
            'url': site_url,
            'description': site_description,
            'icon': site_icon
        })
    return json.dumps(sites_data, ensure_ascii=False)


def generate_category_page(category, parent_category, children, all_sites_in_category,
                           related_categories, favicon_mapping, lang='cn', asset_prefix='../../'):
    """生成单个分类详情页"""
    category_id = category.get('id', 0)
    category_name = category.get('name', '')
    display_name = translate_category(category_name, lang)
    is_root = parent_category is None

    # 分类描述（动态生成200-300字导读）
    parent_name = parent_category.get('name', '') if parent_category else ''
    category_desc = generate_category_intro(category_name, parent_name, len(all_sites_in_category), all_sites_in_category, lang)

    # 面包屑
    if lang == 'cn':
        html_lang = 'zh'
        home_text = '首页'
        if is_root:
            breadcrumb = f'<a href="../index.html">{home_text}</a> / <span>{display_name}</span>'
        else:
            parent_name = translate_category(parent_category.get('name', ''), lang)
            parent_id = parent_category.get('id', 0)
            breadcrumb = f'<a href="../index.html">{home_text}</a> / <a href="{parent_id}.html">{parent_name}</a> / <span>{display_name}</span>'
        sites_text = '个站点'
        sub_cats_text = '子分类'
        related_text = '相关分类'
        hot_sites_text = '热门站点'
        all_sites_text = '全部站点'
        prev_text = '上一页'
        next_text = '下一页'
        page_text = '第'
        page_of_text = '页 / 共'
        pages_text = '页'
        about_text = '关于本站'
    else:
        html_lang = 'en'
        home_text = 'Home'
        if is_root:
            breadcrumb = f'<a href="../index.html">{home_text}</a> / <span>{display_name}</span>'
        else:
            parent_name = translate_category(parent_category.get('name', ''), lang)
            parent_id = parent_category.get('id', 0)
            breadcrumb = f'<a href="../index.html">{home_text}</a> / <a href="{parent_id}.html">{parent_name}</a> / <span>{display_name}</span>'
        sites_text = 'sites'
        sub_cats_text = 'Subcategories'
        related_text = 'Related Categories'
        hot_sites_text = 'Hot Sites'
        all_sites_text = 'All Sites'
        prev_text = 'Previous'
        next_text = 'Next'
        page_text = 'Page'
        page_of_text = '/'
        pages_text = ''
        about_text = 'About Us'

    # 子分类入口（一级分类页面用）
    children_html = ''
    if children:
        for child in children:
            child_id = child.get('id', 0)
            child_name = translate_category(child.get('name', ''), lang)
            child_count = len(child.get('sites', []))
            children_html += f'''
                    <div class="col-sm-3">
                        <a href="{child_id}.html" class="category-card">
                            <div class="category-card-inner">
                                <h4>{child_name}</h4>
                                <p>{child_count} {sites_text}</p>
                            </div>
                        </a>
                    </div>'''

    # 相关分类
    related_html = ''
    if related_categories:
        for rel in related_categories:
            rel_id = rel.get('id', 0)
            rel_name = translate_category(rel.get('name', ''), lang)
            related_html += f'<a href="{rel_id}.html" class="btn btn-default btn-sm" style="margin: 3px;">{rel_name}</a>'

    # 功能特点
    features = get_features(category_name, lang)
    features_html = ''.join([f'<li class="list-group-item"><i class="fa-check-circle" style="color: #5cb85c; margin-right: 8px;"></i>{f}</li>' for f in features])

    # 适用场景
    scenarios = get_scenarios(category_name, lang)

    # 功能特点和适用场景标题
    if lang == 'cn':
        features_title = '功能特点'
        scenarios_title = '适用场景'
    else:
        features_title = 'Features'
        scenarios_title = 'Use Cases'

    # 站点数据JS
    sites_js = generate_sites_js(all_sites_in_category, favicon_mapping, asset_prefix, lang)
    total_sites = len(all_sites_in_category)

    # 语言切换
    if lang == 'cn':
        lang_switcher = f'''
                    <li class="dropdown hover-line language-switcher">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="{asset_prefix}assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                        </a>
                        <ul class="dropdown-menu languages">
                            <li><a href="../../en/category/{category_id}.html"><img src="{asset_prefix}assets/images/flags/flag-us.png" alt="flag-us" /> English</a></li>
                            <li class="active"><a href="../../cn/category/{category_id}.html"><img src="{asset_prefix}assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese</a></li>
                        </ul>
                    </li>'''
    else:
        lang_switcher = f'''
                    <li class="dropdown hover-line language-switcher">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="{asset_prefix}assets/images/flags/flag-us.png" alt="flag-us" /> English
                        </a>
                        <ul class="dropdown-menu languages">
                            <li class="active"><a href="../../en/category/{category_id}.html"><img src="{asset_prefix}assets/images/flags/flag-us.png" alt="flag-us" /> English</a></li>
                            <li><a href="../../cn/category/{category_id}.html"><img src="{asset_prefix}assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese</a></li>
                        </ul>
                    </li>'''

    # 页面标题和meta
    if lang == 'cn':
        title = f'{display_name} - 009tg下海导航'
        keywords = f'{display_name},网址导航,工具推荐,{category_name}'
        description = f'{display_name}分类下的优质工具和资源，共{total_sites}个站点。{category_desc[:100]}'
    else:
        title = f'{display_name} - 009tg Navigation'
        keywords = f'{display_name},url directory,tool recommendation,{category_name}'
        description = f'Quality tools and resources in the {display_name} category, {total_sites} sites total. {category_desc[:100]}'

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
            --border-color: #3a3f48;
            --border-card: #3a3f48;
            --link-color: #5dade2;
            --link-hover: #85c1e9;
            --shadow-card: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.5);
        }}
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
        [data-theme="dark"] .panel-body {{
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .site-item .panel,
        [data-theme="dark"] .xe-widget {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-card) !important;
            box-shadow: var(--shadow-card) !important;
        }}
        [data-theme="dark"] .site-item .panel:hover,
        [data-theme="dark"] .xe-widget:hover {{
            background-color: var(--bg-card-hover) !important;
            box-shadow: var(--shadow-card-hover) !important;
        }}
        [data-theme="dark"] .xe-user-name strong {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .xe-comment p {{
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .breadcrumb {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
        }}
        [data-theme="dark"] .breadcrumb a {{
            color: var(--link-color) !important;
        }}
        [data-theme="dark"] .breadcrumb span {{
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .category-desc {{
            background-color: var(--bg-card) !important;
            border-left-color: var(--link-color) !important;
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .category-card {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-card) !important;
        }}
        [data-theme="dark"] .category-card:hover {{
            background-color: var(--bg-card-hover) !important;
        }}
        [data-theme="dark"] .category-card h4 {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .category-card p {{
            color: var(--text-secondary) !important;
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
        [data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3,
        [data-theme="dark"] h4, [data-theme="dark"] h5, [data-theme="dark"] h6 {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .text-muted,
        [data-theme="dark"] small {{
            color: var(--text-muted) !important;
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
        .breadcrumb {{
            background: #f5f5f5;
            padding: 10px 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        .breadcrumb a {{
            color: #337ab7;
            text-decoration: none;
        }}
        .breadcrumb span {{
            color: #666;
        }}
        .category-desc {{
            background: #f9f9f9;
            border-left: 4px solid #337ab7;
            padding: 15px 20px;
            margin-bottom: 20px;
            line-height: 1.8;
            font-size: 14px;
        }}
        .category-card {{
            display: block;
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 15px;
            text-align: center;
            transition: all 0.3s ease;
            text-decoration: none;
            color: #333;
        }}
        .category-card:hover {{
            border-color: #337ab7;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-3px);
            text-decoration: none;
            color: #337ab7;
        }}
        .category-card h4 {{
            margin: 0 0 8px 0;
            font-size: 16px;
        }}
        .category-card p {{
            margin: 0;
            color: #999;
            font-size: 12px;
        }}
        .site-item {{
            flex: 0 0 calc(12.5% - 15px);
            max-width: calc(12.5% - 15px);
            margin: 0 15px 15px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .site-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .category-content {{
            display: flex;
            flex-wrap: wrap;
        }}
        .pagination-controls {{
            text-align: center;
            margin: 20px 0;
        }}
        .pagination-controls button {{
            margin: 0 5px;
        }}
        .page-info {{
            display: inline-block;
            margin: 0 15px;
            color: #666;
        }}
        @media (max-width: 1400px) {{
            .site-item {{ flex: 0 0 calc(16.666% - 15px); max-width: calc(16.666% - 15px); }}
        }}
        @media (max-width: 1200px) {{
            .site-item {{ flex: 0 0 calc(25% - 15px); max-width: calc(25% - 15px); }}
        }}
        @media (max-width: 992px) {{
            .site-item {{ flex: 0 0 calc(33.333% - 15px); max-width: calc(33.333% - 15px); }}
        }}
        @media (max-width: 768px) {{
            .site-item {{ flex: 0 0 calc(50% - 15px); max-width: calc(50% - 15px); }}
        }}
        @media (max-width: 480px) {{
            .site-item {{ flex: 0 0 100%; max-width: 100%; margin: 0 0 15px 0; }}
        }}
    </style>
    <script src="{asset_prefix}assets/js/jquery-1.11.1.min.js"></script>
    <script src="{asset_prefix}assets/js/lozad.js"></script>
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
                            <span class="title">{home_text}</span>
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
                <ul class="user-info-menu right-links list-inline list-unstyled">
                    <li class="hidden-sm hidden-xs">
                        <button class="theme-toggle-btn" onclick="toggleTheme()" title="切换深色/浅色模式">
                            <i class="fa-moon-o" id="theme-icon"></i>
                        </button>
                    </li>
                </ul>
            </nav>

            <!-- 面包屑 -->
            <div class="breadcrumb">
                {breadcrumb}
            </div>

            <!-- 分类标题和描述 -->
            <div class="row">
                <div class="col-md-12">
                    <h2 style="margin-top: 0;">{display_name} <small style="color: #999;">({total_sites} {sites_text})</small></h2>
                    <div class="category-desc">
                        {category_desc}
                    </div>
                </div>
            </div>

            <!-- 功能特点和适用场景（仅子分类或有站点的一级分类显示） -->
            {f'''
            <div class="row">
                <div class="col-md-6">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title"><i class="fa-check-circle" style="margin-right: 8px;"></i>{features_title}</h4>
                        </div>
                        <div class="panel-body" style="padding: 0;">
                            <ul class="list-group" style="margin-bottom: 0;">
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
                            <p style="font-size: 14px; line-height: 1.8; margin: 0;">{scenarios}</p>
                        </div>
                    </div>
                </div>
            </div>
            ''' if total_sites > 0 else ''}

            <!-- 子分类入口（一级分类页面） -->
            {f'''
            <div class="row">
                <div class="col-md-12">
                    <h3>{sub_cats_text}</h3>
                    <div class="row">
                        {children_html}
                    </div>
                </div>
            </div>
            ''' if children else ''}

            <!-- 相关分类 -->
            {f'''
            <div class="row">
                <div class="col-md-12">
                    <h3>{related_text}</h3>
                    <div style="margin-bottom: 20px;">
                        {related_html}
                    </div>
                </div>
            </div>
            ''' if related_html else ''}

            <!-- 站点列表（仅当有站点时显示） -->
            {f'''
            <div class="row">
                <div class="col-md-12">
                    <h3>{all_sites_text}</h3>
                    <div class="category-content" id="sites-container"></div>
                    <div class="pagination-controls">
                        <button class="btn btn-default" id="prev-page" disabled><i class="fa fa-chevron-left"></i> {prev_text}</button>
                        <span class="page-info" id="page-info"></span>
                        <button class="btn btn-default" id="next-page">{next_text} <i class="fa fa-chevron-right"></i></button>
                    </div>
                </div>
            </div>
            ''' if total_sites > 0 else ''}

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

    {f'''
    <script>
        var allSites = {sites_js};
        var currentPage = 1;
        var itemsPerPage = 32;
        var totalPages = Math.ceil(allSites.length / itemsPerPage);

        function calculateItemsPerPage() {{
            var windowWidth = $(window).width();
            if (windowWidth > 1400) return 32; // 8列 × 4行
            if (windowWidth > 1200) return 24; // 6列 × 4行
            if (windowWidth > 992) return 16;  // 4列 × 4行
            if (windowWidth > 768) return 12;  // 3列 × 4行
            return 8; // 2列 × 4行
        }}

        function renderPage(pageNum) {{
            var container = $('#sites-container');
            container.empty();
            container.css('opacity', '0.5');

            setTimeout(function() {{
                var start = (pageNum - 1) * itemsPerPage;
                var end = Math.min(start + itemsPerPage, allSites.length);

                for (var i = start; i < end; i++) {{
                    var site = allSites[i];
                    var siteHtml = '<div class="site-item">' +
                        '<div class="xe-widget xe-conversations box2 label-info" onclick="window.open(\\'' + '{asset_prefix}redirect.html?url=' + encodeURIComponent(site.url) + '&name=' + encodeURIComponent(site.name) + '\\', \\'_blank\\')" data-toggle="tooltip" data-placement="bottom" title="' + site.url + '">' +
                            '<div class="xe-comment-entry">' +
                                '<a class="xe-user-img"><img src="' + site.icon + '" class="lozad img-circle" width="40" alt="' + site.name + '"></a>' +
                                '<div class="xe-comment">' +
                                    '<a href="#" class="xe-user-name overflowClip_1"><strong>' + site.name + '</strong></a>' +
                                    '<p class="overflowClip_2">' + site.description + '</p>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>';
                    container.append(siteHtml);
                }}

                container.css('opacity', '1');
                if (typeof lozad !== 'undefined') {{
                    var observer = lozad();
                    observer.observe();
                }}
            }}, 200);

            $('#page-info').text('{page_text} ' + pageNum + ' {page_of_text} ' + totalPages + ' {pages_text}');
            $('#prev-page').prop('disabled', pageNum === 1);
            $('#next-page').prop('disabled', pageNum === totalPages);
        }}

        $(document).ready(function() {{
            itemsPerPage = calculateItemsPerPage();
            totalPages = Math.ceil(allSites.length / itemsPerPage);
            renderPage(1);

            $('#prev-page').click(function() {{
                if (currentPage > 1) {{
                    currentPage--;
                    renderPage(currentPage);
                }}
            }});

            $('#next-page').click(function() {{
                if (currentPage < totalPages) {{
                    currentPage++;
                    renderPage(currentPage);
                }}
            }});

            $(window).resize(function() {{
                var newItemsPerPage = calculateItemsPerPage();
                if (newItemsPerPage !== itemsPerPage) {{
                    itemsPerPage = newItemsPerPage;
                    totalPages = Math.ceil(allSites.length / itemsPerPage);
                    currentPage = 1;
                    renderPage(1);
                }}
            }});
        }});
    </script>
    ''' if total_sites > 0 else ''}

    <!-- 深色模式主题切换（所有页面都加载） -->
    <script>
        function initTheme() {{
            var savedTheme = localStorage.getItem('theme');
            if (savedTheme) {{
                document.documentElement.setAttribute('data-theme', savedTheme);
                updateThemeIcon(savedTheme);
            }} else {{
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
        initTheme();
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
    parser = argparse.ArgumentParser(description='生成分类详情页（支持中英文）')
    parser.add_argument('--lang', choices=['cn', 'en', 'all'], default='all', help='生成语言版本')
    parser.add_argument('--category-id', type=int, help='只生成指定ID的分类详情页')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    print("=" * 60)
    print("生成分类详情页（中英文双语）")
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

    # 构建分类树
    root_groups, group_dict = build_category_tree(data['groups'])

    # 收集所有分类（带父分类和子分类信息）
    all_categories = []
    for root in root_groups:
        all_categories.append({
            'category': root,
            'parent': None,
            'children': root.get('children', []),
            'sites': root.get('sites', []),
        })
        for child in root.get('children', []):
            all_categories.append({
                'category': child,
                'parent': root,
                'children': [],
                'sites': child.get('sites', []),
            })

    print(f"共 {len(all_categories)} 个分类（{len(root_groups)} 个一级分类，{len(all_categories)-len(root_groups)} 个子分类）")

    # 筛选要生成的分类
    if args.category_id:
        target_categories = [c for c in all_categories if c['category'].get('id') == args.category_id]
        if not target_categories:
            print(f"未找到ID为{args.category_id}的分类")
            return
    else:
        target_categories = all_categories

    generated = {'cn': 0, 'en': 0}

    for lang in ['cn', 'en']:
        if args.lang != 'all' and args.lang != lang:
            continue

        output_dir = os.path.join(project_root, lang, 'category')
        os.makedirs(output_dir, exist_ok=True)

        for cat_info in target_categories:
            category = cat_info['category']
            parent = cat_info['parent']
            children = cat_info['children']
            sites = cat_info['sites']

            category_id = category.get('id', 0)

            # 相关分类（同属一个父分类的其他分类）
            related = []
            if parent:
                for sibling in parent.get('children', []):
                    if sibling.get('id') != category_id:
                        related.append(sibling)
            else:
                # 一级分类的相关分类：其他一级分类
                for other_root in root_groups:
                    if other_root.get('id') != category_id:
                        related.append(other_root)

            # 生成页面
            html = generate_category_page(
                category, parent, children, sites, related, favicon_mapping, lang
            )

            output_path = os.path.join(output_dir, f'{category_id}.html')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            generated[lang] += 1

        print(f"  {lang}: 生成 {generated[lang]} 个分类详情页 -> {lang}/category/")

    print()
    print("=" * 60)
    print("生成完成！")
    print(f"  中文: cn/category/ ({generated['cn']} 个页面)")
    print(f"  英文: en/category/ ({generated['en']} 个页面)")
    print("=" * 60)


if __name__ == '__main__':
    main()
