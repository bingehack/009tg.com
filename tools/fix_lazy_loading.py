import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 为所有使用data-src的img标签添加src属性
pattern = r'<img data-src="(assets/favicons/[^"]+)" class="lozad img-circle" width="40">'
replacement = r'<img src="\1" data-src="\1" class="lozad img-circle" width="40">'

content = re.sub(pattern, replacement, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('已为所有懒加载图片添加src属性')