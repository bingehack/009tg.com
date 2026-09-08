import json
import os

# 读取主数据，获取所有有效站点的id
with open('完整版导航.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

valid_ids = set()
for group in data.get('groups', []):
    for site in group.get('sites', []):
        site_id = site.get('id')
        if site_id:
            valid_ids.add(str(site_id))

print('有效站点ID数:', len(valid_ids))

# 清理cn/site/目录
cn_dir = 'cn/site'
en_dir = 'en/site'

removed_cn = 0
removed_en = 0

if os.path.exists(cn_dir):
    for filename in os.listdir(cn_dir):
        if filename.endswith('.html'):
            site_id = filename.replace('.html', '')
            if site_id not in valid_ids:
                filepath = os.path.join(cn_dir, filename)
                os.remove(filepath)
                removed_cn += 1
                print('  删除:', filepath)

if os.path.exists(en_dir):
    for filename in os.listdir(en_dir):
        if filename.endswith('.html'):
            site_id = filename.replace('.html', '')
            if site_id not in valid_ids:
                filepath = os.path.join(en_dir, filename)
                os.remove(filepath)
                removed_en += 1
                print('  删除:', filepath)

print()
print('清理完成:')
print('  cn/site/ 删除:', removed_cn, '个文件')
print('  en/site/ 删除:', removed_en, '个文件')
print('  总计删除:', removed_cn + removed_en, '个文件')
