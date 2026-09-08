#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复tools页面的3个问题：
1. 左上角logo：svg齿轮图标 -> 主站logo图片
2. 去掉"纯前端""在线API"标签
3. footer链接：/about.html -> /cn/about.html 等
"""

import os
import re
import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(PROJECT_ROOT, 'tools')

def fix_tools_page(filepath):
    """修复单个tools页面"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 问题1：替换svg齿轮图标为主站logo图片
    # 匹配 <svg viewBox="0 0 24 24">...</svg> 在brand里面
    content = re.sub(
        r'<svg viewBox="0 0 24 24"><path d="[^"]*"/></svg>',
        '<img src="../assets/images/logo@2x.png" alt="009TG" style="height:28px;width:auto;border-radius:4px;">',
        content
    )
    
    # 问题2：去掉"纯前端""在线API"标签
    content = re.sub(
        r'\s*<span class="badge badge-api"[^>]*>[^<]*</span>',
        '',
        content
    )
    content = re.sub(
        r'\s*<span class="badge badge-offline"[^>]*>[^<]*</span>',
        '',
        content
    )
    
    # 问题3：footer链接改成/cn/目录
    content = content.replace('href="/about.html"', 'href="/cn/about.html"')
    content = content.replace('href="/privacy.html"', 'href="/cn/privacy.html"')
    content = content.replace('href="/contact.html"', 'href="/cn/contact.html"')
    content = content.replace('href="/disclaimer.html"', 'href="/cn/disclaimer.html"')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("批量修复tools页面")
    print("=" * 60)
    print()
    
    html_files = glob.glob(os.path.join(TOOLS_DIR, '*.html'))
    print(f"找到 {len(html_files)} 个HTML文件")
    print()
    
    fixed_count = 0
    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        if fix_tools_page(filepath):
            print(f"  [修复] {filename}")
            fixed_count += 1
        else:
            print(f"  [跳过] {filename} (无需修改)")
    
    print()
    print("=" * 60)
    print(f"完成！共修复 {fixed_count} 个文件")
    print("=" * 60)
    print()
    print("修复内容：")
    print("  1. 左上角logo：svg齿轮 -> 主站logo图片")
    print("  2. 去掉'纯前端''在线API'标签")
    print("  3. footer链接：/about.html -> /cn/about.html 等")


if __name__ == '__main__':
    main()
