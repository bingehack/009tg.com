#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新sitemap.xml，加入分类详情页链接"""

import json
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# 读取JSON数据
with open(os.path.join(project_root, '完整版导航.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

# 收集所有分类ID
category_ids = []
for group in data['groups']:
    category_ids.append(group['id'])

print(f"共 {len(category_ids)} 个分类")

# 生成sitemap内容
today = datetime.now().strftime('%Y-%m-%d')

urls = []

# 首页
urls.append(('https://009tg.com/', 'daily', '1.0'))
urls.append(('https://009tg.com/cn/', 'daily', '0.9'))
urls.append(('https://009tg.com/en/', 'daily', '0.9'))

# 标准页面
standard_pages = [
    ('about.html', 'monthly', '0.6'),
    ('privacy.html', 'yearly', '0.4'),
    ('terms.html', 'yearly', '0.4'),
    ('contact.html', 'monthly', '0.5'),
    ('disclaimer.html', 'yearly', '0.4'),
    ('sitemap.html', 'weekly', '0.5'),
]
for page, freq, priority in standard_pages:
    urls.append((f'https://009tg.com/cn/{page}', freq, priority))
    urls.append((f'https://009tg.com/en/{page}', freq, priority))

# 分类详情页
for cat_id in category_ids:
    urls.append((f'https://009tg.com/cn/category/{cat_id}.html', 'weekly', '0.7'))
    urls.append((f'https://009tg.com/en/category/{cat_id}.html', 'weekly', '0.7'))

# 文章页面
article_count = 0
articles_path = os.path.join(project_root, 'data', 'articles.json')
if os.path.exists(articles_path):
    with open(articles_path, 'r', encoding='utf-8') as f:
        articles_data = json.load(f)
    articles = [a for a in articles_data.get('articles', []) if a.get('isPublic', True)]
    article_count = len(articles)
    # 文章列表页
    urls.append(('https://009tg.com/cn/articles.html', 'weekly', '0.8'))
    urls.append(('https://009tg.com/en/articles.html', 'weekly', '0.8'))
    # 文章详情页
    for article in articles:
        urls.append((f'https://009tg.com/cn/article/{article["id"]}.html', 'monthly', '0.6'))
        urls.append((f'https://009tg.com/en/article/{article["id"]}.html', 'monthly', '0.6'))

# 站点详情页
site_ids = []
def collect_sites(group):
    for site in group.get('sites', []):
        site_ids.append(site['id'])
    for child in group.get('children', []):
        collect_sites(child)
for g in data['groups']:
    collect_sites(g)

for site_id in site_ids:
    urls.append((f'https://009tg.com/cn/site/{site_id}.html', 'monthly', '0.5'))
    urls.append((f'https://009tg.com/en/site/{site_id}.html', 'monthly', '0.5'))

# 生成XML
xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

for loc, freq, priority in urls:
    xml_content += f'''    <url>
        <loc>{loc}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>{freq}</changefreq>
        <priority>{priority}</priority>
    </url>
'''

xml_content += '</urlset>\n'

# 写入文件
sitemap_path = os.path.join(project_root, 'sitemap.xml')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(xml_content)

print(f"sitemap.xml 已更新，共 {len(urls)} 个URL")
print(f"  - 首页: 3")
print(f"  - 标准页面: {len(standard_pages) * 2}")
print(f"  - 分类详情页: {len(category_ids) * 2}")
print(f"  - 文章页面: {article_count * 2 + 2 if article_count else 0}")
print(f"  - 站点详情页: {len(site_ids) * 2}")
