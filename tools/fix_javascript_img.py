import re

html_files = ['index.html', 'cn/index.html', 'en/index.html']

for file_name in html_files:
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改JavaScript中的动态生成的img标签，添加src属性
    pattern = r'<img data-src="\$\{site\.icon\}" class="lozad img-circle" width="40">'
    replacement = r'<img src="\${site.icon}" data-src="\${site.icon}" class="lozad img-circle" width="40">'
    
    content = re.sub(pattern, replacement, content)
    
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已更新 {file_name}')