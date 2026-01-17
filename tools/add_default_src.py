import os
import re

# 获取脚本所在目录的父目录（项目根目录）
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# 切换到项目根目录
os.chdir(project_root)

html_files = ['index.html', 'cn/index.html', 'en/index.html']

for file_name in html_files:
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 为所有使用Google favicon服务的图片添加默认的src属性
    # 这样在懒加载之前就会有一个fallback图片
    pattern = r'<img data-src="(https://www\.google\.com/s2/favicons\?domain=[^"]+)" class="lozad img-circle" width="40">'
    replacement = r'<img src="assets/images/logos/default.png" data-src="\1" class="lozad img-circle" width="40">'
    
    count = len(re.findall(pattern, content))
    content = re.sub(pattern, replacement, content)
    
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已更新 {file_name}，添加了 {count} 个默认src属性')
