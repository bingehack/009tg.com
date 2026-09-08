#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adult隔离区页面生成脚本

用途：
    复制指定分类页到adult目录，并去掉Google AdSense广告代码，
    使隔离区页面符合谷歌广告政策（敏感内容不展示广告）。

功能概述：
    1. 从cn/category/和en/category/复制指定id的分类页
    2. 去掉AdSense广告script标签
    3. 输出到cn/adult/和en/adult/目录

使用方法：
    python generate_adult_pages.py

隔离分类ID：
    1, 9, 77（可在ADULT_CATEGORY_IDS中修改）
"""

import os
import re
import shutil

# 隔离区分类ID
ADULT_CATEGORY_IDS = [1, 9, 77]

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def remove_adsense(html_content):
    """去掉AdSense广告代码"""
    # 去掉AdSense script标签
    html_content = re.sub(
        r'<script\s+async\s+src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^"]*"\s*crossorigin="anonymous"></script>\s*',
        '',
        html_content
    )
    # 去掉可能的adsbygoogle初始化代码
    html_content = re.sub(
        r'\(adsbygoogle\s*=\s*window\.adsbygoogle\s*\|\|\s*\[\]\)\.push\(\{\}\);\s*',
        '',
        html_content
    )
    return html_content


def generate_adult_pages():
    """生成adult隔离区页面"""
    print("=" * 60)
    print("生成Adult隔离区页面（无广告版本）")
    print("=" * 60)
    print()

    total_generated = 0

    for lang in ['cn', 'en']:
        src_dir = os.path.join(PROJECT_ROOT, lang, 'category')
        dst_dir = os.path.join(PROJECT_ROOT, lang, 'adult')

        # 创建目标目录
        os.makedirs(dst_dir, exist_ok=True)

        print(f"[{lang}] 源目录: {src_dir}")
        print(f"[{lang}] 目标目录: {dst_dir}")

        for cat_id in ADULT_CATEGORY_IDS:
            src_file = os.path.join(src_dir, f'{cat_id}.html')
            dst_file = os.path.join(dst_dir, f'{cat_id}.html')

            if not os.path.exists(src_file):
                print(f"  [跳过] id={cat_id} 源文件不存在: {src_file}")
                continue

            # 读取源文件
            with open(src_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 去掉AdSense广告
            content = remove_adsense(content)

            # 写入目标文件
            with open(dst_file, 'w', encoding='utf-8') as f:
                f.write(content)

            file_size = os.path.getsize(dst_file)
            print(f"  [OK] id={cat_id} -> {lang}/adult/{cat_id}.html ({file_size} bytes)")
            total_generated += 1

    print()
    print("=" * 60)
    print(f"生成完成！共生成 {total_generated} 个隔离区页面")
    print(f"  中文: cn/adult/ ({len(ADULT_CATEGORY_IDS)} 个)")
    print(f"  英文: en/adult/ ({len(ADULT_CATEGORY_IDS)} 个)")
    print("=" * 60)
    print()
    print("说明：")
    print("  - 隔离区页面已去掉Google AdSense广告代码")
    print("  - 主分类页保持不变（仍有广告）")
    print("  - 隔离区分类ID: " + ', '.join(map(str, ADULT_CATEGORY_IDS)))


if __name__ == '__main__':
    generate_adult_pages()
