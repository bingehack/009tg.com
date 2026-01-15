with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
pattern = r'<img src=".*?site\.icon.*?"'
matches = re.findall(pattern, content)
print('Found', len(matches), 'matches')
for m in matches[:5]:
    print(repr(m))
