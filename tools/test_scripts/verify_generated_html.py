import re
import json

# 读取生成的HTML
with open(r'D:\测试文档\url\009\009tg.com\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 提取所有 allSitesData 条目并统计站点数
pattern = r"allSitesData\['([^']+)'\] = (\[.*?\]);"
matches = re.findall(pattern, html, re.DOTALL)
print(f'有站点的分类数: {len(matches)}')

total_sites_in_html = 0
category_counts = []
for cat_name, sites_json in matches:
    try:
        sites = json.loads(sites_json)
        total_sites_in_html += len(sites)
        category_counts.append((cat_name, len(sites)))
    except Exception as e:
        print(f'  解析失败 {cat_name}: {e}')

print(f'HTML中嵌入的站点总数: {total_sites_in_html}')

# 与JSON对比
with open(r'D:\测试文档\url\009\009tg.com\完整版导航.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
json_sites = sum(len(g.get('sites',[])) for g in data['groups'])
print(f'JSON中groups的站点总数: {json_sites}')
print(f'数量一致: {total_sites_in_html == json_sites}')

# 2. HTML结构完整性
print('\n=== HTML结构检查 ===')
print(f'包含 <!DOCTYPE html>: {"<!DOCTYPE html>" in html}')
print(f'<html> 标签: {html.count("<html")} 个开, {html.count("</html>")} 个闭')
print(f'<head> 标签: {html.count("<head>")} 个开, {html.count("</head>")} 个闭')
print(f'<body> 标签: {html.count("<body")} 个开, {html.count("</body>")} 个闭')
print(f'<script> 标签: {html.count("<script")} 个开, {html.count("</script>")} 个闭')
print(f'包含 main-menu 导航: {"id=\"main-menu\"" in html}')
print(f'包含 allSitesData 初始化: {"var allSitesData" in html}')
print(f'包含 changePage 函数: {"function changePage" in html}')
print(f'包含 $(document).ready: {"$(document).ready" in html}')

# 3. 检查前几个和后几个分类
print('\n=== 分类站点数分布(前5/后5) ===')
for name, cnt in category_counts[:5]:
    print(f'  {name}: {cnt}')
print('  ...')
for name, cnt in category_counts[-5:]:
    print(f'  {name}: {cnt}')
