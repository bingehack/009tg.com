import json
import re

with open('完整版导航.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('connection_failed_sites.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 提取确认失败的站点URL
failed_urls = re.findall(r'https?://[^\s<"]+', html)
print('报告中提取到', len(failed_urls), '个URL')

# 找出所有站点
all_sites = []
for group in data.get('groups', []):
    for site in group.get('sites', []):
        all_sites.append((group.get('name', ''), site))

print('数据中共有', len(all_sites), '个站点')
print()
print('确认失败的站点:')
count = 0
failed_sites = []
for group_name, site in all_sites:
    url = site.get('url', '')
    for fu in failed_urls:
        if url and fu in url:
            count += 1
            failed_sites.append({'group': group_name, 'site': site})
            print(' ', count, '. [', group_name, ']', site.get('name', ''), '-', url)
            break
print('... 共', count, '个匹配')

# 保存确认失败的站点列表
with open('confirmed_dead_sites.json', 'w', encoding='utf-8') as f:
    json.dump(failed_sites, f, ensure_ascii=False, indent=2)
print()
print('已保存到 confirmed_dead_sites.json')
