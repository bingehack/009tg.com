#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查PNG文件头脚本

用途：
    检查指定PNG文件的文件头是否正确。

功能概述：
    读取PNG文件的文件头，验证是否符合PNG格式标准

使用方法：
    python check_png.py

主要特性：
    - 验证PNG文件头格式
    - 显示文件头的十六进制值
"""

with open('assets/favicons/7dadb4e62aa7584241decf0aa741471a.png', 'rb') as f:
    header = f.read(8)
    print(f'PNG header: {header}')
    print(f'PNG header bytes: {[hex(b) for b in header]}')
    expected = b'\x89PNG\r\n\x1a\n'
    print(f'Expected header: {expected}')
    print(f'Expected header bytes: {[hex(b) for b in expected]}')
    print(f'Is valid PNG: {header == expected}')
