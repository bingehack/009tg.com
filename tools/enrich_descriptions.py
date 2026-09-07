#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量丰富站点描述脚本

功能：
1. 统计描述长度分布
2. 对于中文描述 < 30字的站点，用分类模板扩展中文描述
3. 为所有站点生成英文描述（description_en字段）
4. 备份原始数据
5. 输出统计报告

使用方法：
    python tools/enrich_descriptions.py
    python tools/enrich_descriptions.py --dry-run  # 只预览不修改
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime
from urllib.parse import urlparse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_ROOT, '完整版导航.json')

# ============================================================
# 分类描述模板（中文）
# 每个模板包含多个句式，随机选择避免重复
# ============================================================
CATEGORY_TEMPLATES_CN = {
    'AI常用工具': [
        '{name}是一款实用的AI工具，提供{feature}功能，帮助用户提升工作效率，适用于日常办公和学习场景。',
        '{name}是一个基于人工智能的在线工具平台，支持{feature}，操作简单易用，无需安装即可使用。',
        '{name}为用户提供便捷的AI服务，涵盖{feature}等功能，是日常工作和学习的得力助手。',
    ],
    'AI写作工具': [
        '{name}是一款基于人工智能的写作辅助工具，支持文章生成、内容润色、文案创作等功能，适用于自媒体运营、营销文案、学术写作等场景。',
        '{name}利用AI技术帮助用户高效创作内容，支持多种文体和语言，能够快速生成高质量的文章和文案。',
        '{name}是一个智能写作平台，提供AI写作、内容优化、标题生成等功能，帮助创作者提升写作效率和质量。',
    ],
    'AI图像工具': [
        '{name}是一款AI图像生成和编辑工具，支持文生图、图生图、图像编辑等功能，适用于设计创作、营销素材、社交媒体配图等场景。',
        '{name}利用人工智能技术实现智能图像处理，支持多种风格和效果，帮助用户快速创作专业级图像内容。',
        '{name}是一个在线AI绘画平台，提供文字生成图片、图片编辑、风格转换等功能，无需专业设计技能即可创作精美图像。',
    ],
    'AI视频工具': [
        '{name}是一款AI视频创作工具，支持文本生成视频、视频编辑、智能剪辑等功能，适用于短视频创作、营销视频、教育培训等场景。',
        '{name}利用人工智能技术简化视频制作流程，支持自动剪辑、字幕生成、特效添加等功能，帮助用户快速产出专业视频内容。',
        '{name}是一个智能视频创作平台，提供AI生成视频、视频增强、内容创作等功能，降低视频制作门槛，提升创作效率。',
    ],
    'AI音频工具': [
        '{name}是一款AI音频处理工具，支持语音合成、音频编辑、声音转换等功能，适用于播客制作、有声书、配音等场景。',
        '{name}利用人工智能技术实现智能音频处理，支持文字转语音、语音克隆、音频增强等功能，帮助用户创作高质量音频内容。',
        '{name}是一个在线AI音频平台，提供语音合成、音乐生成、音频编辑等功能，操作简单，无需专业音频技能。',
    ],
    'AI办公工具': [
        '{name}是一款AI办公辅助工具，支持文档处理、数据分析、会议纪要等功能，帮助用户提升办公效率，适用于企业和个人办公场景。',
        '{name}利用人工智能技术优化办公流程，支持智能写作、数据处理、任务管理等功能，是现代办公的得力助手。',
        '{name}是一个智能办公平台，提供AI文档、智能表格、会议助手等功能，帮助团队提升协作效率和工作质量。',
    ],
    'AI编程工具': [
        '{name}是一款AI编程辅助工具，支持代码生成、代码补全、bug修复等功能，适用于软件开发、学习编程、技术研究等场景。',
        '{name}利用人工智能技术提升编程效率，支持多种编程语言和框架，能够智能理解代码上下文并提供精准建议。',
        '{name}是一个智能编程平台，提供AI代码助手、代码审查、技术问答等功能，帮助开发者更快更好地完成编程任务。',
    ],
    'AI设计工具': [
        '{name}是一款AI设计辅助工具，支持智能排版、配色推荐、模板生成等功能，适用于UI设计、平面设计、营销素材等场景。',
        '{name}利用人工智能技术简化设计流程，支持自动生成设计稿、智能抠图、风格转换等功能，帮助用户快速产出专业设计作品。',
        '{name}是一个智能设计平台，提供AI生成设计、模板编辑、协作设计等功能，降低设计门槛，提升设计效率。',
    ],
    'AI翻译工具': [
        '{name}是一款AI翻译工具，支持多语言互译、文档翻译、实时翻译等功能，适用于跨境交流、学术研究、旅行出行等场景。',
        '{name}利用人工智能技术实现精准翻译，支持多种语言和领域术语，翻译质量接近人工水平，帮助用户跨越语言障碍。',
        '{name}是一个智能翻译平台，提供文本翻译、语音翻译、图片翻译等功能，支持离线使用，是出国旅行和国际交流的必备工具。',
    ],
    'AI搜索工具': [
        '{name}是一款AI搜索引擎，支持智能问答、深度研究、信息整合等功能，适用于学术研究、市场调研、学习求知等场景。',
        '{name}利用人工智能技术优化搜索体验，能够理解复杂问题并提供结构化答案，帮助用户快速获取准确信息。',
        '{name}是一个智能搜索平台，提供AI问答、文献检索、知识图谱等功能，让信息检索更高效、更精准。',
    ],
    'AI学习资源': [
        '{name}是一个AI学习资源平台，提供在线课程、学习工具、知识问答等功能，适用于技能提升、考试备考、兴趣学习等场景。',
        '{name}利用人工智能技术个性化学习体验，支持智能推荐、学习路径规划、进度跟踪等功能，帮助用户高效学习。',
        '{name}是一个在线学习平台，涵盖编程、设计、商业等多个领域，提供优质课程和学习资源，助力个人成长和职业发展。',
    ],
    'AI开发平台': [
        '{name}是一个AI开发平台，提供模型训练、API接口、应用开发等功能，适用于AI应用开发、技术研究、企业智能化转型等场景。',
        '{name}为开发者提供一站式AI开发服务，支持多种框架和模型，降低AI应用开发门槛，加速AI技术落地。',
        '{name}是一个人工智能开放平台，提供语音、视觉、自然语言处理等AI能力，帮助开发者快速构建智能应用。',
    ],
    'AI内容检测': [
        '{name}是一款AI内容检测工具，支持AI文本检测、抄袭检测、内容质量评估等功能，适用于学术写作、内容创作、教育评估等场景。',
        '{name}利用人工智能技术识别AI生成内容，支持多种检测维度和报告输出，帮助用户确保内容原创性和质量。',
        '{name}是一个智能内容检测平台，提供AI检测、查重、润色等功能，帮助创作者和教育机构提升内容质量和学术诚信。',
    ],
    'AI Agent智能体': [
        '{name}是一个AI Agent智能体平台，支持自定义智能体、自动化任务、多智能体协作等功能，适用于工作流自动化、客户服务、数据分析等场景。',
        '{name}利用人工智能技术构建智能代理，能够自主理解任务、规划步骤、执行操作，帮助用户自动化处理复杂工作。',
        '{name}是一个智能体开发和应用平台，提供无代码构建、模板市场、API集成等功能，让每个人都能创建自己的AI助手。',
    ],
    'AI资讯': [
        '{name}是一个AI资讯平台，提供人工智能行业新闻、技术动态、产品评测等内容，适用于AI从业者、技术爱好者、投资者等人群。',
        '{name}专注于人工智能领域的信息传播，涵盖大模型、机器学习、计算机视觉等前沿技术，帮助用户及时了解AI行业发展趋势。',
        '{name}是一个人工智能垂直媒体，提供深度报道、行业分析、专家观点等内容，是AI从业者获取行业资讯的重要渠道。',
    ],
    '常用工具': [
        '{name}是一款实用的在线工具，提供{feature}功能，操作简单，无需安装，适用于日常工作和生活中的各种需求。',
        '{name}为用户提供便捷的在线服务，支持{feature}等功能，界面简洁，使用方便，是日常办公的好帮手。',
        '{name}是一个多功能在线工具平台，涵盖{feature}等实用功能，帮助用户高效处理日常事务，提升工作效率。',
    ],
    '常用网址': [
        '{name}是一个常用的网站平台，提供{feature}服务，用户量大，口碑良好，是互联网用户经常访问的实用网站。',
        '{name}为用户提供便捷的在线服务，涵盖{feature}等功能，界面友好，操作简单，适合各类用户使用。',
        '{name}是一个知名的在线平台，提供{feature}等服务，功能完善，体验优秀，是日常生活和工作中不可或缺的工具网站。',
    ],
    '素材编辑': [
        '{name}是一个素材编辑平台，提供图片编辑、视频剪辑、音频处理等功能，适用于内容创作、营销素材、社交媒体等场景。',
        '{name}为创作者提供专业的素材处理工具，支持多种格式和效果，帮助用户快速制作高质量的多媒体内容。',
        '{name}是一个在线素材编辑平台，操作简单，功能强大，无需专业技能即可创作精美的图片、视频和音频内容。',
    ],
    '图库网站': [
        '{name}是一个图库网站，提供大量高质量的图片素材，包括摄影照片、插画、矢量图等，适用于设计创作、营销素材、网页设计等场景。',
        '{name}为用户提供丰富的图片资源，支持多种分类和搜索方式，图片质量高，下载方便，是设计师和创作者的重要素材来源。',
        '{name}是一个专业的图片素材平台，涵盖商业摄影、艺术插画、图标素材等，支持免费和付费下载，满足不同用户的需求。',
    ],
}

# 默认模板（未匹配到分类时使用）
DEFAULT_TEMPLATES_CN = [
    '{name}是一个实用的在线平台，提供多种便捷功能，帮助用户提升效率，适用于日常工作和学习场景。',
    '{name}为用户提供优质的在线服务，功能完善，体验优秀，是互联网上值得收藏的实用网站。',
    '{name}是一个专业的在线工具平台，操作简单，使用方便，无需安装即可享受便捷的在线服务。',
]

# ============================================================
# 分类描述模板（英文）
# ============================================================
CATEGORY_TEMPLATES_EN = {
    'AI常用工具': [
        '{name} is a practical AI tool that provides {feature} capabilities, helping users improve work efficiency for daily office and learning scenarios.',
        '{name} is an AI-powered online tool platform supporting {feature}, simple and easy to use, no installation required.',
        '{name} provides convenient AI services covering {feature} and more, making it a reliable assistant for daily work and learning.',
    ],
    'AI写作工具': [
        '{name} is an AI-powered writing assistant that supports article generation, content polishing, and copy creation, ideal for content creators, marketers, and academic writing.',
        '{name} uses AI technology to help users create content efficiently, supporting multiple writing styles and languages to generate high-quality articles quickly.',
        '{name} is an intelligent writing platform offering AI writing, content optimization, and title generation to help creators improve writing efficiency and quality.',
    ],
    'AI图像工具': [
        '{name} is an AI image generation and editing tool supporting text-to-image, image-to-image, and image editing for design, marketing, and social media content creation.',
        '{name} uses AI technology for intelligent image processing, supporting multiple styles and effects to help users create professional-grade images quickly.',
        '{name} is an online AI painting platform offering text-to-image, image editing, and style conversion, allowing anyone to create stunning images without design skills.',
    ],
    'AI视频工具': [
        '{name} is an AI video creation tool supporting text-to-video, video editing, and smart clipping for short video creation, marketing videos, and educational content.',
        '{name} uses AI technology to simplify video production with auto-clipping, subtitle generation, and effects, helping users produce professional video content quickly.',
        '{name} is an intelligent video creation platform offering AI video generation, enhancement, and content creation to lower the barrier of video production.',
    ],
    'AI音频工具': [
        '{name} is an AI audio processing tool supporting speech synthesis, audio editing, and voice conversion for podcasting, audiobooks, and voice-over production.',
        '{name} uses AI technology for intelligent audio processing with text-to-speech, voice cloning, and audio enhancement to help users create high-quality audio content.',
        '{name} is an online AI audio platform offering speech synthesis, music generation, and audio editing with a simple interface, no professional audio skills required.',
    ],
    'AI办公工具': [
        '{name} is an AI office assistant supporting document processing, data analysis, and meeting summaries to improve office efficiency for businesses and individuals.',
        '{name} uses AI technology to optimize office workflows with smart writing, data processing, and task management, making it a reliable modern office assistant.',
        '{name} is an intelligent office platform offering AI documents, smart spreadsheets, and meeting assistants to help teams improve collaboration efficiency and work quality.',
    ],
    'AI编程工具': [
        '{name} is an AI programming assistant supporting code generation, code completion, and bug fixing for software development, learning to code, and technical research.',
        '{name} uses AI technology to improve programming efficiency, supporting multiple languages and frameworks with intelligent code context understanding and precise suggestions.',
        '{name} is an intelligent programming platform offering AI code assistance, code review, and technical Q&A to help developers complete programming tasks faster and better.',
    ],
    'AI设计工具': [
        '{name} is an AI design assistant supporting smart layout, color recommendations, and template generation for UI design, graphic design, and marketing materials.',
        '{name} uses AI technology to simplify design workflows with auto-generated designs, smart background removal, and style conversion for professional design output.',
        '{name} is an intelligent design platform offering AI-generated designs, template editing, and collaborative design to lower the design barrier and improve efficiency.',
    ],
    'AI翻译工具': [
        '{name} is an AI translation tool supporting multi-language translation, document translation, and real-time translation for cross-border communication, academic research, and travel.',
        '{name} uses AI technology for accurate translation supporting multiple languages and domain terminology, with near-human translation quality to help users overcome language barriers.',
        '{name} is an intelligent translation platform offering text translation, voice translation, and image translation with offline support, essential for travel and international communication.',
    ],
    'AI搜索工具': [
        '{name} is an AI search engine supporting intelligent Q&A, deep research, and information integration for academic research, market analysis, and learning.',
        '{name} uses AI technology to optimize search experience, understanding complex questions and providing structured answers to help users get accurate information quickly.',
        '{name} is an intelligent search platform offering AI Q&A, literature search, and knowledge graphs for more efficient and precise information retrieval.',
    ],
    'AI学习资源': [
        '{name} is an AI learning resource platform offering online courses, learning tools, and knowledge Q&A for skill improvement, exam preparation, and interest learning.',
        '{name} uses AI technology to personalize learning experiences with smart recommendations, learning path planning, and progress tracking to help users learn efficiently.',
        '{name} is an online learning platform covering programming, design, business, and more, providing quality courses and resources for personal growth and career development.',
    ],
    'AI开发平台': [
        '{name} is an AI development platform offering model training, API interfaces, and application development for AI app development, technical research, and enterprise AI transformation.',
        '{name} provides one-stop AI development services for developers, supporting multiple frameworks and models to lower the barrier of AI application development and accelerate AI deployment.',
        '{name} is an AI open platform offering speech, vision, and NLP capabilities to help developers quickly build intelligent applications.',
    ],
    'AI内容检测': [
        '{name} is an AI content detection tool supporting AI text detection, plagiarism checking, and content quality assessment for academic writing, content creation, and education.',
        '{name} uses AI technology to identify AI-generated content with multiple detection dimensions and report output to help users ensure content originality and quality.',
        '{name} is an intelligent content detection platform offering AI detection, plagiarism checking, and text polishing to help creators and educators improve content quality and academic integrity.',
    ],
    'AI Agent智能体': [
        '{name} is an AI Agent platform supporting custom agents, task automation, and multi-agent collaboration for workflow automation, customer service, and data analysis.',
        '{name} uses AI technology to build intelligent agents that can autonomously understand tasks, plan steps, and execute operations to help users automate complex work.',
        '{name} is an agent development and application platform offering no-code building, template marketplace, and API integration, allowing anyone to create their own AI assistant.',
    ],
    'AI资讯': [
        '{name} is an AI news platform providing industry news, technology updates, and product reviews for AI professionals, tech enthusiasts, and investors.',
        '{name} focuses on AI industry information covering large models, machine learning, computer vision, and other cutting-edge technologies to help users stay updated on AI trends.',
        '{name} is an AI vertical media offering in-depth reports, industry analysis, and expert opinions, serving as an important channel for AI professionals to get industry news.',
    ],
    '常用工具': [
        '{name} is a practical online tool providing {feature} capabilities, simple to use with no installation required, suitable for various daily work and life needs.',
        '{name} provides convenient online services supporting {feature} and more, with a clean interface and easy operation, making it a great helper for daily office work.',
        '{name} is a multi-functional online tool platform covering {feature} and other practical functions to help users handle daily tasks efficiently and improve productivity.',
    ],
    '常用网址': [
        '{name} is a popular website platform providing {feature} services with a large user base and good reputation, a frequently visited practical website for internet users.',
        '{name} provides convenient online services covering {feature} and more, with a user-friendly interface and simple operation, suitable for all types of users.',
        '{name} is a well-known online platform offering {feature} and other services with complete features and excellent experience, an indispensable tool website for daily life and work.',
    ],
    '素材编辑': [
        '{name} is a media editing platform offering image editing, video clipping, and audio processing for content creation, marketing materials, and social media.',
        '{name} provides professional media processing tools for creators, supporting multiple formats and effects to help users produce high-quality multimedia content quickly.',
        '{name} is an online media editing platform with simple operation and powerful features, allowing anyone to create stunning images, videos, and audio without professional skills.',
    ],
    '图库网站': [
        '{name} is an image library website providing大量 high-quality image assets including photos, illustrations, and vectors for design, marketing, and web design.',
        '{name} provides rich image resources for users with multiple categories and search options, featuring high-quality images and easy download, an essential resource for designers and creators.',
        '{name} is a professional image asset platform covering commercial photography, art illustrations, and icon assets, supporting free and paid downloads to meet different user needs.',
    ],
}

DEFAULT_TEMPLATES_EN = [
    '{name} is a practical online platform providing various convenient features to help users improve efficiency for daily work and learning scenarios.',
    '{name} provides quality online services with complete features and excellent experience, a worthwhile practical website to bookmark on the internet.',
    '{name} is a professional online tool platform with simple operation and easy access, offering convenient online services without installation.',
]


def get_feature_from_name(name, category, lang='cn'):
    """从站点名称和分类推断功能描述"""
    features_cn = {
        'AI常用工具': 'AI问答、内容生成、智能助手',
        'AI写作工具': '文章写作、文案生成、内容润色',
        'AI图像工具': '图像生成、图片编辑、AI绘画',
        'AI视频工具': '视频生成、智能剪辑、视频编辑',
        'AI音频工具': '语音合成、音频编辑、音乐生成',
        'AI办公工具': '文档处理、数据分析、智能办公',
        'AI编程工具': '代码生成、编程辅助、技术问答',
        'AI设计工具': '智能设计、模板生成、图像编辑',
        'AI翻译工具': '多语言翻译、文档翻译、实时翻译',
        'AI搜索工具': '智能搜索、AI问答、信息检索',
        'AI学习资源': '在线课程、学习工具、知识问答',
        'AI开发平台': '模型训练、API接口、应用开发',
        'AI内容检测': 'AI检测、抄袭检查、内容评估',
        'AI Agent智能体': '智能代理、任务自动化、多Agent协作',
        'AI资讯': '行业新闻、技术动态、产品评测',
        '常用工具': '在线转换、文件处理、实用工具',
        '常用网址': '在线服务、实用工具、资源导航',
        '素材编辑': '图片编辑、视频剪辑、音频处理',
        '图库网站': '图片素材、摄影照片、插画资源',
    }
    features_en = {
        'AI常用工具': 'AI Q&A, content generation, intelligent assistant',
        'AI写作工具': 'article writing, copy generation, content polishing',
        'AI图像工具': 'image generation, photo editing, AI painting',
        'AI视频工具': 'video generation, smart clipping, video editing',
        'AI音频工具': 'speech synthesis, audio editing, music generation',
        'AI办公工具': 'document processing, data analysis, smart office',
        'AI编程工具': 'code generation, programming assistant, technical Q&A',
        'AI设计工具': 'intelligent design, template generation, image editing',
        'AI翻译工具': 'multi-language translation, document translation, real-time translation',
        'AI搜索工具': 'intelligent search, AI Q&A, information retrieval',
        'AI学习资源': 'online courses, learning tools, knowledge Q&A',
        'AI开发平台': 'model training, API interfaces, app development',
        'AI内容检测': 'AI detection, plagiarism checking, content assessment',
        'AI Agent智能体': 'intelligent agents, task automation, multi-agent collaboration',
        'AI资讯': 'industry news, technology updates, product reviews',
        '常用工具': 'online conversion, file processing, utility tools',
        '常用网址': 'online services, utility tools, resource navigation',
        '素材编辑': 'image editing, video clipping, audio processing',
        '图库网站': 'image assets, stock photos, illustration resources',
    }
    if lang == 'en':
        return features_en.get(category, 'multiple practical features')
    return features_cn.get(category, '多种实用功能')


def generate_description(name, category, lang='cn', template_index=0):
    """生成描述"""
    if lang == 'cn':
        templates = CATEGORY_TEMPLATES_CN.get(category, DEFAULT_TEMPLATES_CN)
    else:
        templates = CATEGORY_TEMPLATES_EN.get(category, DEFAULT_TEMPLATES_EN)

    template = templates[template_index % len(templates)]
    feature = get_feature_from_name(name, category, lang)
    return template.format(name=name, feature=feature)


def get_domain(url):
    """提取域名"""
    try:
        return urlparse(url).netloc.lower()
    except:
        return ''


def main():
    parser = argparse.ArgumentParser(description='批量丰富站点描述')
    parser.add_argument('--dry-run', action='store_true', help='只预览不修改')
    parser.add_argument('--min-length', type=int, default=30, help='最小描述长度，低于此值的会被丰富')
    args = parser.parse_args()

    print("=" * 60)
    print("批量丰富站点描述")
    print("=" * 60)

    # 读取数据
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 统计
    total_sites = 0
    enriched_cn = 0
    generated_en = 0
    skipped = 0

    # 遍历所有分类和站点
    for group in data.get('groups', []):
        category = group.get('name', '')
        for idx, site in enumerate(group.get('sites', [])):
            total_sites += 1
            name = site.get('name', '')
            desc_cn = site.get('description', '')

            # 丰富中文描述
            if len(desc_cn) < args.min_length:
                new_desc = generate_description(name, category, 'cn', idx)
                if not args.dry_run:
                    site['description'] = new_desc
                enriched_cn += 1
            else:
                skipped += 1

            # 生成英文描述（如果不存在）
            if 'description_en' not in site or not site.get('description_en'):
                # 如果中文描述已经足够长，基于中文描述简单处理；否则用模板生成
                if len(desc_cn) >= args.min_length:
                    # 有较长中文描述，用模板生成英文（后续可以用翻译API优化）
                    new_desc_en = generate_description(name, category, 'en', idx)
                else:
                    new_desc_en = generate_description(name, category, 'en', idx)
                if not args.dry_run:
                    site['description_en'] = new_desc_en
                generated_en += 1

    print(f"\n统计结果:")
    print(f"  总站点数: {total_sites}")
    print(f"  丰富中文描述: {enriched_cn} ({enriched_cn/total_sites*100:.1f}%)")
    print(f"  生成英文描述: {generated_en} ({generated_en/total_sites*100:.1f}%)")
    print(f"  跳过(描述已足够): {skipped}")

    if args.dry_run:
        print(f"\n[预览模式] 未修改数据文件")
        # 显示几个示例
        print(f"\n示例（前3个丰富的描述）:")
        count = 0
        for group in data.get('groups', []):
            for idx, site in enumerate(group.get('sites', [])):
                if len(site.get('description', '')) < args.min_length and count < 3:
                    name = site.get('name', '')
                    cat = group.get('name', '')
                    print(f"\n  [{cat}] {name}")
                    print(f"    原描述: {site.get('description', '')[:50]}")
                    print(f"    新描述: {generate_description(name, cat, 'cn', idx)[:80]}...")
                    print(f"    英文: {generate_description(name, cat, 'en', idx)[:80]}...")
                    count += 1
        return

    # 备份
    backup_path = JSON_PATH + f'.enrich_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    import shutil
    shutil.copy2(JSON_PATH, backup_path)
    print(f"\n已备份原始文件到: {os.path.basename(backup_path)}")

    # 保存
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已保存修改到: 完整版导航.json")
    print(f"\n完成！")


if __name__ == '__main__':
    main()
