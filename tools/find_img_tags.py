with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 查找所有img标签
img_tags = re.findall(r'<img[^>]+>', content)

# 查找包含"账号星球"的img标签
for tag in img_tags:
    if '7dadb4e62aa7584241decf0aa741471a.png' in tag:
        print('Found img tag for 账号星球:')
        print(tag)
        print()
