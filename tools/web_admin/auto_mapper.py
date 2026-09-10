#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动分类映射模块（优化版）
功能：根据站点名称、描述、原分类名称，自动推荐映射到现有分类
优化：从现有数据自动学习关键词、利用站点描述信息、父子分类联合匹配、置信度阈值60%
"""

import json
import os
import re
from collections import defaultdict, Counter

# 项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 分类关键词映射表（手动维护，用于精确匹配）
CATEGORY_KEYWORDS = {
    # AI工具大类
    'AI常用工具': ['ai工具', 'ai导航', '人工智能', 'ai集合', 'ai大全', 'ai助手', 'chatgpt', 'gpt', '大模型', 'ai工具箱', 'ai工具集'],
    'AI对话': ['ai对话', '聊天机器人', 'ai聊天', '对话机器人', '智能对话', 'ai问答', 'chatbot', '大模型对话', 'ai聊天助手'],
    'AI写作工具': ['ai写作', '文案生成', '文章生成', '写作助手', 'ai文案', '内容生成', 'ai写作工具', '智能写作', 'ai文章', '写作工具', 'ai论文', '论文写作', '文案工具', 'ai文案生成'],
    'AI图像工具': ['ai绘图', 'ai画图', '图像生成', '图片生成', 'ai绘画', '文生图', 'ai图像', 'ai图片', 'ai作图', 'ai插画', 'ai设计图', 'ai生成图片', 'ai绘画工具', 'stable diffusion', 'midjourney', '文生图工具'],
    'AI视频工具': ['ai视频', '视频生成', '文生视频', 'ai剪辑', '视频创作', '数字人', 'ai视频生成', 'ai视频工具', 'ai数字人', 'ai剪辑工具', '视频ai', 'ai短视频', 'ai视频制作'],
    'AI音频': ['ai音频', '语音合成', '文字转语音', 'tts', 'ai配音', '语音克隆', 'ai语音', 'ai声音', '语音合成工具', 'ai音乐', '音乐生成', 'ai音效', 'ai变声', '配音工具'],
    'AI设计工具': ['ai设计', '设计工具', '平面设计', 'ui设计', 'logo设计', '海报设计', 'ai设计工具', '智能设计', 'ai平面设计', 'ai海报', 'ai logo', 'ai排版', '设计ai'],
    'AI编程工具': ['ai编程', '代码生成', '编程助手', 'copilot', '代码补全', 'ai开发', 'ai编程工具', '智能编程', 'ai代码', '代码ai', 'ai写代码', '编程ai', 'ai开发工具', 'ai编程助手'],
    'AI学习资源': ['ai学习', 'ai教程', '人工智能教程', 'ai课程', 'prompt', '提示词', 'ai学习资源', 'ai入门', 'ai培训', 'ai教育', '学习ai', 'ai知识库', 'ai教程网'],
    'AI搜索': ['ai搜索', '智能搜索', 'ai搜索引擎', '语义搜索', 'ai搜索工具', '智能搜索引擎', 'ai检索', 'ai搜索助手'],
    'AI翻译': ['ai翻译', '智能翻译', '文档翻译', '翻译工具', 'ai翻译工具', '智能翻译工具', 'ai文档翻译', '翻译ai', 'ai翻译器'],
    'AI内容检测': ['ai检测', '内容检测', 'ai识别', '查重', '原创检测', 'ai内容检测', 'ai检测工具', '内容检测工具', 'ai查重', 'ai识别工具', '原创度检测'],
    'AI Agent智能体': ['agent', '智能体', 'ai agent', '自动化代理', 'ai智能体', 'agent平台', '智能体平台', 'ai自动化', 'agent工具'],
    'AI开发平台': ['ai平台', '开发平台', '模型平台', 'api平台', '大模型平台', 'ai开发平台', '模型服务', 'ai模型平台', '大模型服务', 'ai api', '模型api'],
    'AI办公工具': ['ai办公', '智能办公', 'ai ppt', 'ai表格', 'ai文档', 'ai办公工具', '智能办公工具', 'ai office', 'ai演示', 'ai幻灯片', 'ai excel', 'ai word', '办公ai'],
    'AI教育': ['ai教育', '智能教育', 'ai学习', 'ai课程', 'ai家教', 'ai教育工具', '智能教育平台', 'ai辅导', 'ai老师', '教育ai'],

    # 跨境服务大类
    '跨境支付': ['跨境支付', '国际支付', '海外支付', '支付网关', '全球支付', '收单', '收款', '支付平台', '国际收款', '跨境收款', '第三方支付', '支付工具', '收款工具', '跨境结算', '国际结算'],
    '全球接码': ['接码', '虚拟号', '短信验证', '接码平台', 'sms', '验证码平台', '接码工具', '虚拟手机号', '短信接码', '接码服务', '临时手机号', '短信接收', '验证码接收'],
    '全球网络': ['代理ip', '住宅代理', '海外ip', '全球ip', '网络代理', 'ip代理', '代理服务', 'ip服务', '住宅ip', '动态ip', '静态ip', '海外代理', '全球代理', 'ip工具'],
    '全球VPS': ['vps', '云服务器', '海外服务器', '虚拟主机', '云主机', '服务器', 'vps服务器', '海外vps', '云服务器推荐', 'vps推荐', '独立服务器', '虚拟服务器'],
    '全球邮箱': ['海外邮箱', '临时邮箱', '企业邮箱', '邮箱服务', '邮箱', '临时邮', '一次性邮箱', '国外邮箱', '邮箱工具', '邮件服务'],
    '全球域名': ['域名注册', '海外域名', '域名服务', 'dns', '域名', '域名查询', '域名购买', '域名管理', '域名解析', '域名工具'],
    '指纹浏览器': ['指纹浏览器', '防关联', '多账号', '浏览器环境', '指纹检测', '指纹', '防关联浏览器', '多账号浏览器', '跨境浏览器', '指纹工具'],
    '账号购买': ['账号购买', '买号', '账号出售', '老号', '账号交易', '账号平台', '买账号', '账号出售平台', '老号购买'],
    '企业服务': ['企业服务', 'saas', '企业工具', '办公软件', '协作工具', '企业管理', '企业软件', '企业办公', '团队协作', '企业解决方案'],

    # 社媒资源大类
    '社媒资源': ['社媒', '社交媒体', '社交平台', '社交工具', '社交资源', '社交媒体工具', '社媒工具'],
    '社交营销': ['社媒营销', '社交营销', '网红营销', 'kol营销', 'influencer', '社交媒体营销', '社媒运营', '网红营销工具', 'kol工具', '社媒推广', '社交推广'],
    '社交app': ['社交app', '聊天app', '社交软件', '即时通讯', '社交应用', '聊天软件', '社交平台app', '通讯app'],
    'EDM营销': ['邮件营销', 'edm', '邮件群发', 'newsletter', '邮件营销工具', 'edm营销', '邮件推广', '邮件工具', '邮件群发工具'],
    '广告代理': ['广告代理', 'fb代理', 'google代理', '广告开户', '广告代理商', 'facebook代理', '谷歌代理', '广告投放代理', '海外广告代理'],
    '广告监测': ['广告监测', '广告分析', '广告spy', '竞品分析', '广告监测工具', '广告分析工具', '广告情报', '竞品监测', '广告spy工具'],
    '内容制作': ['内容制作', '视频制作', '短视频', '剪辑工具', '内容创作', '视频剪辑', '短视频制作', '内容工具', '创作工具', '视频工具'],
    '素材编辑': ['素材编辑', '图片编辑', '视频编辑', '修图', '素材工具', '编辑工具', '图片处理', '视频处理', '修图工具', '素材网站'],

    # 电商平台大类
    '电商平台': ['电商', '购物平台', '网购', '商城', '电商平台', '购物网站', '网上购物', '电商网站', '购物商城'],
    '独立站': ['独立站', 'shopify', '自建站', '跨境电商', '独立站建设', 'shopify建站', '独立站工具', '跨境独立站'],
    '选品工具': ['选品', '商品分析', '竞品分析', '选品工具', '选品软件', '商品选品', '电商选品', '选品平台'],
    'ERP系统': ['erp', '店铺管理', '订单管理', '库存管理', 'erp系统', '电商erp', '店铺管理系统', '订单管理系统', '库存管理系统'],

    # 工具资源大类
    '常用工具': ['常用工具', '实用工具', '在线工具', '效率工具', '工具集合', '工具箱', '工具大全', '实用工具集合', '在线工具集合'],
    '效率工具': ['效率', '办公', '生产力', 'todo', '任务管理', '效率工具', '办公工具', '生产力工具', '任务管理工具', '待办工具', '时间管理'],
    '图库网站': ['图库', '图片素材', '壁纸', '图标', '素材网站', '图片网站', '图库网站', '素材库', '图片库', '图标库', '壁纸网站'],
    '视频下载': ['视频下载', 'youtube下载', '在线下载', '下载工具', '视频下载工具', '下载器', '视频下载器', '在线视频下载'],
    '脚本工具': ['脚本', '油猴', 'tampermonkey', '浏览器插件', '扩展', '脚本工具', '油猴脚本', '浏览器扩展', '插件工具', 'chrome插件'],
    '软件开发': ['开发工具', '编程工具', 'ide', '代码编辑器', '软件开发', '程序员工具', '开发软件', '编程软件', '代码工具', '开发资源'],
    '站长工具': ['站长工具', 'seo工具', '网站分析', '域名查询', '站长', 'seo', '网站优化', 'seo优化', '网站工具', '站长资源'],

    # 资讯社区大类
    '中国论坛': ['论坛', '社区', '讨论区', 'bbs', '中文论坛', '国内论坛', '论坛网站', '社区网站'],
    '全球新闻': ['新闻', '资讯', '媒体', 'news', '新闻网站', '资讯网站', '新闻媒体', '国际新闻'],
    'Affliate联盟': ['affiliate', '联盟营销', 'cpa', '网赚', '联盟', '联盟平台', 'cpa联盟', '网赚平台', 'affiliate营销'],
    '教程福利': ['教程', '福利', '免费资源', '白嫖', '学习资源', '教程网站', '免费教程', '资源分享', '福利资源', '免费资源网'],

    # 技术交流大类
    '技术交流': ['技术', '编程', '开发', '技术社区', '技术论坛', '开发者社区', '技术博客', '编程社区', '开发社区'],
    '逆向安全': ['逆向', '安全', '破解', '渗透', '网络安全', '安全论坛', '逆向工程', '渗透测试', '安全工具', '信息安全'],
    '主机交流': ['主机', '服务器', 'vps交流', '运维', '主机论坛', '服务器交流', 'vps论坛', '运维社区'],

    # 全球APP下载大类
    '常用app': ['常用app', '应用推荐', '手机app', '实用app', 'app推荐', '应用集合', 'app集合', '手机应用', '常用软件'],
    '社交app': ['社交app', '聊天app', '社交软件', '即时通讯', '社交应用', '聊天软件', '社交平台app'],
    '电商app': ['电商app', '购物app', '网购app', '购物应用', '电商应用', '购物软件'],
}

# 停用词（不参与匹配）
STOP_WORDS = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '它', '他', '她', '们', '这个', '那个', '什么', '怎么', '为什么', '可以', '能够', '应该', '需要', '因为', '所以', '但是', '而且', '或者', '如果', '虽然', '然后', '接着', '最后', '首先', '其次', '再次', '此外', '另外', '同时', '一起', '共同', '互相', '彼此', '大家', '各位', '别人', '他人', '自己', '自身', '本身', '个人', '私人', '公开', '公共', '共同', '一般', '普通', '平常', '日常', '平时', '通常', '经常', '时常', '偶尔', '有时', '总是', '永远', '已经', '曾经', '刚刚', '刚才', '现在', '目前', '当前', '如今', '现在', '将来', '未来', '以后', '之前', '以前', '从前', '过去', '最近', '近来', '近期', '短期', '长期', '永久', '暂时', '临时', '偶尔', '偶然', '突然', '忽然', '渐渐', '逐渐', '慢慢', '快速', '迅速', '立刻', '马上', '立即', '即刻', '顿时', '霎时', '刹那', '瞬间', '片刻', '须臾', '不久', '很快', '即将', '将要', '快要', '就要', '正', '正在', '在', '着', '过', '了', '的', '得', '地', '啊', '呀', '哦', '哈', '嗯', '唉', '哎', '喂', '嗨', '嘿', '哦', '噢', '喔', '呵', '嘻', '嘿', '呀', '哇', '啊', '呢', '吧', '嘛', '么', '啦', '喽', '哟', '唷', '啵', '呗', '哪', '啥', '怎么', '怎样', '如何', '为何', '为什么', '啥', '嘛', '呢', '吧', '啊', '呀', '哦', '哈', '嗯', '唉', '哎', '喂', '嗨', '嘿'}

# 英文停用词
ENGLISH_STOP_WORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'it', 'its', 'i', 'you', 'he', 'she', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there', 'then', 'once', 'if', 'because', 'as', 'until', 'while', 'about', 'above', 'after', 'below', 'between', 'into', 'through', 'during', 'before', 'after', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once'}


def load_nav_data():
    """加载导航数据"""
    data_path = os.path.join(PROJECT_ROOT, '完整版导航.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_categories_with_info():
    """获取所有分类及其信息"""
    data = load_nav_data()
    groups = data.get('groups', [])
    result = []
    for g in groups:
        parent_name = ''
        if g.get('parent_id'):
            parent = next((p for p in groups if p['id'] == g['parent_id']), None)
            if parent:
                parent_name = parent.get('name', '')
        result.append({
            'id': g.get('id'),
            'name': g.get('name'),
            'parent_id': g.get('parent_id'),
            'parent_name': parent_name,
            'sites_count': len(g.get('sites', [])),
            'full_name': f"{parent_name} > {g['name']}" if parent_name else g['name']
        })
    return result


def extract_keywords(text, min_len=2, max_len=8):
    """从文本中提取关键词（中文词组+英文单词）"""
    if not text:
        return []

    keywords = []

    # 提取英文单词（长度>=3）
    english_words = re.findall(r'[a-zA-Z]{3,}', text.lower())
    for word in english_words:
        if word not in ENGLISH_STOP_WORDS and len(word) >= 3:
            keywords.append(word)

    # 提取中文词组（2-4个字）
    chinese_phrases = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
    for phrase in chinese_phrases:
        if phrase not in STOP_WORDS and len(phrase) >= 2:
            keywords.append(phrase)

    return list(set(keywords))


def learn_keywords_from_data():
    """从现有数据中学习每个分类的高频关键词"""
    data = load_nav_data()
    groups = data.get('groups', [])

    category_keywords = defaultdict(Counter)

    for g in groups:
        cat_name = g.get('name', '')
        sites = g.get('sites', [])

        for site in sites:
            # 从站点名称提取关键词
            name = site.get('name', '')
            name_keywords = extract_keywords(name)
            for kw in name_keywords:
                category_keywords[cat_name][kw] += 2  # 名称权重更高

            # 从站点描述提取关键词
            desc = site.get('description', '')
            desc_keywords = extract_keywords(desc)
            for kw in desc_keywords:
                category_keywords[cat_name][kw] += 1  # 描述权重较低

    # 只保留每个分类出现次数>=2的关键词
    learned = {}
    for cat_name, counter in category_keywords.items():
        top_keywords = [kw for kw, count in counter.most_common(30) if count >= 2]
        if top_keywords:
            learned[cat_name] = top_keywords

    return learned


# 全局缓存：从数据学习的关键词
_LEARNED_KEYWORDS = None


def get_learned_keywords():
    """获取学习到的关键词（懒加载+缓存）"""
    global _LEARNED_KEYWORDS
    if _LEARNED_KEYWORDS is None:
        try:
            _LEARNED_KEYWORDS = learn_keywords_from_data()
        except:
            _LEARNED_KEYWORDS = {}
    return _LEARNED_KEYWORDS


def calculate_similarity(text1, text2):
    """计算两个文本的相似度（基于关键词重合度）"""
    if not text1 or not text2:
        return 0

    kw1 = set(extract_keywords(text1))
    kw2 = set(extract_keywords(text2))

    if not kw1 or not kw2:
        return 0

    intersection = kw1 & kw2
    union = kw1 | kw2

    return len(intersection) / len(union) if union else 0


def auto_map_category(site_name, site_description, source_category, categories=None):
    """
    自动分类映射（优化版）
    返回：[(category_id, category_name, score), ...] 按相似度降序
    """
    if categories is None:
        categories = get_all_categories_with_info()

    # 组合文本用于匹配
    combined_text = f"{site_name} {site_description} {source_category}".lower()
    combined_keywords = set(extract_keywords(combined_text))

    # 获取学习到的关键词
    learned = get_learned_keywords()

    scores = []

    for cat in categories:
        score = 0
        cat_name = cat['name']
        parent_name = cat.get('parent_name', '')

        # 1. 手动关键词精确匹配（权重最高）
        manual_keywords = CATEGORY_KEYWORDS.get(cat_name, [])
        for kw in manual_keywords:
            if kw.lower() in combined_text:
                score += 0.4
                break

        # 2. 从数据学习的关键词匹配（权重次高）
        learned_keywords = learned.get(cat_name, [])
        matched_learned = 0
        for kw in learned_keywords[:15]:  # 只用前15个高频词
            if kw.lower() in combined_keywords:
                matched_learned += 1
        if matched_learned > 0:
            score += min(matched_learned * 0.05, 0.3)  # 最多加0.3

        # 3. 分类名称精确匹配
        if cat_name.lower() in combined_text:
            score += 0.2
        if parent_name and parent_name.lower() in combined_text:
            score += 0.1

        # 4. 原分类名称相似度
        if source_category:
            sim = calculate_similarity(source_category, cat_name)
            score += sim * 0.15

            if parent_name:
                sim_parent = calculate_similarity(source_category, parent_name)
                score += sim_parent * 0.05

        # 5. 站点名称包含分类关键词
        if site_name:
            for kw in manual_keywords[:5]:  # 只用前5个核心关键词
                if kw.lower() in site_name.lower():
                    score += 0.1
                    break

        # 6. 站点描述包含分类关键词
        if site_description:
            desc_matched = 0
            for kw in manual_keywords:
                if kw.lower() in site_description.lower():
                    desc_matched += 1
            if desc_matched > 0:
                score += min(desc_matched * 0.03, 0.15)

        if score > 0:
            scores.append({
                'category_id': cat['id'],
                'category_name': cat['name'],
                'parent_name': parent_name,
                'full_name': cat.get('full_name', cat['name']),
                'score': round(min(score, 1.0), 3)
            })

    # 按分数降序
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:5]  # 返回前5个推荐


def auto_map_all_sites(sites, categories=None):
    """
    批量自动分类映射
    返回：{source_category: [(category_id, category_name, score), ...]}
    """
    if categories is None:
        categories = get_all_categories_with_info()

    # 按原分类分组
    by_source_cat = defaultdict(list)
    for site in sites:
        src_cat = site.get('category', '未分类')
        by_source_cat[src_cat].append(site)

    result = {}
    for src_cat, cat_sites in by_source_cat.items():
        # 取该分类下前3个站点进行匹配（同分类的站点应该映射到相同目标分类）
        sample_sites = cat_sites[:3]

        # 对每个样本站点进行映射，取投票结果
        all_recommendations = []
        for site in sample_sites:
            recs = auto_map_category(
                site.get('name', ''),
                site.get('description', ''),
                src_cat,
                categories
            )
            all_recommendations.append(recs)

        # 投票：取每个样本的最佳匹配，统计出现次数
        vote_counter = Counter()
        score_sum = defaultdict(float)
        for recs in all_recommendations:
            if recs:
                best = recs[0]
                vote_counter[best['category_id']] += 1
                score_sum[best['category_id']] += best['score']

        # 按投票数和平均分排序
        sorted_votes = sorted(vote_counter.items(),
                               key=lambda x: (x[1], score_sum[x[0]]),
                               reverse=True)

        # 构建推荐列表
        recommendations = []
        for cat_id, votes in sorted_votes:
            # 找到该分类的完整信息
            cat_info = next((c for c in categories if c['id'] == cat_id), None)
            if cat_info:
                avg_score = score_sum[cat_id] / votes if votes > 0 else 0
                recommendations.append({
                    'category_id': cat_id,
                    'category_name': cat_info['name'],
                    'parent_name': cat_info.get('parent_name', ''),
                    'full_name': cat_info.get('full_name', cat_info['name']),
                    'score': round(avg_score, 3),
                    'votes': votes
                })

        best_match = recommendations[0] if recommendations else None

        result[src_cat] = {
            'sites_count': len(cat_sites),
            'recommendations': recommendations,
            'best_match': best_match
        }

    return result


if __name__ == '__main__':
    # 测试
    print("=== 自动分类映射测试（优化版）===")

    test_sites = [
        {'name': 'ChatGPT', 'description': 'AI对话助手，智能聊天机器人', 'category': 'AI工具'},
        {'name': '跨境支付平台', 'description': '国际收款，跨境结算，支付网关', 'category': '支付'},
        {'name': '接码平台', 'description': '虚拟手机号接收验证码，短信接码', 'category': '工具'},
        {'name': 'AI绘画工具', 'description': '文生图，AI绘图，图像生成', 'category': 'AI工具'},
        {'name': '短视频剪辑', 'description': '视频制作，剪辑工具，内容创作', 'category': '工具'},
    ]

    result = auto_map_all_sites(test_sites)
    for src_cat, info in result.items():
        print(f"\n原分类: {src_cat} ({info['sites_count']}个站点)")
        print("推荐映射:")
        for rec in info['recommendations'][:3]:
            vote_info = f" (投票:{rec.get('votes', 0)}/3)" if 'votes' in rec else ''
            print(f"  - {rec['full_name']}: {rec['score']*100:.0f}%{vote_info}")
