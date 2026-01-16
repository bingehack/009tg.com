#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查PNG文件有效性

用途：
    检查指定的PNG文件是否有效
"""

import sys

def check_png_validity(file_path):
    """检查PNG文件是否有效"""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            if header == b'\x89PNG\r\n\x1a\n':
                print(f"✓ {file_path} 是有效的PNG文件")
                return True
            else:
                print(f"✗ {file_path} 不是有效的PNG文件")
                print(f"  文件头: {header.hex()}")
                return False
    except Exception as e:
        print(f"✗ 检查文件时出错: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python check_png_file.py <文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    check_png_validity(file_path)
