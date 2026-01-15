import json
import os
import shutil
from datetime import datetime

def load_json_file(file_path):
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data, file_path):
    """保存JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def extract_invalid_sites_from_html(html_file):
    """从HTML报告中提取无效网站的URL"""
    invalid_urls = set()
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # 提取所有href中的URL（更精确的匹配）
        import re
        pattern = r'href="(https://[^"]+)" target="_blank"'
        matches = re.findall(pattern, content)
        invalid_urls.update(matches)
    
    return list(invalid_urls)

def remove_sites_from_data(data, invalid_urls):
    """从JSON数据中删除指定的站点"""
    removed_count = 0
    invalid_urls_set = set(invalid_urls)
    
    # 处理dict格式的数据（包含groups字段）
    if isinstance(data, dict):
        if 'groups' in data and isinstance(data['groups'], list):
            for group in data['groups']:
                if 'sites' in group and isinstance(group['sites'], list):
                    new_sites = []
                    for site in group['sites']:
                        url = site.get('url', '')
                        # 检查URL是否在无效列表中
                        if url in invalid_urls_set:
                            removed_count += 1
                            print(f"删除: {site.get('name', '未知')} - {url}")
                        else:
                            new_sites.append(site)
                    group['sites'] = new_sites
        return data, removed_count
    
    # 处理list格式的数据
    if isinstance(data, list):
        new_data = []
        for item in data:
            if 'list' in item and isinstance(item['list'], list):
                new_list = []
                for site in item['list']:
                    url = site.get('url', '')
                    # 检查URL是否在无效列表中
                    if url in invalid_urls_set:
                        removed_count += 1
                        print(f"删除: {site.get('name', '未知')} - {url}")
                    else:
                        new_list.append(site)
                item['list'] = new_list
            new_data.append(item)
        return new_data, removed_count
    
    return data, removed_count

def main():
    print("=" * 60)
    print("删除无效站点并重新生成HTML")
    print("=" * 60)
    
    # 文件路径
    json_file = '完整版导航.json'
    html_report = 'connection_failed_sites.html'
    backup_file = f"完整版导航.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # 备份原始文件
    print(f"\n备份原始文件到: {backup_file}")
    shutil.copy2(json_file, backup_file)
    
    # 从HTML报告中提取无效URL
    print(f"\n从 {html_report} 中提取无效URL...")
    invalid_urls = extract_invalid_sites_from_html(html_report)
    print(f"找到 {len(invalid_urls)} 个无效URL")
    print("前5个URL:")
    for url in list(invalid_urls)[:5]:
        print(f"  - {url}")
    
    # 加载JSON数据
    print(f"\n加载 {json_file}...")
    data = load_json_file(json_file)
    
    # 删除无效站点
    print(f"\n删除无效站点...")
    new_data, removed_count = remove_sites_from_data(data, invalid_urls)
    
    # 保存新数据
    print(f"\n保存清理后的数据...")
    save_json_file(new_data, json_file)
    
    print("\n" + "=" * 60)
    print(f"删除完成！共删除 {removed_count} 个站点")
    print("=" * 60)
    
    # 重新生成HTML
    print("\n重新生成HTML...")
    os.system('python tools/final_fix.py')

if __name__ == '__main__':
    main()
