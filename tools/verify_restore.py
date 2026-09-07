import json
with open(r'D:\测试文档\url\009\009tg.com\完整版导航.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
total = sum(len(g.get('sites', [])) for g in d['groups'])
groups_with_sites = sum(1 for g in d['groups'] if len(g.get('sites', [])) > 0)
print(f'恢复后: {len(d["groups"])}分类, {groups_with_sites}个有站点, {total}站点')
# 确认没有id=2001的分类
cat_2001 = [g for g in d['groups'] if g['id'] == 2001]
print(f'id=2001的分类: {len(cat_2001)}个 (应为0)')
