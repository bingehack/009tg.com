"""
分析 aididai.cn 详情页结构，提取真实URL
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler'))
from crawler_utils import fetch_page
from bs4 import BeautifulSoup
import re

# 测试一个详情页
url = 'https://www.aididai.cn/sites/2416.html'
print(f'获取详情页: {url}')
html = fetch_page(url, timeout=15)

if not html:
    print('获取失败')
    sys.exit(1)

print(f'HTML长度: {len(html)}')

# 保存
with open('aididai_detail.html', 'w', encoding='utf-8') as f:
    f.write(html)

soup = BeautifulSoup(html, 'html.parser')

# 查找所有外链
print('\n=== 所有外链 ===')
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.startswith('http') and 'aididai.cn' not in href and 'beian' not in href:
        text = a.get_text().strip()[:50]
        print(f'  {text:50s} -> {href}')

# 查找/go/跳转链接
print('\n=== /go/ 跳转链接 ===')
for a in soup.find_all('a', href=True):
    href = a['href']
    if '/go/' in href or '/go?' in href:
        text = a.get_text().strip()[:50]
        print(f'  {text:50s} -> {href}')

# 查找"访问网站"或"立即访问"按钮
print('\n=== 访问按钮 ===')
for a in soup.find_all('a', string=re.compile(r'访问|进入|官网|打开|Visit|Go')):
    print(f'  {a.get_text().strip():30s} -> {a.get("href")}')

# 查找包含URL的data属性
print('\n=== 含URL的data属性 ===')
for tag in soup.find_all(True):
    for attr, value in tag.attrs.items():
        if isinstance(value, str) and re.search(r'https?://', value):
            if 'aididai.cn' not in value and 'wordpress' not in value and 'w3.org' not in value:
                print(f'  <{tag.name} {attr}="{value[:80]}">')

# 查找页面标题
title = soup.find('title')
if title:
    print(f'\n页面标题: {title.get_text()}')

# 查找og:url
og_url = soup.find('meta', property='og:url')
if og_url:
    print(f'og:url: {og_url.get("content")}')
