#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复3个bug的脚本

Bug 1: 关于本站链接在英文版本应指向en/about.html
Bug 2: 英文版本的favicon路径应使用相对路径../assets/favicons/
Bug 3: 英文版本的语言切换器链接应正确跳转
"""

import os
import re

# 获取脚本所在目录的父目录的父目录（项目根目录）
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))

# 切换到项目根目录
os.chdir(project_root)

def fix_about_link(html_content, is_english=False):
    """修复关于本站链接"""
    if is_english:
        # 英文版本：about.html 指向 en/about.html
        html_content = html_content.replace(
            '<a href="about.html">',
            '<a href="about.html">'
        )
    return html_content

def fix_favicon_paths(html_content, is_english=False):
    """修复favicon路径"""
    if is_english:
        # 英文版本：assets/favicons/ -> ../assets/favicons/
        html_content = html_content.replace(
            'data-src="assets/favicons/',
            'data-src="../assets/favicons/'
        )
        # 修复JavaScript中的favicon路径
        html_content = html_content.replace(
            '"icon": "assets/favicons/',
            '"icon": "../assets/favicons/'
        )
    return html_content

def fix_language_switcher(html_content, is_english=False):
    """修复语言切换器"""
    if is_english:
        # 英文版本的语言切换器
        old_switcher = '''<li class="dropdown hover-line language-switcher">
                        <a href="index.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                        </a>
                        <ul class="dropdown-menu languages">
                            <li>
                                <a href="en/index.html">
                                    <img src="assets/images/flags/flag-us.png" alt="flag-us" /> English
                                </a>
                            </li>
                            <li class="active">
                                <a href="index.html">
                                    <img src="assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                                </a>
                            </li>
                        </ul>
                    </li>'''
        
        new_switcher = '''<li class="dropdown hover-line language-switcher">
                        <a href="index.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="../assets/images/flags/flag-us.png" alt="flag-us" /> English
                        </a>
                        <ul class="dropdown-menu languages">
                            <li class="active">
                                <a href="index.html">
                                    <img src="../assets/images/flags/flag-us.png" alt="flag-us" /> English
                                </a>
                            </li>
                            <li>
                                <a href="../index.html">
                                    <img src="../assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                                </a>
                            </li>
                        </ul>
                    </li>'''
        
        html_content = html_content.replace(old_switcher, new_switcher)
        
        # 修复其他assets路径
        html_content = html_content.replace(
            'src="assets/images/',
            'src="../assets/images/'
        )
        html_content = html_content.replace(
            'href="assets/',
            'href="../assets/'
        )
    
    return html_content

def fix_html_file(file_path, is_english=False):
    """修复HTML文件"""
    print(f"修复文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 修复bug
    html_content = fix_about_link(html_content, is_english)
    html_content = fix_favicon_paths(html_content, is_english)
    html_content = fix_language_switcher(html_content, is_english)
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ 修复完成: {file_path}")

def main():
    print("=" * 60)
    print("修复3个bug")
    print("=" * 60)
    
    # 修复根目录的index.html
    fix_html_file('index.html', is_english=False)
    
    # 修复cn/index.html
    fix_html_file('cn/index.html', is_english=False)
    
    # 修复en/index.html
    fix_html_file('en/index.html', is_english=True)
    
    print("\n" + "=" * 60)
    print("所有bug修复完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
