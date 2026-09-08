import json

# 读取确认失败的站点
with open('confirmed_dead_sites.json', 'r', encoding='utf-8') as f:
    dead_sites = json.load(f)

# 提取需要删除的URL
dead_urls = set()
for item in dead_sites:
    url = item['site'].get('url', '')
    if url:
        dead_urls.add(url)

print('需要删除的站点数:', len(dead_urls))

# 读取主数据
with open('完整版导航.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 删除站点
total_before = 0
total_after = 0
removed_count = 0

for group in data.get('groups', []):
    sites = group.get('sites', [])
    total_before += len(sites)
    
    new_sites = []
    for site in sites:
        url = site.get('url', '')
        if url in dead_urls:
            removed_count += 1
            print('  删除:', site.get('name', ''), '-', url)
        else:
            new_sites.append(site)
    
    group['sites'] = new_sites
    total_after += len(new_sites)

print()
print('删除前总站点数:', total_before)
print('删除后总站点数:', total_after)
print('实际删除数:', removed_count)

# 保存
with open('完整版导航.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print()
print('已保存到 完整版导航.json')
