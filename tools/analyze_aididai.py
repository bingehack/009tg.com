"""
分析 aididai.cn 的HTML结构，确定抓取选择器
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler'))
from crawler_utils import fetch_page, clean_text

url = 'https://www.aididai.cn'
print(f'正在获取: {url}')
html = fetch_page(url, timeout=15)

if not html:
    print('获取失败')
    sys.exit(1)

print(f'HTML长度: {len(html)} 字符')

# 保存原始HTML供分析
with open('aididai_home.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('已保存到 aididai_home.html')

# 用BeautifulSoup分析结构
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# 查找分类标题
print('\n=== 查找分类标题 ===')
# 尝试常见的分类容器选择器
for selector in ['h2', 'h3', '.category-title', '.cat-title', '.section-title', '.nav-item', '.category']:
    elements = soup.select(selector)
    if elements:
        print(f'\n{selector}: 找到 {len(elements)} 个')
        for el in elements[:10]:
            text = clean_text(el.get_text())
            if text and len(text) < 50:
                print(f'  - {text}')

# 查找工具卡片
print('\n=== 查找工具卡片 ===')
for selector in ['.tool-card', '.site-card', '.card', '.item', '.tool-item', '.site-item', 'li', 'article']:
    elements = soup.select(selector)
    if elements and len(elements) > 5:
        # 检查是否包含链接
        with_links = [el for el in elements if el.find('a')]
        if with_links:
            print(f'\n{selector}: 找到 {len(elements)} 个, 其中 {len(with_links)} 个含链接')
            # 打印第一个的结构
            if with_links:
                print('  第一个卡片HTML结构:')
                print(str(with_links[0])[:500])
            break

# 查找所有外链
print('\n=== 查找外链结构 ===')
external_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.startswith('http') and 'aididai.cn' not in href:
        text = clean_text(a.get_text())
        if text:
            external_links.append((text, href))

print(f'找到 {len(external_links)} 个外链')
for text, href in external_links[:15]:
    print(f'  {text[:30]:30s} -> {href}')

# 查找分类页面链接
print('\n=== 查找分类页面链接 ===')
cat_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    text = clean_text(a.get_text())
    if ('/category' in href or '/cat' in href or '/list' in href) and text:
        cat_links.append((text, href))

print(f'找到 {len(cat_links)} 个分类链接')
for text, href in cat_links[:20]:
    print(f'  {text[:30]:30s} -> {href}')
