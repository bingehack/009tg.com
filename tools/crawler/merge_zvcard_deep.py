#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zvcard深度抓取数据清洗、自动分类、合并脚本
"""

import json
import re
from urllib.parse import urlparse
from collections import Counter

# ========== 配置 ==========

# favorites slug -> 分类名映射
FAVORITES_SLUG_MAP = {
    'huanjing': '网络环境',
    'jiema': '接码平台',
    'yunfw': '云服务',
    'qiye': '企业服务',
    'datafx': '数据分析',
    'medium': '媒体资讯',
    'zhsoft': '中文软件',
}

# zvcard分类 -> 我们的分类ID 映射规则（关键词匹配）
CATEGORY_RULES = [
    # 网络/代理
    (['代理', 'proxy', 'ip', '网络环境', '住宅', '动态ip', '静态ip'], 30),  # 全球网络
    # 接码
    (['接码', '短信', 'sms', '验证码', '虚拟号码'], 35),  # 全球接码
    # 云服务
    (['云服务', '云服务器', 'vps', '主机', '服务器', 'cdn', '云存储'], 30),  # 全球网络
    # 支付
    (['支付', '收款', '钱包', 'payment', 'paypal', 'stripe', '信用卡', '虚拟卡', 'visa', 'mastercard'], 46),  # 全球支付
    # 数字货币
    (['数字货币', '加密货币', '比特币', 'eth', '区块链', '交易所', 'wallet', 'crypto'], 39),  # 数字货币
    # 数据分析
    (['数据分析', '数据服务', 'analytics', '大数据', '统计', 'tracking', '监测'], 10),  # AI工具（先放AI工具，后续可调整）
    # 广告工具
    (['广告', 'ad', 'advertising', '投放', 'spy', '广告工具'], 58),  # 广告工具
    # SEO
    (['seo', '搜索引擎优化', '关键词', '排名'], 79),  # 引流工具
    # 推广/引流
    (['推广', '引流', '营销', 'marketing', '推广工具', '变现'], 79),  # 引流工具
    # 选品
    (['选品', '产品', 'product', '选品工具'], 84),  # 跨境电商
    # 独立站/SaaS
    (['独立站', 'saas', '建站', 'shopify', '独立站工具'], 84),  # 跨境电商
    # 外包/产品开发
    (['外包', '产品开发', '开发', '外包服务', 'freelance'], 89),  # 跨境服务
    # 本地化
    (['本地化', '翻译', 'translation', '语言本地化', 'i18n'], 68),  # 内容制作
    # 云通讯/语音
    (['云通讯', '语音', 'voip', '电话', '语音通讯', '国际短信'], 30),  # 全球网络
    # 企业服务
    (['企业服务', '企业', 'erp', 'crm', '办公', '协作'], 89),  # 跨境服务
    # 媒体资讯
    (['媒体', '资讯', '新闻', 'media', '博客', '论坛'], 17),  # 跨境资讯
    # 中文软件
    (['中文软件', '软件', '工具', '下载'], 10),  # AI工具（先放AI工具）
    # AI工具
    (['ai', '人工智能', 'gpt', 'chatgpt', '机器学习', '深度学习'], 10),  # AI工具
    # 社媒
    (['社交', '社媒', 'facebook', 'instagram', 'tiktok', 'twitter', 'youtube', 'linkedin'], 27),  # 社媒资源
    # 内容制作
    (['内容', '设计', '视频', '图片', '剪辑', '设计工具', '内容制作'], 68),  # 内容制作
    # 跨境电商
    (['电商', 'ecommerce', '亚马逊', 'amazon', '速卖通', 'shopee', 'lazada'], 84),  # 跨境电商
    # 指纹浏览器
    (['指纹', '浏览器', 'anti-detect', 'multilogin', '指纹浏览器'], 63),  # 指纹浏览器
]

# 默认分类ID
DEFAULT_CATEGORY_ID = 89  # 跨境服务

# ========== 函数 ==========

def clean_sites(sites):
    """清洗站点数据"""
    cleaned = []
    removed_internal = 0
    removed_invalid = 0
    
    for site in sites:
        url = site.get('url', '').strip()
        name = site.get('name', '').strip()
        
        # 过滤内部链接
        if 'zvcard.com' in url:
            removed_internal += 1
            continue
        
        # 过滤无效URL
        if not url or not url.startswith('http'):
            removed_invalid += 1
            continue
        
        # 过滤无效名称
        if not name:
            removed_invalid += 1
            continue
        
        # 修复名称格式（去除多余空格）
        name = re.sub(r'\s+', ' ', name).strip()
        
        # 提取域名
        try:
            domain = urlparse(url).netloc.lower()
        except:
            domain = ''
        
        site['name'] = name
        site['url'] = url
        site['domain'] = domain
        cleaned.append(site)
    
    print(f'清洗完成: 保留 {len(cleaned)}, 过滤内部链接 {removed_internal}, 过滤无效 {removed_invalid}')
    return cleaned

def fix_favorites_categories(sites):
    """修复favorites分类的名称（从slug推断）"""
    # 由于抓取时分类名都是"more+"，我们需要根据站点内容重新分类
    # 这里先标记为favorites，后续通过关键词匹配分类
    for site in sites:
        if site['category'] == 'more+':
            site['category'] = 'favorites_unknown'
    return sites

def auto_categorize(sites):
    """自动分类映射"""
    categorized = []
    uncategorized = []
    cat_counter = Counter()
    
    for site in sites:
        name = site.get('name', '').lower()
        desc = site.get('description', '').lower()
        url = site.get('url', '').lower()
        domain = site.get('domain', '').lower()
        zvcard_cat = site.get('category', '').lower()
        
        # 组合所有文本用于匹配
        text = f'{name} {desc} {url} {domain} {zvcard_cat}'
        
        # 匹配分类规则
        matched_cat = None
        for keywords, cat_id in CATEGORY_RULES:
            for kw in keywords:
                if kw.lower() in text:
                    matched_cat = cat_id
                    break
            if matched_cat:
                break
        
        if matched_cat:
            site['target_category_id'] = matched_cat
            cat_counter[matched_cat] += 1
            categorized.append(site)
        else:
            site['target_category_id'] = DEFAULT_CATEGORY_ID
            uncategorized.append(site)
            cat_counter[DEFAULT_CATEGORY_ID] += 1
    
    print(f'\n自动分类完成:')
    print(f'  已分类: {len(categorized)}')
    print(f'  未分类(默认跨境服务): {len(uncategorized)}')
    
    return categorized + uncategorized, cat_counter

def load_main_data():
    """加载主数据"""
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_existing_domains(main_data):
    """获取主数据中已有的域名集合"""
    domains = set()
    for group in main_data.get('groups', []):
        for site in group.get('sites', []):
            url = site.get('url', '')
            try:
                domain = urlparse(url).netloc.lower()
                if domain:
                    domains.add(domain)
            except:
                pass
    return domains

def merge_to_main(sites, main_data):
    """合并新站点到主数据"""
    existing_domains = get_existing_domains(main_data)
    
    # 构建分类ID -> group映射
    group_map = {}
    for group in main_data.get('groups', []):
        group_map[group['id']] = group
    
    # 找最大站点ID
    max_id = 0
    for group in main_data.get('groups', []):
        for site in group.get('sites', []):
            if site.get('id', 0) > max_id:
                max_id = site['id']
    
    new_sites = []
    duplicate_count = 0
    
    for site in sites:
        domain = site.get('domain', '')
        
        # 去重（按域名）
        if domain in existing_domains:
            duplicate_count += 1
            continue
        
        # 检查目标分类是否存在
        cat_id = site.get('target_category_id', DEFAULT_CATEGORY_ID)
        if cat_id not in group_map:
            cat_id = DEFAULT_CATEGORY_ID
        
        # 找该分类下的最大order_num
        group = group_map[cat_id]
        max_order = 0
        for s in group.get('sites', []):
            if s.get('order_num', 0) > max_order:
                max_order = s['order_num']
        
        max_id += 1
        max_order += 1
        
        new_site = {
            'id': max_id,
            'group_id': cat_id,
            'name': site['name'],
            'url': site['url'],
            'icon': '',
            'description': site.get('description', '')[:100],
            'description_en': '',
            'notes': '',
            'order_num': max_order,
            'is_public': True,
            'created_at': '2026-09-08',
            'updated_at': '2026-09-08',
        }
        
        group['sites'].append(new_site)
        new_sites.append(new_site)
        existing_domains.add(domain)
    
    print(f'\n合并完成:')
    print(f'  新增站点: {len(new_sites)}')
    print(f'  重复跳过: {duplicate_count}')
    
    return main_data, new_sites

def main():
    print('=' * 60)
    print('zvcard深度抓取数据清洗、自动分类、合并')
    print('=' * 60)
    
    # 1. 加载抓取数据
    with open('raw/zvcard深度抓取.json', 'r', encoding='utf-8') as f:
        crawl_data = json.load(f)
    
    sites = crawl_data['sites']
    print(f'\n加载抓取数据: {len(sites)} 个站点')
    
    # 2. 清洗数据
    print('\n--- 步骤1: 清洗数据 ---')
    sites = clean_sites(sites)
    
    # 3. 修复favorites分类
    print('\n--- 步骤2: 修复favorites分类 ---')
    sites = fix_favorites_categories(sites)
    
    # 4. 自动分类
    print('\n--- 步骤3: 自动分类映射 ---')
    sites, cat_counter = auto_categorize(sites)
    
    # 打印分类分布
    print('\n分类分布:')
    # 加载分类名映射
    with open('完整版导航.json', 'r', encoding='utf-8') as f:
        main_data_tmp = json.load(f)
    cat_name_map = {g['id']: g['name'] for g in main_data_tmp['groups']}
    
    for cat_id, count in cat_counter.most_common():
        cat_name = cat_name_map.get(cat_id, f'未知({cat_id})')
        print(f'  {cat_name}({cat_id}): {count}')
    
    # 5. 加载主数据并合并
    print('\n--- 步骤4: 合并到主数据 ---')
    main_data = load_main_data()
    main_data, new_sites = merge_to_main(sites, main_data)
    
    # 6. 保存主数据
    with open('完整版导航.json', 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    print(f'\n主数据已保存: 完整版导航.json')
    
    # 7. 保存新增站点列表
    with open('raw/zvcard深度抓取_新增站点.json', 'w', encoding='utf-8') as f:
        json.dump(new_sites, f, ensure_ascii=False, indent=2)
    print(f'新增站点列表已保存: raw/zvcard深度抓取_新增站点.json')
    
    # 8. 统计
    total_sites = sum(len(g['sites']) for g in main_data['groups'])
    print(f'\n' + '=' * 60)
    print(f'合并完成！')
    print(f'  新增站点: {len(new_sites)}')
    print(f'  总站点数: {total_sites}')
    print(f'=' * 60)
    
    # 打印前20个新增站点
    print('\n新增站点预览（前20个）:')
    for i, site in enumerate(new_sites[:20], 1):
        cat_name = cat_name_map.get(site['group_id'], '未知')
        print(f'  {i}. [{cat_name}] {site["name"]} -> {site["url"]}')

if __name__ == '__main__':
    main()
