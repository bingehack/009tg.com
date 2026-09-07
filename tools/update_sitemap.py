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
    ('sitemap.html', 'weekly', '0.5'),
]
for page, freq, priority in standard_pages:
    urls.append((f'https://009tg.com/cn/{page}', freq, priority))
    urls.append((f'https://009tg.com/en/{page}', freq, priority))

# 分类详情页
for cat_id in category_ids:
    urls.append((f'https://009tg.com/cn/category/{cat_id}.html', 'weekly', '0.7'))
    urls.append((f'https://009tg.com/en/category/{cat_id}.html', 'weekly', '0.7'))

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
