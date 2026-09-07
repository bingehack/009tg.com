"""
深入分析 aididai.cn 工具卡片结构
"""
from bs4 import BeautifulSoup
import re

with open('aididai_home.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# 查找所有h3（工具名称）
h3_list = soup.find_all('h3')
print(f'找到 {len(h3_list)} 个h3元素')

# 分析前5个h3的父元素结构
print('\n=== 前5个h3的完整父元素结构 ===')
for i, h3 in enumerate(h3_list[:5]):
    parent = h3.parent
    grandparent = parent.parent if parent else None
    print(f'\n--- h3[{i}]: {h3.get_text().strip()[:30]} ---')
    print(f'  parent tag: {parent.name if parent else "None"}, class: {parent.get("class") if parent else "None"}')
    print(f'  grandparent tag: {grandparent.name if grandparent else "None"}, class: {grandparent.get("class") if grandparent else "None"}')
    # 打印parent的完整HTML（截断）
    if parent:
        html_str = str(parent)
        print(f'  parent HTML (前800字符):')
        print(f'  {html_str[:800]}')

# 查找包含工具URL的元素（data属性、onclick等）
print('\n=== 查找包含URL的data属性 ===')
url_pattern = re.compile(r'https?://[^\s"\'<>]+')
elements_with_url = []
for tag in soup.find_all(True):
    for attr, value in tag.attrs.items():
        if isinstance(value, str) and url_pattern.search(value):
            if 'aididai.cn' not in value and 'wordpress' not in value and 'w3.org' not in value:
                elements_with_url.append((tag.name, attr, value[:100]))

print(f'找到 {len(elements_with_url)} 个含外部URL的属性')
for tag, attr, url in elements_with_url[:20]:
    print(f'  <{tag} {attr}="{url}">')

# 查找"查看全部"链接
print('\n=== 查找"查看全部"链接 ===')
for a in soup.find_all('a', string=re.compile(r'查看全部|更多|all')):
    print(f'  {a.get_text().strip()} -> {a.get("href")}')

# 查找分类导航菜单
print('\n=== 查找导航菜单 ===')
nav = soup.find('nav')
if nav:
    links = nav.find_all('a', href=True)
    print(f'导航菜单找到 {len(links)} 个链接')
    for a in links[:30]:
        text = a.get_text().strip()
        href = a.get('href')
        if text:
            print(f'  {text[:20]:20s} -> {href}')

# 查找所有内部链接（可能是分类页）
print('\n=== 查找内部链接模式 ===')
internal_links = set()
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.startswith('/') or 'aididai.cn' in href:
        # 提取路径模式
        if 'aididai.cn' in href:
            path = href.split('aididai.cn')[-1]
        else:
            path = href
        if path and path != '/' and not path.startswith('/wp-') and not path.startswith('/?'):
            internal_links.add(path)

print(f'找到 {len(internal_links)} 个内部链接路径')
for path in sorted(internal_links)[:40]:
    print(f'  {path}')
