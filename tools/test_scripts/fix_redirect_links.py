#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复redirect.html链接脚本

用途：
    修复cn/index.html和en/index.html中的redirect.html链接，将redirect.html替换为../redirect.html

使用方法：
    python fix_redirect_links.py
"""

import os

def fix_redirect_links():
    """修复redirect.html链接"""
    
    # 修复cn/index.html
    print("修复cn/index.html...")
    cn_path = 'cn/index.html'
    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_html = f.read()
    
    # 替换redirect.html为../redirect.html
    cn_html = cn_html.replace("window.open('redirect.html", "window.open('../redirect.html")
    
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_html)
    
    print("cn/index.html修复完成！")
    
    # 修复en/index.html
    print("修复en/index.html...")
    en_path = 'en/index.html'
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    # 替换redirect.html为../redirect.html
    en_html = en_html.replace("window.open('redirect.html", "window.open('../redirect.html")
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_html)
    
    print("en/index.html修复完成！")
    print("所有文件修复完成！")

if __name__ == '__main__':
    fix_redirect_links()
