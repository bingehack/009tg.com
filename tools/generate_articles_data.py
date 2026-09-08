#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成各分类文章，写入 data/articles.json
为19个一级分类各生成一篇文章（中英文双语）
"""

import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 分类文章内容定义
ARTICLES_DATA = [
    {
        "id": 1,
        "category": "下海推荐",
        "category_en": "Featured",
        "title": "下海推荐：精选优质工具与资源聚合平台",
        "title_en": "Featured: Curated Quality Tools and Resource Aggregation Platform",
        "summary": "下海推荐分类精选了全网最实用、最高效的工具和资源，涵盖创业、副业、投资、跨境电商等多个领域，帮助用户快速提升工作效率。",
        "summary_en": "The Featured category curates the most practical and efficient tools and resources from across the web, covering entrepreneurship, side hustles, investment, cross-border e-commerce and more, helping users quickly improve work efficiency.",
        "content": """<h2>一、分类概述</h2><p>下海推荐是009tg导航的核心分类之一，精选了经过严格筛选的优质工具和资源。这个分类的每一个站点都经过人工审核，确保安全可靠、实用高效。</p><h2>二、收录标准</h2><ul><li><strong>实用性</strong>：工具必须能够解决用户的实际问题，提升工作效率</li><li><strong>安全性</strong>：网站必须合法合规，不涉及违法违规内容</li><li><strong>稳定性</strong>：网站需要有持续的维护和更新，访问速度快</li><li><strong>口碑好</strong>：在用户中有良好的口碑和评价</li></ul><h2>三、使用建议</h2><p>建议用户在使用下海推荐分类时，先浏览分类下的所有站点，了解每个工具的功能和特点，然后根据自身需求选择合适的工具。同时，建议收藏本站，定期查看更新，获取最新的优质工具推荐。</p><h2>四、推荐工具</h2><p>下海推荐分类包含了多个领域的优质工具，涵盖效率工具、短链生成、指纹检测、筛号工具等多个子分类。每个工具都有详细的描述和使用说明，帮助用户快速上手。</p><p>更多优质工具，请访问<a href='../category/1.html'>下海推荐分类</a>页面。</p>""",
        "content_en": """<h2>1. Category Overview</h2><p>Featured is one of the core categories of 009tg Navigation, curating quality tools and resources that have undergone rigorous screening. Every site in this category has been manually reviewed to ensure it is safe, reliable, practical, and efficient.</p><h2>2. Inclusion Criteria</h2><ul><li><strong>Practicality</strong>: Tools must solve real user problems and improve work efficiency</li><li><strong>Security</strong>: Websites must be legal and compliant, without illegal or prohibited content</li><li><strong>Stability</strong>: Websites require continuous maintenance and updates with fast access speeds</li><li><strong>Good Reputation</strong>: Positive reputation and reviews among users</li></ul><h2>3. Usage Recommendations</h2><p>When using the Featured category, we recommend users first browse all sites under the category to understand each tool's features and characteristics, then select appropriate tools based on their own needs. Additionally, we recommend bookmarking this site and checking for updates regularly to get the latest quality tool recommendations.</p><h2>4. Recommended Tools</h2><p>The Featured category includes quality tools across multiple fields, covering efficiency tools, short link generation, fingerprint detection, number screening tools and more subcategories. Each tool has detailed descriptions and usage instructions to help users get started quickly.</p><p>For more quality tools, visit the <a href='../category/1.html'>Featured category</a> page.</p>""",
        "tags": ["精选工具", "效率提升", "资源聚合"],
        "tags_en": ["Featured Tools", "Efficiency", "Resource Aggregation"],
    },
    {
        "id": 2,
        "category": "AI工具",
        "category_en": "AI Tools",
        "title": "AI工具大全：2026年最值得关注的人工智能工具汇总",
        "title_en": "AI Tools Complete Guide: Top Artificial Intelligence Tools Worth Watching in 2026",
        "summary": "本文汇总了2026年最值得关注的AI工具，涵盖AI写作、AI绘画、AI视频、AI编程、AI办公等多个领域，帮助用户快速找到适合自己的AI工具。",
        "summary_en": "This article summarizes the most noteworthy AI tools of 2026, covering AI writing, AI drawing, AI video, AI programming, AI office and more, helping users quickly find AI tools that suit them.",
        "content": """<h2>一、AI工具发展现状</h2><p>2026年，人工智能技术已经深入到我们工作和生活的方方面面。从文本生成到图像创作，从视频制作到编程辅助，AI工具正在深刻改变着我们的工作方式。009tg导航的AI工具分类收录了超过200款优质AI工具，涵盖12个子分类。</p><h2>二、核心子分类</h2><h3>1. AI常用工具</h3><p>包含ChatGPT、Claude、文心一言等通用大语言模型，适用于文本生成、问题解答、代码编写等多种场景。</p><h3>2. AI写作工具</h3><p>专注于内容创作的AI工具，支持文章写作、文案生成、内容润色等功能，是内容创作者的得力助手。</p><h3>3. AI图像工具</h3><p>包括Midjourney、Stable Diffusion、DALL-E等AI绘画工具，支持文本生成图像、图像编辑、风格迁移等功能。</p><h3>4. AI视频工具</h3><p>Runway、腾讯智影等AI视频工具，支持文本生成视频、视频剪辑、数字人播报等功能，大幅降低视频制作门槛。</p><h3>5. AI编程工具</h3><p>GitHub Copilot、Cursor等AI编程助手，支持代码补全、代码解释、Bug修复、代码重构等功能，提升开发效率。</p><h2>三、选择建议</h2><p>面对众多AI工具，用户应该根据自身需求选择2-3款核心工具深入学习，而不是浅尝辄止。通用型工具建议选择ChatGPT或Claude，专业领域工具根据具体需求选择。</p><p>更多AI工具，请访问<a href='../category/10.html'>AI工具分类</a>页面。</p>""",
        "content_en": """<h2>1. AI Tools Development Status</h2><p>In 2026, artificial intelligence technology has penetrated into all aspects of our work and life. From text generation to image creation, from video production to programming assistance, AI tools are profoundly changing the way we work. The AI Tools category of 009tg Navigation lists over 200 quality AI tools across 12 subcategories.</p><h2>2. Core Subcategories</h2><h3>2.1 AI Common Tools</h3><p>Includes general large language models like ChatGPT, Claude, ERNIE Bot, suitable for text generation, Q&A, coding and more scenarios.</p><h3>2.2 AI Writing Tools</h3><p>AI tools focused on content creation, supporting article writing, copy generation, content polishing and more, essential assistants for content creators.</p><h3>2.3 AI Image Tools</h3><p>Includes AI drawing tools like Midjourney, Stable Diffusion, DALL-E, supporting text-to-image, image editing, style transfer and more.</p><h3>2.4 AI Video Tools</h3><p>AI video tools like Runway, Tencent Zhiying, supporting text-to-video, video editing, digital human broadcasting, significantly lowering the barrier to video production.</p><h3>2.5 AI Programming Tools</h3><p>AI programming assistants like GitHub Copilot, Cursor, supporting code completion, code explanation, bug fixing, code refactoring, improving development efficiency.</p><h2>3. Selection Recommendations</h2><p>Faced with numerous AI tools, users should select 2-3 core tools based on their own needs and learn them in depth, rather than scratching the surface. For general-purpose tools, ChatGPT or Claude are recommended; for professional domain tools, choose based on specific needs.</p><p>For more AI tools, visit the <a href='../category/10.html'>AI Tools category</a> page.</p>""",
        "tags": ["AI工具", "人工智能", "效率工具"],
        "tags_en": ["AI Tools", "Artificial Intelligence", "Productivity"],
    },
    {
        "id": 3,
        "category": "跨境资讯",
        "category_en": "Cross-border News",
        "title": "跨境资讯：获取全球跨境电商行业动态的最佳渠道",
        "title_en": "Cross-border News: Best Channels for Global E-commerce Industry Updates",
        "summary": "跨境资讯分类收录了全球主流的跨境电商新闻媒体、行业论坛和资讯平台，帮助从业者及时了解行业动态、政策变化和市场趋势。",
        "summary_en": "The Cross-border News category lists mainstream global cross-border e-commerce news media, industry forums and information platforms, helping practitioners stay updated on industry dynamics, policy changes and market trends.",
        "content": """<h2>一、为什么关注跨境资讯</h2><p>跨境电商行业变化迅速，政策法规、平台规则、市场趋势都在不断变化。及时获取准确的行业资讯，是跨境电商从业者做出正确决策的基础。009tg导航的跨境资讯分类收录了全球主流的资讯渠道，帮助用户一站式获取行业动态。</p><h2>二、核心子分类</h2><h3>1. 全球新闻</h3><p>涵盖国际主流财经媒体和科技媒体，提供全球宏观经济和科技行业的最新动态。</p><h3>2. 中国论坛</h3><p>国内知名的跨境电商论坛和社区，包括知无不言、跨境知道等，用户可以交流经验、分享资源。</p><h3>3. 国外论坛</h3><p>国外知名的电商论坛和社区，包括Warrior Forum、Black Hat World等，了解海外卖家的玩法和策略。</p><h3>4. 行业媒体</h3><p>专注于跨境电商行业的垂直媒体，包括亿邦动力、雨果网、跨境眼等，提供深度行业分析和报道。</p><h2>三、资讯获取建议</h2><ul><li><strong>每日浏览</strong>：建议每天花15-30分钟浏览行业资讯，保持对行业的敏感度</li><li><strong>重点关注</strong>：关注平台政策变化、关税政策调整、汇率波动等直接影响业务的信息</li><li><strong>深度阅读</strong>：对于重要的行业报告和分析文章，建议深度阅读，理解背后的逻辑</li><li><strong>交流讨论</strong>：在论坛和社区中与其他从业者交流，获取不同视角的信息</li></ul><p>更多跨境资讯渠道，请访问<a href='../category/17.html'>跨境资讯分类</a>页面。</p>""",
        "content_en": """<h2>1. Why Follow Cross-border News</h2><p>The cross-border e-commerce industry changes rapidly, with policies, platform rules, and market trends constantly evolving. Timely access to accurate industry information is the foundation for cross-border e-commerce practitioners to make correct decisions. The Cross-border News category of 009tg Navigation lists mainstream global information channels, helping users get industry dynamics in one stop.</p><h2>2. Core Subcategories</h2><h3>2.1 Global News</h3><p>Covers international mainstream financial and tech media, providing the latest updates on global macroeconomics and the tech industry.</p><h3>2.2 China Forums</h3><p>Well-known domestic cross-border e-commerce forums and communities, where users can exchange experiences and share resources.</p><h3>2.3 Foreign Forums</h3><p>Well-known international e-commerce forums and communities, to understand overseas sellers' strategies and tactics.</p><h3>2.4 Industry Media</h3><p>Vertical media focused on the cross-border e-commerce industry, providing in-depth industry analysis and reporting.</p><h2>3. Information Acquisition Recommendations</h2><ul><li><strong>Daily Browsing</strong>: Recommend spending 15-30 minutes daily browsing industry news to maintain industry sensitivity</li><li><strong>Key Focus</strong>: Focus on information that directly affects business, such as platform policy changes, tariff policy adjustments, exchange rate fluctuations</li><li><strong>In-depth Reading</strong>: For important industry reports and analysis articles, recommend in-depth reading to understand the underlying logic</li><li><strong>Discussion</strong>: Communicate with other practitioners in forums and communities to get information from different perspectives</li></ul><p>For more cross-border news channels, visit the <a href='../category/17.html'>Cross-border News category</a> page.</p>""",
        "tags": ["跨境资讯", "行业动态", "新闻媒体"],
        "tags_en": ["Cross-border News", "Industry Updates", "News Media"],
    },
    {
        "id": 4,
        "category": "跨境推广",
        "category_en": "Cross-border Marketing",
        "title": "跨境推广：海外营销推广工具与渠道完全指南",
        "title_en": "Cross-border Marketing: Complete Guide to Overseas Marketing Tools and Channels",
        "summary": "跨境推广分类收录了广告联盟、SEO工具、流量交换、邮件营销等海外营销推广工具，帮助跨境卖家提升品牌曝光和产品销量。",
        "summary_en": "The Cross-border Marketing category lists overseas marketing tools including ad networks, SEO tools, traffic exchange, email marketing, helping cross-border sellers increase brand exposure and product sales.",
        "content": """<h2>一、跨境推广的重要性</h2><p>在竞争激烈的跨境电商市场，好的产品需要好的推广才能卖出去。跨境推广涵盖了广告投放、搜索引擎优化、社交媒体营销、邮件营销等多个方面，是跨境电商运营的核心环节之一。009tg导航的跨境推广分类收录了丰富的推广工具和渠道。</p><h2>二、核心子分类</h2><h3>1. 广告联盟</h3><p>包括Google Ads、Facebook Ads、TikTok Ads等主流广告平台，以及原生广告、弹窗广告等 specialized 广告网络。通过广告投放可以快速获取精准流量。</p><h3>2. SEO工具</h3><p>包括Ahrefs、SEMrush、Moz等专业SEO工具，帮助优化独立站的搜索引擎排名，获取长期稳定的自然流量。</p><h3>3. 流量交换</h3><p>流量交换平台可以帮助新站快速获取初始流量，提升网站的曝光度和排名。</p><h3>4. 邮件营销</h3><p>包括Mailchimp、ConvertKit、GetResponse等邮件营销工具，用于客户留存、复购营销和新品推广。</p><h2>三、推广策略建议</h2><ul><li><strong>多渠道组合</strong>：不要依赖单一渠道，建议广告+SEO+社媒+邮件多渠道组合推广</li><li><strong>数据驱动</strong>：每个推广渠道都要跟踪数据，计算ROI，把预算投入到效果最好的渠道</li><li><strong>本地化</strong>：针对不同国家和地区的用户，采用本地化的营销策略和素材</li><li><strong>持续优化</strong>：推广是一个持续优化的过程，需要不断测试和调整策略</li></ul><p>更多跨境推广工具，请访问<a href='../category/22.html'>跨境推广分类</a>页面。</p>""",
        "content_en": """<h2>1. Importance of Cross-border Marketing</h2><p>In the highly competitive cross-border e-commerce market, good products need good marketing to sell. Cross-border marketing covers advertising, search engine optimization, social media marketing, email marketing and more, and is one of the core aspects of cross-border e-commerce operations. The Cross-border Marketing category of 009tg Navigation lists rich marketing tools and channels.</p><h2>2. Core Subcategories</h2><h3>2.1 Ad Networks</h3><p>Includes mainstream advertising platforms like Google Ads, Facebook Ads, TikTok Ads, as well as native advertising, pop-up advertising and other specialized ad networks. Through advertising, you can quickly acquire targeted traffic.</p><h3>2.2 SEO Tools</h3><p>Includes professional SEO tools like Ahrefs, SEMrush, Moz, helping optimize independent site search engine rankings to acquire long-term stable organic traffic.</p><h3>2.3 Traffic Exchange</h3><p>Traffic exchange platforms can help new sites quickly acquire initial traffic, improving site exposure and rankings.</p><h3>2.4 Email Marketing</h3><p>Includes email marketing tools like Mailchimp, ConvertKit, GetResponse, for customer retention, repurchase marketing and new product promotion.</p><h2>3. Marketing Strategy Recommendations</h2><ul><li><strong>Multi-channel Combination</strong>: Don't rely on a single channel; recommend combining advertising + SEO + social media + email marketing</li><li><strong>Data-driven</strong>: Track data for every marketing channel, calculate ROI, and invest budget in the best-performing channels</li><li><strong>Localization</strong>: Adopt localized marketing strategies and creatives for users in different countries and regions</li><li><strong>Continuous Optimization</strong>: Marketing is a continuous optimization process that requires constant testing and strategy adjustment</li></ul><p>For more cross-border marketing tools, visit the <a href='../category/22.html'>Cross-border Marketing category</a> page.</p>""",
        "tags": ["跨境推广", "广告投放", "SEO", "邮件营销"],
        "tags_en": ["Cross-border Marketing", "Advertising", "SEO", "Email Marketing"],
    },
    {
        "id": 5,
        "category": "社媒资源",
        "category_en": "Social Media",
        "title": "社媒资源：海外社交媒体运营工具与账号管理大全",
        "title_en": "Social Media: Complete Guide to Overseas Social Media Operations Tools and Account Management",
        "summary": "社媒资源分类收录了社交媒体工具、社媒导航、账号管理、数据分析等资源，帮助运营者高效管理海外社交媒体账号，提升运营效果。",
        "summary_en": "The Social Media category lists social media tools, social navigation, account management, data analysis and more resources, helping operators efficiently manage overseas social media accounts and improve operational results.",
        "content": """<h2>一、海外社交媒体运营概述</h2><p>海外社交媒体是跨境电商和品牌出海的重要营销渠道。Facebook、Instagram、TikTok、YouTube、Twitter等平台拥有数十亿用户，是品牌获取流量和客户的重要来源。009tg导航的社媒资源分类收录了丰富的社媒运营工具和资源。</p><h2>二、核心子分类</h2><h3>1. 社媒工具</h3><p>包括社交媒体管理工具（如Buffer、Hootsuite）、内容创作工具、数据分析工具等，帮助运营者高效管理多个社媒账号。</p><h3>2. 社媒导航</h3><p>收录了全球主流的社交媒体平台和社区，方便用户快速访问和了解各个平台的特点。</p><h2>三、主要平台特点</h2><ul><li><strong>Facebook</strong>：全球最大的社交平台，用户覆盖广，适合品牌建设和广告投放</li><li><strong>Instagram</strong>：以图片和短视频为主，适合时尚、美妆、生活方式类产品</li><li><strong>TikTok</strong>：短视频平台，增长迅速，适合年轻用户群体和病毒式营销</li><li><strong>YouTube</strong>：长视频平台，适合产品评测、教程和品牌故事内容</li><li><strong>Twitter</strong>：实时信息平台，适合品牌公关和实时互动</li><li><strong>Telegram</strong>：加密通讯工具，适合社群运营和私域流量</li></ul><h2>四、运营建议</h2><ul><li><strong>平台选择</strong>：根据目标用户和产品特点选择2-3个核心平台深耕，不要贪多</li><li><strong>内容为王</strong>：持续产出优质内容是社媒运营的核心，建议制定内容日历</li><li><strong>数据分析</strong>：定期分析各平台的数据表现，优化内容策略</li><li><strong>用户互动</strong>：积极回复用户评论和私信，建立品牌忠诚度</li></ul><p>更多社媒资源，请访问<a href='../category/27.html'>社媒资源分类</a>页面。</p>""",
        "content_en": """<h2>1. Overseas Social Media Operations Overview</h2><p>Overseas social media is an important marketing channel for cross-border e-commerce and brand globalization. Platforms like Facebook, Instagram, TikTok, YouTube, Twitter have billions of users and are important sources of traffic and customers for brands. The Social Media category of 009tg Navigation lists rich social media operation tools and resources.</p><h2>2. Core Subcategories</h2><h3>2.1 Social Media Tools</h3><p>Includes social media management tools (like Buffer, Hootsuite), content creation tools, data analysis tools, helping operators efficiently manage multiple social media accounts.</p><h3>2.2 Social Navigation</h3><p>Lists mainstream global social media platforms and communities, making it easy for users to quickly access and understand each platform's characteristics.</p><h2>3. Main Platform Characteristics</h2><ul><li><strong>Facebook</strong>: The world's largest social platform with broad user coverage, suitable for brand building and advertising</li><li><strong>Instagram</strong>: Primarily image and short video based, suitable for fashion, beauty, lifestyle products</li><li><strong>TikTok</strong>: Short video platform with rapid growth, suitable for young user demographics and viral marketing</li><li><strong>YouTube</strong>: Long video platform, suitable for product reviews, tutorials and brand story content</li><li><strong>Twitter</strong>: Real-time information platform, suitable for brand PR and real-time interaction</li><li><strong>Telegram</strong>: Encrypted communication tool, suitable for community operations and private domain traffic</li></ul><h2>4. Operation Recommendations</h2><ul><li><strong>Platform Selection</strong>: Select 2-3 core platforms based on target users and product characteristics; don't try to do too many</li><li><strong>Content is King</strong>: Continuously producing quality content is the core of social media operations; recommend creating a content calendar</li><li><strong>Data Analysis</strong>: Regularly analyze data performance across platforms to optimize content strategy</li><li><strong>User Interaction</strong>: Actively respond to user comments and messages to build brand loyalty</li></ul><p>For more social media resources, visit the <a href='../category/27.html'>Social Media category</a> page.</p>""",
        "tags": ["社媒资源", "社交媒体", "运营工具"],
        "tags_en": ["Social Media", "Social Networks", "Operations Tools"],
    },
]

# 由于篇幅限制，这里只定义5篇，剩余14篇用模板生成
# 实际上我会在下面用代码生成完整的19篇

def generate_article_from_template(cat_id, cat_name, cat_name_en, site_count):
    """根据分类模板生成文章"""
    # 分类描述映射
    cat_descriptions = {
        "全球网络": ("全球网络工具与资源汇总", "Global Network Tools and Resources Summary",
                     "VPS、域名、CDN、DNS等网络基础设施工具", "VPS, domain, CDN, DNS and other network infrastructure tools"),
        "全球接码": ("全球接码平台与虚拟号码服务大全", "Global SMS Verification and Virtual Number Services Guide",
                     "虚拟号码、验证码接收、隐私保护等服务", "Virtual numbers, SMS verification, privacy protection services"),
        "数字货币": ("数字货币与区块链资源完全指南", "Cryptocurrency and Blockchain Resources Complete Guide",
                     "交易所、钱包、行情、DeFi、NFT等区块链资源", "Exchanges, wallets, market data, DeFi, NFT and blockchain resources"),
        "全球支付": ("全球支付与跨境收款工具汇总", "Global Payment and Cross-border Collection Tools Summary",
                     "跨境支付、收款平台、虚拟卡、汇款等支付工具", "Cross-border payment, collection platforms, virtual cards, remittance and payment tools"),
        "Facebook": ("Facebook营销与广告投放完全指南", "Facebook Marketing and Advertising Complete Guide",
                     "Facebook广告、主页运营、社群管理等工具", "Facebook ads, page operations, community management tools"),
        "Google": ("Google工具与服务完全指南", "Google Tools and Services Complete Guide",
                     "Google搜索、广告、分析、云服务等工具", "Google search, ads, analytics, cloud services and tools"),
        "广告工具": ("广告投放与营销工具大全", "Advertising and Marketing Tools Complete Guide",
                     "广告平台、追踪工具、素材制作等营销工具", "Ad platforms, tracking tools, creative production and marketing tools"),
        "指纹浏览器": ("指纹浏览器与反检测工具完全指南", "Antidetect Browser and Anti-detection Tools Complete Guide",
                     "多账号管理、指纹伪装、反检测浏览器工具", "Multi-account management, fingerprint spoofing, anti-detection browser tools"),
        "全球APP下载": ("全球APP下载与应用资源汇总", "Global APP Download and Application Resources Summary",
                     "海外应用商店、APP下载、破解资源等", "Overseas app stores, APP downloads, cracked resources"),
        "内容制作": ("内容创作与多媒体制作工具大全", "Content Creation and Multimedia Production Tools Guide",
                     "图片设计、视频剪辑、音频处理、文案写作等工具", "Image design, video editing, audio processing, copywriting tools"),
        "技术交流": ("技术交流与开发者资源汇总", "Tech Community and Developer Resources Summary",
                     "开发者社区、技术论坛、开源项目、编程工具", "Developer communities, tech forums, open source projects, programming tools"),
        "引流工具": ("流量获取与引流工具完全指南", "Traffic Generation and Lead Generation Tools Guide",
                     "流量交换、SEO、社媒引流、内容营销等工具", "Traffic exchange, SEO, social media traffic, content marketing tools"),
        "跨境电商": ("跨境电商工具与平台完全指南", "Cross-border E-commerce Tools and Platforms Guide",
                     "电商平台、选品工具、ERP、物流、支付等工具", "E-commerce platforms, product research, ERP, logistics, payment tools"),
        "跨境服务": ("跨境服务与外包资源汇总", "Cross-border Services and Outsourcing Resources Summary",
                     "翻译、设计、开发、客服等跨境服务", "Translation, design, development, customer service and cross-border services"),
    }

    if cat_name in cat_descriptions:
        title, title_en, desc, desc_en = cat_descriptions[cat_name]
    else:
        title = f"{cat_name}：优质工具与资源完全指南"
        title_en = f"{cat_name_en}: Quality Tools and Resources Complete Guide"
        desc = f"{cat_name}相关的优质工具和资源"
        desc_en = f"Quality tools and resources related to {cat_name_en}"

    summary = f"{cat_name}分类收录了{site_count}个优质站点，涵盖{desc}，帮助用户快速找到所需工具和资源。"
    summary_en = f"The {cat_name_en} category lists {site_count} quality sites, covering {desc_en}, helping users quickly find the tools and resources they need."

    content = f"""<h2>一、分类概述</h2><p>{cat_name}是009tg导航的重要分类之一，收录了{site_count}个优质站点，涵盖{desc}。这个分类的每一个站点都经过严格筛选，确保安全可靠、实用高效。</p><h2>二、核心功能与特点</h2><ul><li><strong>工具丰富</strong>：涵盖{desc}等多个方面，满足用户多样化需求</li><li><strong>严格筛选</strong>：每个站点都经过人工审核，确保质量和安全性</li><li><strong>持续更新</strong>：定期更新站点列表，移除失效站点，添加新的优质工具</li><li><strong>分类清晰</strong>：采用多级分类结构，方便用户快速定位所需工具</li></ul><h2>三、使用建议</h2><p>建议用户在使用{cat_name}分类时，先了解每个工具的功能和特点，然后根据自身需求选择合适的工具。同时，建议收藏本站，定期查看更新，获取最新的工具推荐。</p><h2>四、注意事项</h2><ul><li><strong>安全第一</strong>：使用任何工具前，建议先了解其安全性和隐私政策</li><li><strong>合规使用</strong>：确保使用工具的方式符合当地法律法规</li><li><strong>数据备份</strong>：重要数据建议定期备份，避免意外丢失</li><li><strong>成本控制</strong>：付费工具建议先试用，确认满足需求后再付费</li></ul><p>更多{cat_name}相关工具，请访问<a href='../category/{cat_id}.html'>{cat_name}分类</a>页面。</p>"""

    content_en = f"""<h2>1. Category Overview</h2><p>{cat_name_en} is one of the important categories of 009tg Navigation, listing {site_count} quality sites, covering {desc_en}. Every site in this category has undergone rigorous screening to ensure it is safe, reliable, practical, and efficient.</p><h2>2. Core Features and Characteristics</h2><ul><li><strong>Rich Tools</strong>: Covers multiple aspects including {desc_en}, meeting diverse user needs</li><li><strong>Rigorous Screening</strong>: Every site is manually reviewed to ensure quality and security</li><li><strong>Continuous Updates</strong>: Regularly update the site list, remove broken sites, add new quality tools</li><li><strong>Clear Classification</strong>: Multi-level category structure for easy navigation to find needed tools</li></ul><h2>3. Usage Recommendations</h2><p>When using the {cat_name_en} category, we recommend users first understand each tool's features and characteristics, then select appropriate tools based on their own needs. Additionally, we recommend bookmarking this site and checking for updates regularly to get the latest tool recommendations.</p><h2>4. Precautions</h2><ul><li><strong>Safety First</strong>: Before using any tool, recommend understanding its security and privacy policy</li><li><strong>Compliant Use</strong>: Ensure the way you use tools complies with local laws and regulations</li><li><strong>Data Backup</strong>: Recommend regular backups of important data to avoid accidental loss</li><li><strong>Cost Control</strong>: For paid tools, recommend trying before paying to confirm they meet your needs</li></ul><p>For more {cat_name_en} related tools, visit the <a href='../category/{cat_id}.html'>{cat_name_en} category</a> page.</p>"""

    tags = [cat_name, "工具推荐", "资源汇总"]
    tags_en = [cat_name_en, "Tool Recommendations", "Resource Summary"]

    return {
        "id": cat_id + 100,  # 避免与已有文章ID冲突
        "title": title,
        "title_en": title_en,
        "category": cat_name,
        "category_en": cat_name_en,
        "author": "Invisible Man",
        "publishDate": "2026-09-08",
        "summary": summary,
        "summary_en": summary_en,
        "content": content,
        "content_en": content_en,
        "tags": tags,
        "tags_en": tags_en,
        "views": 0,
        "isPublic": True,
    }


def main():
    # 读取分类数据
    with open(os.path.join(PROJECT_ROOT, '完整版导航.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    groups = [g for g in data['groups'] if g.get('parent_id') is None]

    # 已有文章（手动写的5篇）
    existing_articles = ARTICLES_DATA

    # 已有分类ID集合
    existing_cats = {a['category'] for a in existing_articles}

    # 为剩余分类生成文章
    all_articles = existing_articles.copy()
    for g in groups:
        if g['name'] not in existing_cats:
            article = generate_article_from_template(g['id'], g['name'], g['name'], len(g['sites']))
            all_articles.append(article)

    # 按ID排序
    all_articles.sort(key=lambda x: x['id'])

    # 保存
    output = {
        "version": "2.0",
        "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
        "articles": all_articles
    }

    output_path = os.path.join(PROJECT_ROOT, 'data', 'articles.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"生成完成！共 {len(all_articles)} 篇文章")
    for a in all_articles:
        print(f"  [{a['id']}] {a['category']}: {a['title'][:40]}...")


if __name__ == '__main__':
    main()
