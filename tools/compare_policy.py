import re
import io

def extract_text(html_file):
    with io.open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # 移除style和script
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '\n', content)
    # 清理空白
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

print("=" * 60)
print("伙伴 privacy.html 内容")
print("=" * 60)
text = extract_text('temp/extracted/policy/privacy.html')
# 只打印Cookie和AdSense相关部分
lines = text.split('\n')
in_section = False
count = 0
for i, line in enumerate(lines):
    if 'Cookie' in line or 'AdSense' in line or '广告' in line or 'Google' in line:
        in_section = True
    if in_section and count < 50:
        print(line[:120])
        count += 1
    if in_section and '儿童' in line and count > 10:
        break

print()
print("=" * 60)
print("伙伴 about.html 内容")
print("=" * 60)
text = extract_text('temp/extracted/policy/about.html')
print(text[:1500])

print()
print("=" * 60)
print("伙伴 contact.html 内容")
print("=" * 60)
text = extract_text('temp/extracted/policy/contact.html')
print(text[:1500])
