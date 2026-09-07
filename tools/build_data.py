#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_data.py - 从 raw/ 目录合并数据到完整版导航.json

用途：
    扫描 raw/ 目录下所有 JSON 文件（_template.json 除外），按分类匹配/创建，
    按 URL 域名去重后追加站点，生成完整版导航.json。

功能概述：
    1. 读取完整版导航.json 作为基础
    2. 扫描 raw/ 目录下所有 .json 文件
    3. 按 category + parent_category 匹配现有分类，不存在则自动创建
    4. 按 URL 域名去重，新站点自动分配 id、group_id、order_num、时间戳
    5. 备份原文件后输出完整版导航.json

使用方法：
    python build_data.py

主要特性：
    - 自动备份原 JSON 文件
    - 按域名去重，避免重复添加
    - 自动创建缺失的分类（含父分类）
    - 详细的合并统计输出
    - 不影响 generate_new_html.py（输出格式完全兼容）
"""

import json
import os
import shutil
import yaml
from datetime import datetime
from urllib.parse import urlparse

# 路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(PROJECT_ROOT, '完整版导航.json')
RAW_DIR = os.path.join(PROJECT_ROOT, 'raw')
BACKUP_PATH = os.path.join(PROJECT_ROOT, '完整版导航.json.build_backup')
MAPPING_PATH = os.path.join(SCRIPT_DIR, 'category_mapping.yaml')


def get_domain(url):
    """从URL提取域名（小写）"""
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ''


def load_base_data():
    """读取基础 JSON 数据"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def scan_raw_files():
    """扫描 raw/ 目录下所有 JSON 文件（排除 _template.json 和 README.md）"""
    raw_files = []
    if not os.path.exists(RAW_DIR):
        print(f'raw/ 目录不存在: {RAW_DIR}')
        return raw_files

    for filename in sorted(os.listdir(RAW_DIR)):
        if not filename.endswith('.json'):
            continue
        if filename.startswith('_'):
            continue
        filepath = os.path.join(RAW_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            raw_files.append((filename, data))
            print(f'  读取: {filename} ({len(data.get("sites", []))} 个站点)')
        except Exception as e:
            print(f'  跳过: {filename} - 解析失败: {e}')
    return raw_files


def load_category_mapping():
    """加载分类映射表 category_mapping.yaml"""
    if not os.path.exists(MAPPING_PATH):
        print(f'  警告: 映射表不存在: {MAPPING_PATH}，将使用原始分类名')
        return {}
    try:
        with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
            mapping = yaml.safe_load(f)
        print(f'  已加载分类映射表: {os.path.basename(MAPPING_PATH)}')
        return mapping or {}
    except Exception as e:
        print(f'  警告: 映射表加载失败: {e}，将使用原始分类名')
        return {}


def map_category(mapping, source_name, source_category):
    """
    根据映射表将源分类名转换为目标分类名

    Args:
        mapping: 映射表字典
        source_name: 源站名（如"AI地带"）
        source_category: 源分类名（如"AI图像工具"）

    Returns:
        (target_category, parent_category): 目标分类名和父分类名
    """
    default_config = mapping.get('_default', {})
    fallback_category = default_config.get('fallback_category', 'AI常用工具')
    default_parent = default_config.get('parent_category', 'AI工具')

    # 查找源站映射
    source_mapping = mapping.get(source_name, {})
    if source_mapping and source_category in source_mapping:
        target = source_mapping[source_category]
        return target, default_parent

    # 未找到映射，使用兜底分类
    if source_mapping:
        print(f'    未映射分类 [{source_category}]，使用兜底分类 [{fallback_category}]')
    return fallback_category, default_parent


def find_category(groups, category_name, parent_category_name=None):
    """按名称查找分类，返回 group 对象或 None
    查找策略：
    1. 如果指定了 parent_category_name，先按"父分类+分类名"精确匹配
    2. 精确匹配失败时，降级为全局按分类名查找（避免同名分类重复创建）
    """
    # 策略1：精确匹配（父分类+分类名）
    if parent_category_name:
        for g in groups:
            if g['name'] == category_name:
                parent = find_category_by_id(groups, g.get('parent_id'))
                if parent and parent['name'] == parent_category_name:
                    return g

    # 策略2：全局按分类名查找（降级匹配）
    for g in groups:
        if g['name'] == category_name:
            if parent_category_name is None:
                # 未指定父分类时，只匹配一级分类
                if g.get('parent_id') is None:
                    return g
            else:
                # 指定了父分类但精确匹配失败，返回第一个同名分类（全局降级）
                return g

    return None


def find_category_by_id(groups, category_id):
    """按 ID 查找分类"""
    if category_id is None:
        return None
    for g in groups:
        if g['id'] == category_id:
            return g
    return None


def get_next_group_id(groups):
    """获取下一个可用的分类 ID"""
    max_id = 0
    for g in groups:
        if g['id'] > max_id:
            max_id = g['id']
    return max_id + 1


def get_next_site_id(groups):
    """获取下一个可用的站点 ID"""
    max_id = 0
    for g in groups:
        for s in g.get('sites', []):
            if s.get('id', 0) > max_id:
                max_id = s['id']
    return max_id + 1


def get_next_order_num(groups, parent_id=None):
    """获取同级分类下一个 order_num"""
    max_order = -1
    for g in groups:
        if g.get('parent_id') == parent_id:
            if g.get('order_num', 0) > max_order:
                max_order = g['order_num']
    return max_order + 1


def get_next_site_order_num(group):
    """获取分类内下一个站点 order_num"""
    max_order = -1
    for s in group.get('sites', []):
        if s.get('order_num', 0) > max_order:
            max_order = s['order_num']
    return max_order + 1


def build_existing_domains(groups):
    """构建现有站点的域名集合（用于去重）"""
    domains = set()
    for g in groups:
        for s in g.get('sites', []):
            domain = get_domain(s.get('url', ''))
            if domain:
                domains.add(domain)
    return domains


def create_category(groups, category_name, parent_category_name=None):
    """创建新分类（含父分类，如果父分类不存在）"""
    parent_id = None
    if parent_category_name:
        parent = find_category(groups, parent_category_name)
        if not parent:
            # 父分类不存在，先创建父分类
            parent = create_category(groups, parent_category_name, None)
        parent_id = parent['id']

    new_group = {
        'id': get_next_group_id(groups),
        'name': category_name,
        'order_num': get_next_order_num(groups, parent_id),
        'parent_id': parent_id,
        'sites': []
    }
    groups.append(new_group)
    print(f'    创建分类: {category_name} (id={new_group["id"]}, parent_id={parent_id})')
    return new_group


def merge_raw_data(base_data, raw_files, category_mapping=None):
    """合并 raw 数据到基础数据（支持分类映射表）"""
    groups = base_data['groups']
    existing_domains = build_existing_domains(groups)
    next_site_id = get_next_site_id(groups)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    stats = {
        'files_processed': 0,
        'categories_matched': 0,
        'categories_created': 0,
        'sites_total': 0,
        'sites_added': 0,
        'sites_skipped_duplicate': 0,
        'sites_skipped_invalid': 0,
    }

    for filename, raw_data in raw_files:
        stats['files_processed'] += 1
        source_name = raw_data.get('source', '')
        source_category = raw_data.get('category', '')
        sites = raw_data.get('sites', [])

        if not source_category:
            print(f'  跳过 {filename}: 缺少 category 字段')
            continue

        # 应用分类映射表
        if category_mapping:
            category_name, parent_category_name = map_category(
                category_mapping, source_name, source_category
            )
            print(f'\n处理: {filename}')
            print(f'  源分类: {source_name}/{source_category}')
            print(f'  映射目标: {category_name} (父: {parent_category_name})')
        else:
            category_name = source_category
            parent_category_name = raw_data.get('parent_category')
            print(f'\n处理: {filename}')
            print(f'  分类: {category_name}' + (f' (父: {parent_category_name})' if parent_category_name else ' (一级)'))

        print(f'  待处理站点: {len(sites)}')

        # 匹配或创建分类
        group = find_category(groups, category_name, parent_category_name)
        if group:
            stats['categories_matched'] += 1
            print(f'  匹配到现有分类: id={group["id"]}')
        else:
            stats['categories_created'] += 1
            group = create_category(groups, category_name, parent_category_name)

        # 处理站点
        next_order = get_next_site_order_num(group)
        for site in sites:
            stats['sites_total'] += 1
            name = site.get('name', '').strip()
            url = site.get('url', '').strip()
            description = site.get('description', '').strip()
            status = site.get('status', 'verified')

            if not name or not url:
                stats['sites_skipped_invalid'] += 1
                print(f'    跳过(无效): {name or "无名称"} - {url or "无URL"}')
                continue

            # 按域名去重
            domain = get_domain(url)
            if domain in existing_domains:
                stats['sites_skipped_duplicate'] += 1
                print(f'    跳过(重复): {name} - {domain}')
                continue

            # icon 处理：留空则用 faviconextractor API 占位
            icon = site.get('icon', '').strip()
            if not icon and domain:
                icon = f'https://www.faviconextractor.com/api/favicon/{domain}'

            # 创建新站点
            new_site = {
                'id': next_site_id,
                'group_id': group['id'],
                'name': name,
                'url': url,
                'icon': icon,
                'description': description,
                'notes': site.get('notes', f'来源: {filename}'),
                'order_num': next_order,
                'is_public': 1 if status == 'verified' else 0,
                'created_at': now_str,
                'updated_at': now_str,
            }

            group['sites'].append(new_site)
            existing_domains.add(domain)
            next_site_id += 1
            next_order += 1
            stats['sites_added'] += 1
            print(f'    添加: {name} - {url} (id={new_site["id"]})')

    return base_data, stats


def save_output(data):
    """备份原文件并保存输出"""
    # 备份
    if os.path.exists(JSON_PATH):
        shutil.copy2(JSON_PATH, BACKUP_PATH)
        print(f'\n已备份原文件到: {os.path.basename(BACKUP_PATH)}')

    # 保存（保持缩进格式，与清理后的 JSON 一致）
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    new_size = os.path.getsize(JSON_PATH)
    print(f'已保存: {JSON_PATH} ({new_size} 字节, {new_size/1024:.1f} KB)')


def print_stats(stats):
    """打印合并统计"""
    print('\n' + '=' * 50)
    print('合并统计')
    print('=' * 50)
    print(f'  处理文件数:     {stats["files_processed"]}')
    print(f'  匹配现有分类:   {stats["categories_matched"]}')
    print(f'  新建分类:       {stats["categories_created"]}')
    print(f'  处理站点总数:   {stats["sites_total"]}')
    print(f'  成功添加:       {stats["sites_added"]}')
    print(f'  跳过(重复):     {stats["sites_skipped_duplicate"]}')
    print(f'  跳过(无效):     {stats["sites_skipped_invalid"]}')
    print('=' * 50)


def main():
    print('=' * 50)
    print('build_data.py - 合并 raw/ 数据到完整版导航.json')
    print('=' * 50)

    # 1. 读取基础数据
    print(f'\n读取基础数据: {os.path.basename(JSON_PATH)}')
    base_data = load_base_data()
    print(f'  现有分类: {len(base_data["groups"])}')
    print(f'  现有站点: {sum(len(g.get("sites", [])) for g in base_data["groups"])}')

    # 2. 扫描 raw 文件
    print(f'\n扫描 raw/ 目录: {RAW_DIR}')
    raw_files = scan_raw_files()
    print(f'共找到 {len(raw_files)} 个数据文件')

    # 2.5 加载分类映射表
    print(f'\n加载分类映射表...')
    category_mapping = load_category_mapping()

    # 3. 合并数据
    if raw_files:
        base_data, stats = merge_raw_data(base_data, raw_files, category_mapping)
        print_stats(stats)
    else:
        print('\nraw/ 目录无数据文件，仅验证基础数据格式')
        stats = None

    # 4. 保存输出
    save_output(base_data)

    # 5. 最终验证
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        verify = json.load(f)
    total_sites = sum(len(g.get('sites', [])) for g in verify['groups'])
    print(f'\n最终验证: {len(verify["groups"])} 分类, {total_sites} 站点')
    print('完成!')


if __name__ == '__main__':
    main()
