import os
import re

# 获取脚本所在目录的父目录的父目录（项目根目录）
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))

# 切换到项目根目录
os.chdir(project_root)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 为所有使用data-src的img标签添加src属性
pattern = r'<img data-src="(assets/favicons/[^"]+)" class="lozad img-circle" width="40">'
replacement = r'<img src="\1" data-src="\1" class="lozad img-circle" width="40">'

content = re.sub(pattern, replacement, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('已为所有懒加载图片添加src属性')