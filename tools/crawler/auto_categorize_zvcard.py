#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zvcard抓取站点自动分类映射
根据站点名称、描述、URL关键词自动匹配到现有分类体系
"""

import json
import os
import re
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 关键词→分类映射规则
# 格式: (关键词列表, 目标分类名)
CATEGORY_RULES = [
    # 虚拟卡/支付
    (['虚拟卡', 'virtual card', 'vmcard', 'airsecurecard', 'vmlogin'], '虚拟卡'),
    (['支付', 'payment', 'payssion', 'oceanpayment', 'asiabill', 'useepay', 'glocash',
      'xtransfer', 'remitly', 'xoom', 'western union', 'paysend', '熊猫速汇', '考拉速汇',
      '通联支付', '珊瑚跨境', 'onerway', 'allinpay', 'adyen', 'checkout', 'square',
      'paymentwall', 'authorize', 'stripe', 'nuvei', '2checkout', 'worldpay',
      'koho', 'greenwood', 'green dot', 'greenlight', 'first global', 'step',
      'majority', 'nubank', 'novo', 'current', 'lili', 'varo', 'chime', 'airbase',
      'yokoy', 'tribal', 'm2p', 'tide', 'jeeves', 'divvy', 'e.pn', 'spendesk',
      'brex', 'mesh', '分贝通', 'fenbeitong', 'juni', 'ramp', 'payoneer', 'paypal'],
     '全球支付'),

    # 指纹浏览器
    (['指纹浏览器', '指纹', 'fingerprint', 'adspower', '比特浏览器', 'bitbrowser',
      'vmlogin', 'vmlogin.us', 'multilogin', 'gologin', 'undetectable', 'kameleo',
      'dolphin', 'anty', 'sessionbox', 'linken sphere', 'incogniton', 'vpass'],
     '指纹浏览器'),

    # 代理IP
    (['代理', 'proxy', 'ip代理', '住宅代理', '静态代理', '动态ip', 'ipipgo', '922proxy',
      '911proxy', 'lunaproxy', 'smartproxy', 'astrill', 'thordata', 'cliproxy', 'ip2up',
      'novproxy', '辣椒http', 'lajiaohttp', 'loongproxy', '神龙', 'shenlongproxy',
      'pyproxy', 'pyproxy.com', 'toktik', '猎豹tk', 'liebaotk', '快洋淘',
      '小熊ip', '流冠', '极光', '芝麻http', 'iprocket', 'iprocket', 'stormproxies',
      'oxylabs', 'bright data', 'luminati', 'netnut', 'shifter', 'geoedge',
      'soax', 'proxy-cheap', 'infatica', 'packetstream', 'peer2profit', 'iproyal',
      'mightyproxy', 'proxy-seller', 'fineproxy', 'buyproxies', 'sslprivateproxy',
      'squidproxies', 'myprivateproxy', 'instantproxies', 'proxynova', 'free-proxy',
      'vpn', '翻墙', '科学上网'],
     '全球网络'),

    # 接码/短信
    (['接码', '短信', 'sms', '验证码', '虚拟号码', 'sms-activate', '5sim', 'smspva',
      'smshub', 'sms-man', 'onlinesim', 'receive-sms', 'textverified', 'smstools',
      'cheapsms', 'smsleg', 'getsms', 'sms-online', 'supercloudsms', '超级云短信',
      '云上focus', 'bnxrn', 'jiemadi', 'z-sms', 'smsonline', 'textnow',
      'google voice', 'gv号', '虚拟号'],
     '全球接码'),

    # 社媒账户
    (['社媒账户', '账户购买', '账号购买', 'accsmarket', 'nowacc', 'accmarket',
      'facebook账号', 'instagram账号', 'twitter账号', 'tiktok账号', 'telegram账号',
      'google账号', 'gmail账号', 'youtube账号', 'reddit账号', 'discord账号',
      'spotify账号', 'netflix账号', 'amazon账号', 'ebay账号', 'paypal账号',
      '苹果id', 'apple id', '国外id', 'appstore', 'itunes', '账号星球',
      'accboy', 'acceboy', '账号', '老号', '白号', '黑号', '农场号'],
     '社媒资源'),

    # 涨粉/社媒营销
    (['涨粉', '粉丝', 'famesweb', 'fames', 'likes', 'views', 'followers',
      '社交媒体营销', 'social media', '社媒营销', '刷粉', '刷赞', '刷播放',
      'socialtracker', 'social tracker', 'socialmediaexaminer', 'social media examiner'],
     '社媒资源'),

    # TikTok相关
    (['tiktok', '抖音', 'tikrank', 'tikbuddy', 'exolyt', 'tichoo', '滴嗒狗',
      'didadog', 'pentos', 'kalodata', 'tabcut', 'tiklog', 'tikstar', 'fastdata',
      '飞瓜', 'feigua', '短鱼儿', 'duanyuer', '抖查查', 'douchacha',
      'analisa', 'tiktok数据分析', 'tiktok运营', 'tk运营', '短视频', '直播'],
     '社媒资源'),

    # 跨境电商/ERP
    (['跨境电商', '电商', 'erp', '选品', '积加', 'gcbnt', '酋长', 'datacaciques',
      '宝莲云', 'baoliannet', '客优云', 'keyouyun', '万里牛', 'hupun', 'sorftime',
      'sellics', 'perpetua', 'merchantspring', '全卖通', 'quanmaitong', 'algopix',
      'amz one', 'amzone', 'fetcher', 'junglescout', 'jungle scout', 'ppcscope',
      'bqool', '比酷尔', '数派', 'isellerpal', '跨境', '亚马逊', 'amazon',
      'shopify', '独立站', 'woocommerce', 'magento', 'opencart', 'prestashop',
      'bigcommerce', 'wix', 'wordpress', '建站', '店匠', 'shoplemo', 'ueeshop',
      'shopyy', 'shopline', 'shoplazza', '店小秘', '赛盒', '通途', '芒果店长',
      '马帮', '普源', '网店管家', '管易', 'e店宝', '卖家云', '速脉', '全球交易助手'],
     '跨境电商'),

    # AI工具
    (['ai', '人工智能', 'chatgpt', 'gpt', 'midjourney', 'stable diffusion', 'dall-e',
      'runway', 'gen2', 'make-a-video', 'makeavideo', '商汤', 'sensetime',
      'decoherence', '腾讯智影', 'zenvideo', 'autopod', 'invideo', 'memo ai',
      'propainter', 'tokenflow', 'heygen', 'gaussian painters', 'modelscope',
      'stable audio', '创客贴', 'chuangkit', 'musiclm', '讯飞听见', 'iflyrec',
      'lalal.ai', 'aiva', 'vectorizer', 'faceswapper', '腾讯arc', 'arc.tencent',
      'smashorpass', '前嗅', 'forenose', 'ip adapter', 'mnbvc', 'sec insights',
      'secinsights', '腾讯混元', 'hunyuan', 'falcon', 'aipetphotos', 'ai宠物',
      'ai工具', 'ai写作', 'ai绘画', 'ai视频', 'ai语音', 'ai翻译', 'ai编程',
      'copilot', 'github copilot', 'cursor', 'tabnine', 'codeium', 'ai21',
      'anthropic', 'claude', 'bard', 'gemini', '文心一言', '通义千问', '讯飞星火',
      '智谱清言', 'chatglm', 'baichuan', '百川', 'minimax', 'moonshot', 'kimi',
      'deepseek', '零一万物', 'yi', 'qwen', 'llama', 'mistral', 'phi', 'grok',
      'perplexity', 'pi', 'character.ai', 'replika', 'janitorai', 'chai',
      'novelai', 'nai', 'stable diffusion', 'sd', 'comfyui', 'automatic1111',
      'webui', 'invokeai', 'leonardo', 'leonardo.ai', 'seaart', 'seaart.ai',
      'tensor.art', 'tensorart', 'civitai', 'huggingface', 'hugging face',
      'replicate', 'replicate.com', 'banana', 'banana.dev', 'runpod', 'runpod.io',
      'vast.ai', 'vastai', 'lambdalabs', 'lambda labs', 'coreweave',
      'openai', 'openai.com', 'dalle', 'dall-e', 'whisper', 'embedding',
      'fine-tuning', '微调', '训练', '大模型', 'llm', 'agi'],
     'AI常用工具'),

    # 广告/营销
    (['广告', 'ad', 'advertising', 'marketing', '营销', '推广', 'adsense', 'adwords',
      'google ads', 'facebook ads', 'meta ads', 'tiktok ads', 'instagram ads',
      'youtube ads', 'twitter ads', 'linkedin ads', 'pinterest ads', 'snapchat ads',
      'reddit ads', 'quora ads', 'taboola', 'outbrain', 'mgid', 'revcontent',
      'content.ad', 'adsterra', 'propellerads', 'popads', 'exoclick', 'trafficjunky',
      'trafficfactory', 'juicyads', 'plugrush', 'exoClick', 'adnium', 'adsupply',
      'admedia', 'adnow', 'adreactor', 'adscooh', 'adtarget', 'adventurefeeds',
      'affiliate', '联盟', 'cpa', 'cpa营销', 'cpa联盟', 'offer', 'affiliate marketing',
      'clickbank', 'cj', 'commission junction', 'shareasale', 'impact', 'partnerstack',
      'refersion', 'post affiliate pro', 'tapfiliate', 'rewardful', 'firstpromoter',
      'growsumo', 'partnerize', 'rakuten', 'awin', 'webgains', 'tradedoubler',
      'flexoffers', 'pepperjam', 'jvzoo', 'warriorplus', 'muncheye', 'clickmagick',
      'voluum', 'bemob', 'binom', 'keitaro', 'trackingdesk', 'redtrack', 'thrive',
      'cpalab', 'cpalander', 'cpazilla', 'cpadirectory', 'cpafinder', 'cpalead',
      'ogads', 'cpagrip', 'cpamatica', 'cpaway', 'cpabuild', 'cpalock', 'cpagetti',
      'mylead', 'mycash', 'cpafile', 'cpastack', 'cpaprofit', 'cpagenius',
      'seo', '搜索引擎优化', '关键词', 'backlink', '外链', 'ahrefs', 'semrush',
      'moz', 'majestic', 'spyfu', 'serpstat', 'kwfinder', 'long tail pro',
      'wordtracker', 'ubersuggest', 'answerthepublic', 'google trends', 'trends',
      'google analytics', 'ga', 'google search console', 'gsc', 'bing webmaster',
      'yandex webmaster', '百度统计', '百度站长', '5118', '爱站', 'chinaz',
      '站长工具', 'seoquake', 'seo minion', 'linkminer', 'buzzsumo', 'buzzstream',
      'niche', '利基', 'niche finder', 'niche research', 'keyword research',
      '内容营销', 'content marketing', 'copywriting', '文案', '写作',
      '邮件营销', 'email marketing', 'edm', 'mailchimp', 'convertkit', 'getresponse',
      'aweber', 'activecampaign', 'klaviyo', 'omnisend', 'sendinblue', 'mailerlite',
      'moosend', 'benchmark', 'campaign monitor', 'constant contact', 'sendgrid',
      'mailgun', 'postmark', 'sparkpost', 'amazon ses', 'sendpulse', 'mailjet',
      'smtp', '邮件发送', '邮件验证', 'email verification', 'neverbounce', 'zerobounce',
      'briteverify', 'kickbox', 'emaillistverify', 'emailchecker', 'debounce',
      'clearout', 'bouncer', 'proofy', 'thechecker', 'millionverifier',
      '社交媒体管理', 'social media management', 'buffer', 'hootsuite', 'sprout social',
      'later', 'planoly', 'tailwind', 'meetedgar', 'missinglettr', 'dlvrit',
      'socialoomph', 'socialpilot', 'eclincher', 'agorapulse', 'sendible',
      'contentstudio', 'publer', 'loomly', 'khoros', 'sprinklr', 'emplifi',
      'falcon.io', 'brandwatch', 'mention', 'awario', 'brand24', 'talkwalker',
      'meltwater', 'digimind', 'netbase', 'quid', 'social listening', '社交聆听',
      '舆情监控', '品牌监控', 'influencer', '网红', 'kol', 'koc', '达人',
      'upfluence', 'aspireiq', 'grin', 'creatoriq', 'linqia', 'mavrck',
      'traackr', 'onalytica', ' Julius', 'heepsy', 'modash', 'hypeauditor',
      'influencity', 'starngage', 'noxinfluencer', 'socialblade', 'social blade'],
     '跨境推广'),

    # 数字货币
    (['比特币', 'bitcoin', 'btc', '以太坊', 'ethereum', 'eth', '加密货币', 'cryptocurrency',
      'crypto', '数字货币', '虚拟货币', '区块链', 'blockchain', '交易所', 'exchange',
      'binance', '币安', 'okx', 'okex', 'huobi', '火币', 'coinbase', 'kraken',
      'bitfinex', 'bitstamp', 'gemini', 'bittrex', 'poloniex', 'kucoin', 'gate.io',
      'mexc', '抹茶', 'bybit', 'ftx', 'deribit', 'bitmex', 'okcoin', 'zb',
      '中币', 'bithumb', 'upbit', 'coinone', 'korbit', 'gopax', 'indodax',
      'tokocrypto', 'zipmex', 'coins.ph', 'coinhako', 'crypto.com', 'kraken',
      '钱包', 'wallet', 'metamask', '小狐狸', 'trust wallet', 'imtoken', 'tokenpocket',
      'math wallet', '麦子钱包', 'atomic wallet', 'exodus', 'jaxx', 'coinomi',
      'edge', 'bread', 'mycelium', 'samourai', 'wasabi', 'electrum', 'ledger',
      'trezor', 'keepkey', 'coolwallet', 'bitbox', 'secux', 'ellipal', 'ngrave',
      'cobo', 'hoosat', 'bitpay', 'coinbase commerce', 'coinpayments', 'gourl',
      'blockonomics', 'coingate', 'coinify', 'spectrocoin', 'btcpay', 'btcpayserver',
      'nowpayments', 'plisio', 'coinremitter', 'amlnode', 'coinsbank',
      '行情', 'market', 'coinmarketcap', 'cmc', 'coingecko', 'messari', 'coinpaprika',
      'cryptocompare', 'worldcoinindex', 'coinlib', 'coincodex', 'coincheckup',
      'onchainfx', 'coin360', 'cryptosheets', 'cryptorank', 'icodrops', 'icotracker',
      'icobench', 'icorating', 'icoholder', 'tokentrove', 'nft', '非同质化代币',
      'opensea', 'rarible', 'foundation', 'superrare', 'knownorigin', 'mintable',
      'enjin', 'wax', 'decentraland', 'sandbox', 'axie infinity', 'gods unchained',
      'sorare', 'nba top shot', 'veve', 'curio', 'nifty gateway', 'makersplace',
      'async art', 'hic et nunc', 'objkt', 'kalamint', 'hicetnunc', 'teia',
      'defi', '去中心化金融', 'uniswap', 'sushiswap', 'pancakeswap', 'curve',
      'balancer', 'aave', 'compound', 'maker', 'synthetix', 'yearn', 'convex',
      'lido', 'rocket pool', 'stakehound', 'stakefish', 'everstake', 'figment',
      'p2p', 'p2p交易', 'localbitcoins', 'paxful', 'bisq', 'hodl hodl', 'agoradesk',
      'bitquick', 'coincola', '可盈可乐', 'otc', '场外交易', '挖矿', 'mining',
      '矿池', 'mining pool', 'f2pool', '鱼池', 'antpool', '蚁池', 'slushpool',
      'btc.com', 'via btc', 'viabtc', 'poolin', '币印', 'btc.top', 'bw.com',
      '1hash', '58coin', 'hashnest', 'genesis mining', 'nicehash', 'minergate',
      'hashflare', 'cloud mining', '云挖矿', '矿机', 'miner', 'antminer', '蚂蚁矿机',
      'whatsminer', '神马矿机', 'innosilicon', '芯动', 'avalon', '阿瓦隆',
      'bitmain', '比特大陆', 'microbt', 'ebang', 'canaan', '嘉楠耘智'],
     '数字货币'),

    # 技术/开发
    (['开发', 'developer', '编程', 'programming', '代码', 'code', 'github', 'git',
      'stack overflow', 'stackoverflow', 'csdn', '掘金', 'juejin', 'segmentfault',
      '思否', 'v2ex', '开源', 'open source', 'gitee', '码云', 'gitlab', 'bitbucket',
      'coding', '云开发', 'serverless', '云计算', 'cloud computing', 'aws', 'amazon web services',
      'azure', '阿里云', 'aliyun', '腾讯云', 'tencent cloud', '华为云', 'huawei cloud',
      '百度云', 'baidu cloud', '谷歌云', 'google cloud', 'gcp', 'ibm cloud', 'oracle cloud',
      'digitalocean', 'vultr', 'linode', '搬瓦工', 'bandwagonhost', 'vps', '虚拟主机',
      'web hosting', 'hosting', '域名', 'domain', 'namecheap', 'godaddy', 'namesilo',
      'cloudflare', 'cdn', '加速', 'dns', '域名解析', '容器', 'docker', 'kubernetes',
      'k8s', '数据库', 'database', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
      'api', '接口', 'postman', 'insomnia', 'swagger', 'rap2', 'yapi', 'eolinker',
      'apizza', 'apifox', 'showdoc', 'apidoc', '蓝湖', 'lanhu', 'figma', 'sketch',
      'adobe xd', '摹客', 'mockplus', '墨刀', 'modao', 'axure', 'visio', 'processon',
      '在线作图', '流程图', '思维导图', 'mindmap', 'xmind', 'mindmanager', 'freemind',
      '幕布', 'mubu', 'notion', '语雀', 'yuque', '飞书', 'feishu', '钉钉', 'dingtalk',
      '企业微信', 'wecom', 'slack', 'teams', 'zoom', '腾讯会议', '飞书会议',
      '项目管理', 'project management', 'jira', 'trello', 'asana', 'monday', 'clickup',
      'wrike', 'basecamp', 'notion', 'coda', 'airtable', 'nocoDB', 'baserow',
      '低代码', 'low code', '无代码', 'no code', '宜搭', '明道云', '简道云',
      '氚云', '轻流', 'teambition', 'tower', 'worktile', 'pingcode', 'ones',
      '禅道', 'zentao', 'tapd', 'leangoo', 'cornerstone', 'redmine',
      '文德数慧', 'vendetech', '远想云', 'yuanxiangtech', '浪潮', 'inspur', '华信数据',
      'cloudlight', '奥远电子', 'allrun', '九鼎瑞信', 'evercreative', '中创云讯',
      'bubaocloud', '北银金科', 'bobfintech', '光音网络', 'goyoo', 'authing',
      'moka', 'mokahr', '奇妙时光', 'mzboss', '国云科技', 'g-cloud', '猫灵网络',
      'maoln', 'ai数据', '大数据', 'big data', '数据分析', 'data analysis',
      '数据可视化', 'data visualization', 'tableau', 'power bi', 'finebi', '帆软',
      'superset', 'metabase', 'grafana', 'kibana', 'echarts', 'd3.js', 'chart.js',
      '爬虫', 'crawler', 'scrapy', 'selenium', 'playwright', 'puppeteer',
      '前嗅大数据', 'forenose', '八爪鱼', 'bazhuayu', '后羿采集器', 'houyi',
      '火车采集器', 'locoy', 'webscraper', 'import.io', 'parsehub', 'octoparse',
      'dexi', 'mozenda', 'diffbot', 'scrapingbee', 'scraperapi', 'scrapingdog',
      'proxycrawl', 'crawlbase', 'zenrows', 'bright data', 'oxylabs', 'apify',
      'phantombuster', 'diggernaut', 'outwit', 'fminer', 'visual scraper',
      'content grabber', 'uipath', 'automation anywhere', 'blue prism', 'rpa',
      '影刀', 'yingdao', '实在智能', 'zhineng', '来也', 'laiye', '弘玑', 'cyclone',
      '云扩', 'encootech', '艺赛旗', 'isisoft', '金智维', 'kingware', '达观数据',
      'datagrand', '第四范式', '4paradigm', '明略科技', 'mininglamp', '九章云极',
      'datacanvas', '星环科技', 'transwarp', '偶数科技', 'oushu', '涛思数据', 'taosdata',
      'pingcap', 'tidb', 'oceanbase', 'polardb', 'gaussdb', 'opengauss',
      'authing', '身份认证', '身份云', 'identity', 'oauth', 'sso', '单点登录',
      'okta', 'auth0', 'onelogin', 'jumpcloud', 'keycloak', 'casdoor', 'authing'],
     '技术交流'),
]

def match_category(site):
    """根据站点信息匹配分类"""
    name = site.get('name', '').lower()
    description = site.get('description', '').lower()
    url = site.get('url', '').lower()
    text = f"{name} {description} {url}"

    best_match = None
    best_score = 0

    for keywords, category in CATEGORY_RULES:
        score = 0
        for kw in keywords:
            if kw.lower() in text:
                # 名称中匹配权重更高
                if kw.lower() in name:
                    score += 3
                elif kw.lower() in description:
                    score += 2
                else:
                    score += 1

        if score > best_score:
            best_score = score
            best_match = category

    return best_match, best_score


def main():
    # 读取抓取结果（最新的zvcard文件）
    raw_dir = os.path.join(PROJECT_ROOT, 'raw')
    zvcard_files = sorted([f for f in os.listdir(raw_dir) if f.startswith('zvcard') and f.endswith('.json')],
                           reverse=True)
    if not zvcard_files:
        print('未找到zvcard抓取结果文件')
        return

    crawl_data = load_json(os.path.join(raw_dir, zvcard_files[0]))
    sites = crawl_data.get('sites', [])
    print(f'读取抓取结果: {zvcard_files[0]}')
    print(f'站点总数: {len(sites)}')

    # 读取当前分类体系
    nav_data = load_json(os.path.join(PROJECT_ROOT, '完整版导航.json'))
    existing_categories = [g['name'] for g in nav_data.get('groups', [])]
    print(f'现有分类数: {len(existing_categories)}')

    # 自动分类映射
    mapped_count = 0
    unmapped_count = 0
    category_stats = {}

    for site in sites:
        category, score = match_category(site)
        if category and category in existing_categories:
            site['category'] = category
            mapped_count += 1
            category_stats[category] = category_stats.get(category, 0) + 1
        else:
            site['category'] = '未分类'
            unmapped_count += 1

    print(f'\n自动映射结果:')
    print(f'  已映射: {mapped_count}个')
    print(f'  未映射: {unmapped_count}个')
    print(f'\n分类统计:')
    for cat, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        print(f'  {cat}: {count}个')

    if unmapped_count > 0:
        print(f'\n未映射站点（前10个）:')
        unmapped = [s for s in sites if s['category'] == '未分类']
        for s in unmapped[:10]:
            print(f"  - {s['name']}: {s['url'][:60]}")

    # 保存映射后的结果
    crawl_data['sites'] = sites
    crawl_data['categories'] = [{'name': k, 'count': v} for k, v in sorted(category_stats.items(), key=lambda x: x[1], reverse=True)]
    output_file = os.path.join(raw_dir, 'zvcard导航_已分类.json')
    save_json(crawl_data, output_file)
    print(f'\n映射结果已保存: {output_file}')

    return crawl_data


if __name__ == '__main__':
    main()
