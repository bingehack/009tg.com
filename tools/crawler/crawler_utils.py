#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crawler_utils.py - 导航站抓取通用工具模块

提供抓取脚本共用的基础功能：
- HTTP 请求封装（随机UA、重试、延迟、超时）
- 域名提取与去重
- 现有站点域名加载
- raw 格式输出（直接可被 build_data.py 合并）
- 文本清洗
- 分类名转安全文件名

使用方式：
    from crawler_utils import fetch_page, get_domain, load_existing_domains, save_raw_output, clean_text
"""

import os
import re
import json
import time
import random
import hashlib
from urllib.parse import urlparse, urljoin
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None

# ============================================================
# 路径配置
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))  # tools/crawler/ → 项目根
RAW_DIR = os.path.join(PROJECT_ROOT, 'raw')
JSON_PATH = os.path.join(PROJECT_ROOT, '完整版导航.json')

# ============================================================
# User-Agent 池
# ============================================================
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
]


def get_random_headers():
    """获取随机请求头"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }


# ============================================================
# HTTP 请求
# ============================================================
def fetch_page(url, timeout=15, retries=3, delay_range=(1, 3), encoding=None):
    """
    抓取网页内容，带重试和延迟

    Args:
        url: 目标URL
        timeout: 超时时间（秒）
        retries: 重试次数
        delay_range: 请求间隔（秒），随机取范围值
        encoding: 指定编码，None 则自动检测

    Returns:
        str: 页面HTML内容，失败返回 None
    """
    if requests is None:
        raise ImportError('请先安装 requests: pip install requests')

    for attempt in range(retries):
        try:
            headers = get_random_headers()
            response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)

            if response.status_code == 200:
                if encoding:
                    response.encoding = encoding
                else:
                    # 自动检测编码
                    if response.encoding and response.encoding.lower() in ('iso-8859-1', 'ascii'):
                        response.encoding = response.apparent_encoding or 'utf-8'
                return response.text
            else:
                print(f'  [尝试 {attempt+1}/{retries}] HTTP {response.status_code}: {url}')

        except requests.exceptions.Timeout:
            print(f'  [尝试 {attempt+1}/{retries}] 超时: {url}')
        except requests.exceptions.ConnectionError:
            print(f'  [尝试 {attempt+1}/{retries}] 连接失败: {url}')
        except Exception as e:
            print(f'  [尝试 {attempt+1}/{retries}] 错误: {e}')

        if attempt < retries - 1:
            delay = random.uniform(*delay_range)
            time.sleep(delay)

    print(f'  抓取失败（已重试{retries}次）: {url}')
    return None


def polite_sleep(delay_range=(1, 3)):
    """礼貌延迟，避免请求过快"""
    delay = random.uniform(*delay_range)
    time.sleep(delay)


# ============================================================
# 域名与URL处理
# ============================================================
def get_domain(url):
    """从URL提取域名（小写，去掉www前缀和端口号）"""
    try:
        parsed = urlparse(url)
        # 使用hostname去掉端口号，netloc会包含端口
        domain = (parsed.hostname or parsed.netloc).lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except Exception:
        return ''


def normalize_url(url):
    """规范化URL：补全协议、去掉末尾斜杠、去掉锚点"""
    if not url:
        return ''
    url = url.strip()
    # 补全协议
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    # 去掉锚点
    url = url.split('#')[0]
    # 去掉末尾斜杠（保留协议后的//）
    if url.endswith('/') and not url.endswith('//'):
        url = url.rstrip('/')
    return url


def is_valid_site_url(url):
    """判断是否为有效的站点URL（排除内容站、搜索引擎等）"""
    if not url:
        return False

    domain = get_domain(url)
    if not domain:
        return False

    # 排除常见内容站和非工具站
    blocklist = [
        'baidu.com', 'zhihu.com', 'csdn.net', 'jianshu.com', 'weibo.com',
        'bilibili.com', 'douyin.com', 'youtube.com', 'twitter.com', 'facebook.com',
        'instagram.com', 'linkedin.com', 'reddit.com', 'quora.com', 'medium.com',
        'github.com', 'gitee.com', 'stackoverflow.com', 'wikipedia.org',
        'google.com', 'bing.com', 'so.com', 'sogou.com',
        'taobao.com', 'jd.com', 'pinduoduo.com', '1688.com', 'alibaba.com',
        'amazon.com', 'ebay.com', 'shopify.com',
        'qq.com', '163.com', 'sina.com.cn', 'sohu.com', 'ifeng.com',
        'thepaper.cn', '36kr.com', 'huxiu.com', 'iyiou.com',
        'mp.weixin.qq.com', 'toutiao.com', 'kuaishou.com',
    ]

    for blocked in blocklist:
        if domain == blocked or domain.endswith('.' + blocked):
            return False

    return True


# ============================================================
# 去重
# ============================================================
def load_existing_domains(json_path=None):
    """
    从完整版导航.json加载现有站点的域名集合（用于去重）

    Returns:
        set: 域名集合
    """
    if json_path is None:
        json_path = JSON_PATH

    if not os.path.exists(json_path):
        print(f'  警告: JSON文件不存在: {json_path}')
        return set()

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    domains = set()
    for group in data.get('groups', []):
        for site in group.get('sites', []):
            domain = get_domain(site.get('url', ''))
            if domain:
                domains.add(domain)

    return domains


def load_raw_domains(raw_dir=None):
    """
    从 raw/ 目录加载已抓取但尚未合并的站点域名（避免重复抓取）

    Returns:
        set: 域名集合
    """
    if raw_dir is None:
        raw_dir = RAW_DIR

    domains = set()
    if not os.path.exists(raw_dir):
        return domains

    for filename in os.listdir(raw_dir):
        if not filename.endswith('.json') or filename.startswith('_'):
            continue
        filepath = os.path.join(raw_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for site in data.get('sites', []):
                domain = get_domain(site.get('url', ''))
                if domain:
                    domains.add(domain)
        except Exception:
            continue

    return domains


# ============================================================
# 文本清洗
# ============================================================
def clean_text(text):
    """清洗文本：去除多余空格、换行、HTML实体"""
    if not text:
        return ''
    # 去除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 替换HTML实体
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def truncate_text(text, max_len=200):
    """截断文本到指定长度"""
    if not text:
        return ''
    text = clean_text(text)
    if len(text) > max_len:
        text = text[:max_len] + '...'
    return text


# ============================================================
# 文件名处理
# ============================================================
def safe_filename(name):
    """将分类名转换为安全的文件名"""
    # 替换不安全字符
    name = re.sub(r'[\\/:*?"<>|\s]+', '_', name)
    # 限制长度
    if len(name) > 50:
        name = name[:50]
    return name


def generate_output_filename(source_name, category_name):
    """生成输出文件名: {source}_{category}.json"""
    source = safe_filename(source_name)
    category = safe_filename(category_name)
    return f'{source}_{category}.json'


# ============================================================
# raw 格式输出
# ============================================================
def save_raw_output(category_name, sites, source_name='crawler', parent_category=None,
                    output_dir=None, overwrite=False):
    """
    保存抓取结果为 raw 格式 JSON（直接可被 build_data.py 合并）

    Args:
        category_name: 分类名称
        sites: 站点列表，每个元素为 dict，需包含 name, url, description
        source_name: 数据来源标识（用于文件名和追溯）
        parent_category: 父分类名称（可选）
        output_dir: 输出目录，默认 raw/
        overwrite: 是否覆盖已存在的文件

    Returns:
        str: 输出文件路径，失败返回 None
    """
    if output_dir is None:
        output_dir = RAW_DIR

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = generate_output_filename(source_name, category_name)
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath) and not overwrite:
        print(f'  文件已存在，跳过: {filename} (使用 overwrite=True 覆盖)')
        return filepath

    # 构建 raw 格式数据
    raw_data = {
        'category': category_name,
        'source': source_name,
        'updated_at': datetime.now().strftime('%Y-%m-%d'),
        'sites': []
    }

    if parent_category:
        raw_data['parent_category'] = parent_category

    for site in sites:
        name = clean_text(site.get('name', ''))
        url = normalize_url(site.get('url', ''))
        description = truncate_text(site.get('description', ''), 300)
        icon = site.get('icon', '')

        if not name or not url:
            continue

        raw_site = {
            'name': name,
            'url': url,
            'description': description,
            'icon': icon,
            'tags': site.get('tags', []),
            'status': site.get('status', 'verified'),
        }
        raw_data['sites'].append(raw_site)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    print(f'  已保存: {filename} ({len(raw_data["sites"])} 个站点)')
    return filepath


# ============================================================
# 统计输出
# ============================================================
def print_crawl_summary(source_name, categories_count, sites_total, sites_added,
                         sites_skipped_duplicate, sites_skipped_invalid):
    """打印抓取统计摘要"""
    print('\n' + '=' * 50)
    print(f'抓取完成 - {source_name}')
    print('=' * 50)
    print(f'  遍历分类数:     {categories_count}')
    print(f'  提取站点总数:   {sites_total}')
    print(f'  有效新增:       {sites_added}')
    print(f'  跳过(重复):     {sites_skipped_duplicate}')
    print(f'  跳过(无效):     {sites_skipped_invalid}')
    print('=' * 50)
