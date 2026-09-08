import re
import os

def extract_footer_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    # 找到<footer class="site-footer">到</footer>之间的内容
    match = re.search(r'<footer class="site-footer">(.*?)</footer>', html, re.DOTALL)
    if not match:
        return None
    footer = match.group(1)
    links = re.findall(r'<a href="([^"]+)">([^<]+)</a>', footer)
    return links

pages = [
    ('首页', 'cn/index.html'),
    ('分类页', 'cn/category/1.html'),
    ('详情页', 'cn/site/1.html'),
    ('标准页-联系', 'cn/contact.html'),
    ('英文首页', 'en/index.html'),
    ('英文分类页', 'en/category/1.html'),
    ('英文详情页', 'en/site/1.html'),
    ('英文标准页', 'en/contact.html'),
]

for name, path in pages:
    if not os.path.exists(path):
        print(name, ': 文件不存在 -', path)
        continue
    links = extract_footer_links(path)
    if links is None:
        print(name, ': 没有找到site-footer!')
        continue
    print('===', name, '(', path, ')===')
    for href, text in links:
        # 检查链接目标文件是否存在
        dir_name = os.path.dirname(path)
        target = os.path.normpath(os.path.join(dir_name, href))
        exists = os.path.exists(target)
        status = 'OK' if exists else 'BROKEN'
        print('  [{}] {} -> {}'.format(status, text, href))
    print()
