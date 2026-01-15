html_files = ['index.html', 'cn/index.html', 'en/index.html']

for file_name in html_files:
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复JavaScript中的动态生成的img标签，移除错误的反斜杠
    # 直接使用字符串替换
    old_str = '<img src="\\${site.icon}" class="img-circle" width="40">'
    new_str = '<img src="${site.icon}" class="img-circle" width="40">'
    
    count = content.count(old_str)
    content = content.replace(old_str, new_str)
    
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已更新 {file_name}，修复了 {count} 处')
