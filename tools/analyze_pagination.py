"""
快速分析AI地带分类页的分页结构
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler'))
from crawler_utils import fetch_page
from bs4 import BeautifulSoup
import re

# 测试AI图像工具分类的第2页
base = 'https://www.aididai.cn/favorites/ai%e5%9b%be%e5%83%8f%e5%b7%a5%e5%85%b7'

# 尝试几种分页格式
candidates = [
    f'{base}/page/2/',
    f'{base}?page=2',
    f'{base}?paged=2',
    f'{base}/2/',
]

for url in candidates:
    print(f'\n尝试: {url}')
    html = fetch_page(url, timeout=10, retries=1)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('a.sites-body')
        title = soup.find('title')
        print(f'  状态: OK, 工具卡片数: {len(cards)}, 标题: {title.get_text()[:50] if title else "N/A"}')
        # 查找分页导航
        pagination = soup.select('.pagination, .nav-links, .page-numbers, .wp-pagenavi')
        if pagination:
            print(f'  找到分页元素: {pagination[0].name}.{pagination[0].get("class")}')
            # 打印分页链接
            links = pagination[0].find_all('a', href=True)
            for a in links[:10]:
                print(f'    {a.get_text().strip():10s} -> {a["href"]}')
    else:
        print(f'  状态: 失败')
