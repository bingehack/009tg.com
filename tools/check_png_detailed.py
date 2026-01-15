with open('assets/favicons/7dadb4e62aa7584241decf0aa741471a.png', 'rb') as f:
    content = f.read()
    
print(f'文件大小: {len(content)} 字节')
print(f'文件头: {content[:16]}')
print(f'PNG头: {content[:8]}')
expected_header = b'\x89PNG\r\n\x1a\n'
print(f'期望PNG头: {expected_header}')
print(f'是否为有效PNG: {content[:8] == expected_header}')

# 检查文件是否全为0或重复内容
unique_bytes = len(set(content))
print(f'唯一字节数: {unique_bytes}')
print(f'是否全为相同字节: {unique_bytes == 1}')

# 检查文件内容是否为空或损坏
if len(content) < 8:
    print('文件太小，可能损坏')
elif content[:8] != expected_header:
    print('文件头不匹配，不是有效的PNG文件')
else:
    print('文件头正确，应该是有效的PNG文件')
