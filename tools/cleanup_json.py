#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理完整版导航.json中的冗余数据

删除：
- 顶层 sites[]（1219条扁平站点，与groups中站点重复，生成脚本不使用）
- configs{}（原平台导出配置，生成脚本不使用）

保留：
- groups[]（94个分类，含内嵌站点，生成脚本唯一数据源）
- version
- exportDate
"""

import json
import os

JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '完整版导航.json')

print(f'读取: {JSON_PATH}')
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'\n清理前:')
print(f'  顶层字段: {list(data.keys())}')
print(f'  groups 数量: {len(data.get("groups", []))}')
print(f'  groups 中站点总数: {sum(len(g.get("sites", [])) for g in data.get("groups", []))}')
print(f'  顶层 sites 数量: {len(data.get("sites", []))}')
print(f'  configs: {data.get("configs", {})}')

# 删除冗余字段
if 'sites' in data:
    del data['sites']
    print(f'\n已删除顶层 sites[]')

if 'configs' in data:
    del data['configs']
    print(f'已删除 configs{{}}')

print(f'\n清理后:')
print(f'  顶层字段: {list(data.keys())}')
print(f'  groups 数量: {len(data.get("groups", []))}')
print(f'  groups 中站点总数: {sum(len(g.get("sites", [])) for g in data.get("groups", []))}')

# 写回，保持与原文件相同的格式（不缩进，紧凑格式，与原文件一致）
# 先检查原文件格式
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    raw = f.read()
# 判断原文件是否有缩进
has_indent = '\n  ' in raw[:500]
print(f'\n原文件格式: {"缩进" if has_indent else "紧凑"}')

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    if has_indent:
        json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        json.dump(data, f, ensure_ascii=False)

new_size = os.path.getsize(JSON_PATH)
print(f'\n写入完成: {JSON_PATH}')
print(f'新文件大小: {new_size} 字节 ({new_size/1024:.1f} KB)')
print(f'减少: {1192412 - new_size} 字节 ({(1192412 - new_size)/1024:.1f} KB)')

# 验证可正常解析
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    verify = json.load(f)
assert 'groups' in verify, 'groups 字段缺失!'
assert len(verify['groups']) == 94, f'分类数量异常: {len(verify["groups"])}'
assert 'sites' not in verify, 'sites 未删除!'
assert 'configs' not in verify, 'configs 未删除!'
print('\n验证通过: groups=94, 无冗余字段, JSON可正常解析')
