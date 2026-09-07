import json
import os

os.chdir(r'D:\测试文档\url\009\009tg.com')

with open('完整版导航.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

total = sum(len(g.get('sites', [])) for g in d['groups'])
groups_with_sites = sum(1 for g in d['groups'] if len(g.get('sites', [])) > 0)

print(f'分类总数: {len(d["groups"])}')
print(f'有站点的分类: {groups_with_sites}')
print(f'站点总数: {total}')
print(f'JSON大小: {os.path.getsize("完整版导航.json")} 字节')
print(f'index.html大小: {os.path.getsize("index.html")} 字节')

# 验证HTML中嵌入的站点数
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
import re
# 查找 allSitesData 中的站点数量
match = re.search(r'const allSitesData\s*=\s*(\{.*?\});', html, re.DOTALL)
if match:
    sites_data = json.loads(match.group(1))
    html_sites = sum(len(v) for v in sites_data.values())
    print(f'HTML中嵌入的站点数: {html_sites}')
else:
    print('未找到allSitesData')
