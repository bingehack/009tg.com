#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析导航站页面结构"""
import requests
from bs4 import BeautifulSoup
import re
import urllib3
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def analyze(url, name):
    print(f'\n{"="*60}')
    print(f'=== {name}: {url}')
    print(f'{"="*60}')

    resp = requests.get(url, headers=headers, timeout=15, verify=False)
    resp.encoding = resp.apparent_encoding or 'utf-8'
    print(f'页面大小: {len(resp.text)} 字节')
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 统计各种可能的卡片结构
    print(f'\n包含data-url的a标签: {len(soup.find_all("a", attrs={"data-url": True}))}')
    print(f'class含site的a标签: {len(soup.find_all("a", class_=re.compile(r"site", re.I)))}')
    print(f'class含card的元素: {len(soup.find_all(class_=re.compile(r"card", re.I)))}')
    print(f'class含item的元素: {len(soup.find_all(class_=re.compile(r"item", re.I)))}')
    print(f'class含tool的元素: {len(soup.find_all(class_=re.compile(r"tool", re.I)))}')
    print(f'class含link的元素: {len(soup.find_all(class_=re.compile(r"link", re.I)))}')
    print(f'class含nav的元素: {len(soup.find_all(class_=re.compile(r"nav", re.I)))}')
    print(f'class含app的元素: {len(soup.find_all(class_=re.compile(r"app", re.I)))}')
    print(f'class含web的元素: {len(soup.find_all(class_=re.compile(r"web", re.I)))}')

    # 找可能的卡片容器（包含多个a标签的div）
    print(f'\n可能的卡片容器（div内含>=3个a标签）:')
    count = 0
    for div in soup.find_all('div'):
        links = div.find_all('a', href=True)
        if 3 <= len(links) <= 50:
            # 检查是否有class
            cls = div.get('class', [])
            if cls and count < 8:
                print(f'  div class={" ".join(cls)} 链接数={len(links)}')
                count += 1

    # 找包含外链的a标签（http开头且不是本站）
    domain = url.split('/')[2]
    external_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http') and domain not in href:
            text = a.get_text(strip=True)
            if text and len(text) < 50:
                external_links.append((text[:30], href[:60], a.get('class', [])))

    print(f'\n外链数量: {len(external_links)}')
    print('前10个外链:')
    for text, href, cls in external_links[:10]:
        print(f'  {text} -> {href} class={cls}')

# 分析几个站点
analyze('https://www.2345ai.com/', '2345AI导航')
analyze('https://hao.uisdc.com/', '优设导航')
analyze('https://www.aigc.cn/', 'AIGC工具导航')
