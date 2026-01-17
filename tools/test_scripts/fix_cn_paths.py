#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复中文版资源路径脚本

用途：
    修复cn/index.html文件中的资源路径，将assets/替换为../assets/

使用方法：
    python fix_cn_paths.py
"""

import os

def fix_cn_paths():
    """修复中文版资源路径"""
    
    # 读取cn/index.html文件
    print("读取cn/index.html文件...")
    cn_path = 'cn/index.html'
    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_html = f.read()
    
    # 替换资源路径
    print("修复资源路径...")
    cn_html = cn_html.replace('src="assets/', 'src="../assets/')
    cn_html = cn_html.replace('href="assets/', 'href="../assets/')
    
    # 修复JavaScript数据中的图标路径
    cn_html = cn_html.replace('"icon": "assets/', '"icon": "../assets/')
    
    # 修复语言切换菜单的链接
    cn_html = cn_html.replace('href="index.html"', 'href="../index.html"')
    cn_html = cn_html.replace('href="../cn/index.html"', 'href="../index.html"')
    
    # 修复redirect.html链接
    cn_html = cn_html.replace("window.open('redirect.html", "window.open('../redirect.html")
    
    # 保存文件
    print("保存文件...")
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_html)
    
    print("修复完成！")

if __name__ == '__main__':
    fix_cn_paths()
