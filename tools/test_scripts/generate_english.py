#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英文版生成脚本

用途：
    将中文版HTML文件翻译为英文版本。

功能概述：
    1. 读取中文版HTML文件
    2. 使用预定义的翻译映射表替换中文内容
    3. 修改HTML语言属性为en
    4. 修复资源路径（en目录下的相对路径）
    5. 更新语言切换菜单

使用方法：
    python generate_english.py

主要特性：
    - 支持完整的分类名称翻译
    - 自动修复资源路径
    - 更新语言切换菜单状态
    - 保持HTML结构和样式不变
"""

import json
import re

def generate_english_version():
    """生成英文版本"""
    
    # 读取中文版HTML文件
    print("读取中文版HTML文件...")
    with open('index.html', 'r', encoding='utf-8') as f:
        zh_html = f.read()
    
    # 英文翻译映射
    translations = {
        # 页面标题和元信息
        '009tg下海导航 - Invisible Man': '009tg Navigation - Invisible Man',
        '009tg下海导航,网址导航,上网导航,网址大全,网址目录,创业工具,副业赚钱,投资理财,跨境电商,营销工具,AI工具,社交媒体,独立站,广告投放': '009tg Navigation,website navigation,internet navigation,website directory,entrepreneurial tools,side hustle,investment and wealth management,cross-border e-commerce,marketing tools,AI tools,social media,independent sites,advertising',
        '009tg下海导航致力于打造国内最好的互联网上优质网站网址大全，收录了全网好用强大的网站网址和软件包括创业、副业、投资、跨境电商、营销工具、AI工具、社交媒体、独立站、广告投放、生活、休闲、办公、工具、资源等超全面的网址和职业技巧内容，让您的上网体验更便捷更放心，努力成为全民级人人都在用的网址导航。': '009tg Navigation is committed to creating the best high-quality website directory on the Chinese internet, collecting powerful websites and software from the entire internet including entrepreneurship,side hustles,investment,cross-border e-commerce,marketing tools,AI tools,social media,independent sites,advertising,lifestyle,leisure,office,tools,resources and other comprehensive URLs and professional skills content,making your internet experience more convenient and reassuring,striving to become a national-level website navigation used by everyone.',
        
        # 分类名称
        '下海推荐': 'Recommended',
        'AI工具': 'AI Tools',
        '跨境资讯': 'Cross-border News',
        '跨境推广': 'Cross-border Promotion',
        '社媒资源': 'Social Media Resources',
        '全球网络': 'Global Network',
        '全球接码': 'Global SMS',
        '数字货币': 'Cryptocurrency',
        '全球支付': 'Global Payment',
        'Facebook': 'Facebook',
        'Google': 'Google',
        '广告工具': 'Ad Tools',
        '指纹浏览器': 'Fingerprint Browsers',
        '全球APP下载': 'Global App Download',
        '内容制作': 'Content Creation',
        '技术交流': 'Tech Discussion',
        '引流工具': 'Traffic Tools',
        '跨境电商': 'Cross-border E-commerce',
        '跨境服务': 'Cross-border Services',
        '实用工具': 'Practical Tools',
        '常用工具': 'Common Tools',
        '推荐工具': 'Recommended Tools',
        '常用网址': 'Common URLs',
        '效率工具': 'Efficiency Tools',
        '短链生成工具': 'Short Link Tools',
        '指纹检测': 'Fingerprint Detection',
        'SCRM工具': 'SCRM Tools',
        '筛号工具': 'Number Screening Tools',
        'AI常用工具': 'AI Common Tools',
        'AI办公工具': 'AI Office Tools',
        'AI写作工具': 'AI Writing Tools',
        'AI视频工具': 'AI Video Tools',
        'AI设计工具': 'AI Design Tools',
        'AI编程工具': 'AI Programming Tools',
        '全球新闻': 'Global News',
        '中国论坛': 'Chinese Forums',
        '全球论坛': 'Global Forums',
        'Affliate联盟': 'Affiliate Programs',
        '社交媒体': 'Social Media',
        '社交营销': 'Social Marketing',
        '网红营销': 'Influencer Marketing',
        'EDM营销': 'EDM Marketing',
        '账号购买': 'Account Purchase',
        '涨粉平台': 'Follower Growth Platforms',
        '全球VPS': 'Global VPS',
        '中国VPS': 'Chinese VPS',
        '全球IP代理': 'Global IP Proxy',
        '域名注册': 'Domain Registration',
        '2FA短信验证码发送': '2FA SMS Verification',
        '短信接码': 'SMS Receiving',
        '虚拟邮箱': 'Virtual Email',
        '区块链媒体': 'Blockchain Media',
        '财经新闻': 'Financial News',
        '市场数据': 'Market Data',
        'NFT工具': 'NFT Tools',
        '交易所': 'Exchanges',
        '钱包': 'Wallets',
        '跨境支付': 'Cross-border Payment',
        'FB常用工具': 'FB Common Tools',
        'FB申诉链接': 'FB Appeal Links',
        'FB官方资料': 'FB Official Resources',
        'FB广告工具': 'FB Advertising Tools',
        'Google常用': 'Google Common',
        '谷歌插件': 'Google Plugins',
        '关键词工具': 'Keyword Tools',
        'SEO工具': 'SEO Tools',
        '广告监测': 'Ad Monitoring',
        '追踪系统': 'Tracking Systems',
        'Cloak工具': 'Cloaking Tools',
        '检测优化': 'Detection & Optimization',
        '社交app': 'Social Apps',
        '电商app': 'E-commerce Apps',
        '常用app': 'Common Apps',
        'Lander制作': 'Lander Creation',
        '文案工具': 'Copywriting Tools',
        '素材编辑': 'Material Editing',
        '图库网站': 'Image Libraries',
        'Logo设计': 'Logo Design',
        '视频下载': 'Video Download',
        '软件开发': 'Software Development',
        '逆向安全': 'Reverse Engineering',
        '主机交流': 'Hosting Discussion',
        '脚本工具': 'Script Tools',
        '云手机': 'Cloud Phones',
        '模拟器': 'Emulators',
        '新机工具': 'New Device Tools',
        '电商平台': 'E-commerce Platforms',
        '独立站': 'Independent Sites',
        '选品分析': 'Product Selection Analysis',
        'Deals平台': 'Deals Platforms',
        '广告代理': 'Ad Agencies',
        '常用ERP': 'Common ERP',
        '物流货代': 'Logistics & Freight',
        '货源网站': 'Source Websites',
    }
    
    # 替换HTML中的中文内容
    print("替换中文内容为英文...")
    en_html = zh_html
    
    # 替换页面标题和元信息
    for zh, en in translations.items():
        en_html = en_html.replace(zh, en)
    
    # 修改HTML语言属性
    en_html = en_html.replace('<html lang="zh">', '<html lang="en">')
    
    # 修复资源路径 - en目录下的文件需要使用相对路径
    en_html = en_html.replace('href="assets/', 'href="../assets/')
    en_html = en_html.replace('src="assets/', 'src="../assets/')
    
    # 修复JavaScript数据中的图标路径
    en_html = en_html.replace('"icon": "assets/', '"icon": "../assets/')
    
    # 修复语言切换菜单 - 英文版本应该默认显示English
    # 使用字符串查找方法来匹配完整的language-switcher li标签
    start_tag = '<li class="dropdown hover-line language-switcher">'
    start_pos = en_html.find(start_tag)
    
    if start_pos != -1:
        # 从start_pos开始，找到对应的结束</li>
        # 需要找到language-switcher li标签的结束位置
        # 这个li标签内部包含一个ul，ul内部包含多个li
        # 所以我们需要找到第一个</ul>，然后找到它后面的</li>
        temp_pos = start_pos + len(start_tag)
        
        # 找到第一个</ul>
        ul_end_pos = en_html.find('</ul>', temp_pos)
        if ul_end_pos != -1:
            # 找到</ul>后面的</li>
            li_end_pos = en_html.find('</li>', ul_end_pos)
            if li_end_pos != -1:
                old_menu = en_html[start_pos:li_end_pos + 5]  # +5 是为了包含</li>
                
                new_menu = '''<li class="dropdown hover-line language-switcher">
                        <a href="../index.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="../assets/images/flags/flag-us.png" alt="flag-us" /> English
                        </a>
                        <ul class="dropdown-menu languages">
                            <li class="active">
                                <a href="../index.html">
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
                
                en_html = en_html.replace(old_menu, new_menu, 1)  # 只替换第一个匹配
                print("语言切换菜单已更新")
            else:
                print("警告：未找到language-switcher的结束</li>")
        else:
            print("警告：未找到language-switcher内部的</ul>")
    else:
        print("警告：未找到语言切换菜单")
    
    # 修复redirect.html链接
    print("修复redirect.html链接...")
    en_html = en_html.replace("window.open('redirect.html", "window.open('../redirect.html")
    
    # 保存英文版本
    print("保存英文版本...")
    with open('en/index.html', 'w', encoding='utf-8') as f:
        f.write(en_html)
    
    print("英文版本生成完成！文件：en/index.html")

if __name__ == '__main__':
    generate_english_version()
