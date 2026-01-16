#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有favicon文件的有效性

用途：
    扫描assets/favicons目录，检查所有PNG文件的有效性
    删除无效的PNG文件
"""

import os
import hashlib

def check_png_validity(file_path):
    """检查PNG文件是否有效"""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            if header == b'\x89PNG\r\n\x1a\n':
                return True
            else:
                return False
    except Exception as e:
        print(f"  检查文件时出错: {e}")
        return False

def scan_favicons():
    """扫描并检查所有favicon文件"""
    favicons_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'favicons')
    
    if not os.path.exists(favicons_dir):
        print(f"目录不存在: {favicons_dir}")
        return
    
    print(f"扫描目录: {favicons_dir}")
    
    invalid_files = []
    valid_count = 0
    total_count = 0
    
    for filename in os.listdir(favicons_dir):
        if filename.endswith('.png'):
            file_path = os.path.join(favicons_dir, filename)
            total_count += 1
            
            if check_png_validity(file_path):
                valid_count += 1
            else:
                invalid_files.append(filename)
                print(f"✗ 无效文件: {filename}")
    
    print(f"\n扫描完成！")
    print(f"总文件数: {total_count}")
    print(f"有效文件: {valid_count}")
    print(f"无效文件: {len(invalid_files)}")
    
    if invalid_files:
        print(f"\n无效文件列表:")
        for filename in invalid_files:
            print(f"  - {filename}")
        
        # 询问是否删除无效文件
        response = input("\n是否删除所有无效文件？(y/n): ")
        if response.lower() == 'y':
            for filename in invalid_files:
                file_path = os.path.join(favicons_dir, filename)
                try:
                    os.remove(file_path)
                    print(f"✓ 已删除: {filename}")
                except Exception as e:
                    print(f"✗ 删除失败 {filename}: {e}")
            print(f"\n共删除 {len(invalid_files)} 个无效文件")
        else:
            print("未删除任何文件")
    else:
        print("\n✓ 所有favicon文件都是有效的！")

if __name__ == '__main__':
    scan_favicons()
