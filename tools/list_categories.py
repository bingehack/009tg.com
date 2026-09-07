"""
查看站点现有分类结构，特别是AI相关分类
"""
import json
import os

os.chdir(r'D:\测试文档\url\009\009tg.com')

with open('完整版导航.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

groups = data['groups']

# 构建分类树
print("=" * 70)
print("站点现有分类结构（一级分类 → 子分类）")
print("=" * 70)

# 先找一级分类（parent_id为null）
top_level = [g for g in groups if g.get('parent_id') is None]
top_level.sort(key=lambda x: x.get('order_num', 0))

for top in top_level:
    children = [g for g in groups if g.get('parent_id') == top['id']]
    children.sort(key=lambda x: x.get('order_num', 0))
    child_count = len(children)
    site_count = len(top.get('sites', []))
    total_sites = site_count + sum(len(c.get('sites', [])) for c in children)

    print(f"\n【{top['name']}】 (id={top['id']}, {child_count}个子分类, {total_sites}个站点)")
    if children:
        for child in children:
            cs = len(child.get('sites', []))
            print(f"  ├─ {child['name']} (id={child['id']}, {cs}个站点)")
    else:
        print(f"  (无子分类，直接有 {site_count} 个站点)")

# 专门列出AI相关分类
print("\n" + "=" * 70)
print("AI相关分类筛选")
print("=" * 70)
ai_keywords = ['AI', 'ai', '人工智能', '大模型', 'GPT', 'ChatGPT', '工具']
for g in groups:
    name = g['name']
    if any(kw in name for kw in ai_keywords):
        site_count = len(g.get('sites', []))
        parent = next((p['name'] for p in groups if p['id'] == g.get('parent_id')), '一级')
        print(f"  {name} (id={g['id']}, 父={parent}, {site_count}个站点)")
