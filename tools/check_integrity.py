import json
import os

# 读取JSON
with open('完整版导航.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计站点数和ID
site_ids = set()
total = 0
for group in data.get('groups', []):
    for site in group.get('sites', []):
        total += 1
        sid = site.get('id')
        if sid:
            site_ids.add(str(sid))

print('JSON中站点总数:', total)
print('JSON中唯一ID数:', len(site_ids))

# 检查重复ID
if total != len(site_ids):
    print('警告: 存在重复ID或缺失ID!')

# 检查详情页文件
cn_site_dir = 'cn/site'
en_site_dir = 'en/site'
cn_files = set(f.replace('.html', '') for f in os.listdir(cn_site_dir) if f.endswith('.html'))
en_files = set(f.replace('.html', '') for f in os.listdir(en_site_dir) if f.endswith('.html'))

print('cn/site/ 详情页数:', len(cn_files))
print('en/site/ 详情页数:', len(en_files))

# 找出缺失的详情页
missing_cn = site_ids - cn_files
missing_en = site_ids - en_files
extra_cn = cn_files - site_ids
extra_en = en_files - site_ids

print('缺失的中文详情页:', len(missing_cn))
if missing_cn and len(missing_cn) <= 10:
    print('  ', list(missing_cn)[:10])
print('缺失的英文详情页:', len(missing_en))
if missing_en and len(missing_en) <= 10:
    print('  ', list(missing_en)[:10])
print('多余的中文详情页:', len(extra_cn))
print('多余的英文详情页:', len(extra_en))

# 检查默认favicon
default_icon = 'assets/images/logos/default.png'
if os.path.exists(default_icon):
    print('默认favicon存在:', default_icon)
else:
    print('警告: 默认favicon不存在!', default_icon)

# 检查favicon目录
favicon_dir = 'assets/images/logos'
if os.path.exists(favicon_dir):
    icons = [f for f in os.listdir(favicon_dir) if f.endswith(('.png', '.ico', '.jpg', '.svg'))]
    print('favicon图标文件数:', len(icons))

# 检查站点是否缺少必要字段
missing_url = 0
missing_name = 0
missing_id = 0
for group in data.get('groups', []):
    for site in group.get('sites', []):
        if not site.get('url'):
            missing_url += 1
        if not site.get('name'):
            missing_name += 1
        if not site.get('id'):
            missing_id += 1
print('缺少url的站点:', missing_url)
print('缺少name的站点:', missing_name)
print('缺少id的站点:', missing_id)
