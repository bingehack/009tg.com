#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
009tg导航站 - Web管理后台
功能：抓取、分类映射、重复检测、合并生成、数据管理
"""

import os
import sys
import json
import subprocess
import traceback
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# 项目根目录（tools/web_admin/ 的上两级）
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'tools'))

app = Flask(__name__)
app.secret_key = '009tg-admin-secret-key-2026'
app.config['JSON_AS_ASCII'] = False

# ============== 工具函数 ==============

def load_data():
    """加载完整版导航.json"""
    data_path = os.path.join(PROJECT_ROOT, '完整版导航.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """保存完整版导航.json"""
    data_path = os.path.join(PROJECT_ROOT, '完整版导航.json')
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_stats():
    """获取统计数据"""
    data = load_data()
    groups = data.get('groups', [])
    root_categories = [g for g in groups if g.get('parent_id') is None]
    sub_categories = [g for g in groups if g.get('parent_id') is not None]
    total_sites = sum(len(g.get('sites', [])) for g in groups)

    # 分类站点数排行
    category_stats = []
    for g in groups:
        sites_count = len(g.get('sites', []))
        if sites_count > 0:
            category_stats.append({
                'id': g.get('id'),
                'name': g.get('name'),
                'sites_count': sites_count
            })
    category_stats.sort(key=lambda x: x['sites_count'], reverse=True)

    return {
        'total_sites': total_sites,
        'total_categories': len(groups),
        'root_categories': len(root_categories),
        'sub_categories': len(sub_categories),
        'top_categories': category_stats[:10],
        'export_date': data.get('exportDate', '未知')
    }

def get_all_categories():
    """获取所有分类（用于映射下拉框）"""
    data = load_data()
    groups = data.get('groups', [])
    result = []
    for g in groups:
        parent_name = ''
        if g.get('parent_id'):
            parent = next((p for p in groups if p['id'] == g['parent_id']), None)
            if parent:
                parent_name = parent.get('name', '')
        result.append({
            'id': g.get('id'),
            'name': g.get('name'),
            'parent_id': g.get('parent_id'),
            'parent_name': parent_name,
            'sites_count': len(g.get('sites', []))
        })
    return result

def get_existing_domains():
    """获取已有站点域名集合（用于重复检测）"""
    data = load_data()
    domains = set()
    for g in data.get('groups', []):
        for s in g.get('sites', []):
            url = s.get('url', '')
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).hostname.lower()
                if domain:
                    domains.add(domain)
            except:
                pass
    return domains

def run_command(cmd, cwd=None):
    """运行命令并捕获输出"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300
        )
        return {
            'success': result.returncode == 0,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': '命令执行超时（>300秒）'}
    except Exception as e:
        return {'success': False, 'error': str(e), 'traceback': traceback.format_exc()}

# ============== 页面路由 ==============

@app.route('/')
def dashboard():
    """仪表盘"""
    stats = get_stats()
    return render_template('dashboard.html', stats=stats, active='dashboard')

@app.route('/crawl')
def crawl_page():
    """抓取页面"""
    # 可用的抓取脚本
    crawler_dir = os.path.join(PROJECT_ROOT, 'tools', 'crawler')
    crawlers = []
    if os.path.exists(crawler_dir):
        for f in os.listdir(crawler_dir):
            if f.startswith('crawl_') and f.endswith('.py'):
                crawlers.append(f)
    return render_template('crawl.html', crawlers=crawlers, active='crawl')

@app.route('/merge')
def merge_page():
    """合并执行页面"""
    crawl_result = session.get('crawl_result', None)
    if not crawl_result:
        return redirect(url_for('crawl_page'))
    categories = get_all_categories()
    existing_domains = get_existing_domains()

    # 重复检测
    raw_sites = crawl_result.get('sites', [])
    duplicates = []
    new_sites = []
    for site in raw_sites:
        url = site.get('url', '')
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).hostname.lower()
        except:
            domain = ''
        if domain and domain in existing_domains:
            site['_is_duplicate'] = True
            site['_domain'] = domain
            duplicates.append(site)
        else:
            site['_is_duplicate'] = False
            site['_domain'] = domain
            new_sites.append(site)

    crawl_result['sites'] = raw_sites
    crawl_result['duplicates'] = duplicates
    crawl_result['new_sites'] = new_sites
    session['crawl_result'] = crawl_result

    return render_template('merge.html',
                           crawl_result=crawl_result,
                           categories=categories,
                           active='merge')

@app.route('/manage')
def manage_page():
    """数据管理页面"""
    categories = get_all_categories()
    return render_template('manage.html', categories=categories, active='manage')

# ============== API路由 ==============

@app.route('/api/stats')
def api_stats():
    """获取统计数据"""
    return jsonify(get_stats())

@app.route('/api/search')
def api_search():
    """搜索站点"""
    keyword = request.args.get('q', '').strip().lower()
    category_id = request.args.get('category_id', '').strip()
    if not keyword and not category_id:
        return jsonify({'sites': [], 'total': 0})

    data = load_data()
    results = []
    for g in data.get('groups', []):
        if category_id and str(g.get('id')) != category_id:
            continue
        for s in g.get('sites', []):
            if keyword:
                name = s.get('name', '').lower()
                url = s.get('url', '').lower()
                desc = s.get('description', '').lower()
                if keyword not in name and keyword not in url and keyword not in desc:
                    continue
            results.append({
                'id': s.get('id'),
                'name': s.get('name'),
                'url': s.get('url'),
                'description': s.get('description', ''),
                'category_id': g.get('id'),
                'category_name': g.get('name')
            })
    return jsonify({'sites': results[:200], 'total': len(results)})

@app.route('/api/delete_site', methods=['POST'])
def api_delete_site():
    """删除站点"""
    data = request.get_json()
    site_id = data.get('site_id')
    if not site_id:
        return jsonify({'success': False, 'error': '缺少site_id'})

    nav_data = load_data()
    removed = False
    removed_info = None
    for g in nav_data.get('groups', []):
        sites = g.get('sites', [])
        new_sites = []
        for s in sites:
            if s.get('id') == site_id:
                removed = True
                removed_info = {'name': s.get('name'), 'url': s.get('url'), 'category': g.get('name')}
            else:
                new_sites.append(s)
        g['sites'] = new_sites

    if removed:
        save_data(nav_data)
        return jsonify({'success': True, 'removed': removed_info})
    else:
        return jsonify({'success': False, 'error': '未找到该站点'})

@app.route('/api/crawl', methods=['POST'])
def api_crawl():
    """执行抓取"""
    data = request.get_json()
    url = data.get('url', '').strip()
    crawler_type = data.get('crawler_type', 'generic')
    custom_script = data.get('custom_script', '')

    if not url and crawler_type == 'generic':
        return jsonify({'success': False, 'error': '请输入目标站点URL'})

    try:
        if crawler_type == 'generic':
            # 通用抓取
            result = run_command([
                sys.executable,
                os.path.join(PROJECT_ROOT, 'tools', 'web_admin', 'crawler_generic.py'),
                url
            ])
        else:
            # 指定脚本抓取
            script_path = os.path.join(PROJECT_ROOT, 'tools', 'crawler', custom_script)
            if not os.path.exists(script_path):
                return jsonify({'success': False, 'error': f'脚本不存在: {custom_script}'})
            result = run_command([sys.executable, script_path])

        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': result.get('error', '抓取失败'),
                'stderr': result.get('stderr', ''),
                'stdout': result.get('stdout', '')
            })

        # 解析抓取结果（脚本输出JSON到stdout最后一行）
        stdout = result.get('stdout', '')
        result_data = None
        for line in stdout.strip().split('\n'):
            line = line.strip()
            if line.startswith('{') and 'CRAWL_RESULT' in line:
                try:
                    result_data = json.loads(line.replace('CRAWL_RESULT:', ''))
                    break
                except:
                    pass

        if not result_data:
            # 尝试从raw目录读取最新文件
            raw_dir = os.path.join(PROJECT_ROOT, 'raw')
            if os.path.exists(raw_dir):
                files = [f for f in os.listdir(raw_dir) if f.endswith('.json')]
                if files:
                    latest = max(files, key=lambda f: os.path.getmtime(os.path.join(raw_dir, f)))
                    with open(os.path.join(raw_dir, latest), 'r', encoding='utf-8') as f:
                        result_data = json.load(f)
                    result_data['source_file'] = latest

        if not result_data:
            return jsonify({
                'success': False,
                'error': '无法解析抓取结果',
                'stdout': stdout[-2000:]
            })

        # 存储到session
        session['crawl_result'] = result_data
        return jsonify({
            'success': True,
            'data': result_data,
            'categories_count': len(result_data.get('categories', [])),
            'sites_count': len(result_data.get('sites', []))
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })

@app.route('/api/merge', methods=['POST'])
def api_merge():
    """执行合并+生成"""
    data = request.get_json()
    mappings = data.get('mappings', {})  # {源分类名: 目标分类id}
    skip_duplicates = data.get('skip_duplicates', True)
    skip_categories = data.get('skip_categories', [])  # 跳过的分类

    crawl_result = session.get('crawl_result', None)
    if not crawl_result:
        return jsonify({'success': False, 'error': '没有抓取结果，请先抓取'})

    logs = []
    try:
        # 1. 合并数据到完整版导航.json
        logs.append('【1/5】开始合并数据...')
        nav_data = load_data()
        existing_domains = get_existing_domains()
        existing_ids = set()
        for g in nav_data.get('groups', []):
            for s in g.get('sites', []):
                existing_ids.add(s.get('id', 0))

        new_id = max(existing_ids) + 1 if existing_ids else 1
        added_count = 0
        duplicate_count = 0
        skipped_count = 0
        category_added = {}

        sites = crawl_result.get('sites', [])
        for site in sites:
            source_category = site.get('category', '')
            if source_category in skip_categories:
                skipped_count += 1
                continue

            target_category_id = mappings.get(source_category)
            if not target_category_id:
                skipped_count += 1
                continue

            # 重复检测
            url = site.get('url', '')
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).hostname.lower()
            except:
                domain = ''
            if skip_duplicates and domain and domain in existing_domains:
                duplicate_count += 1
                continue

            # 找到目标分类
            target_group = next((g for g in nav_data['groups'] if g['id'] == int(target_category_id)), None)
            if not target_group:
                skipped_count += 1
                continue

            # 添加站点
            new_site = {
                'id': new_id,
                'group_id': int(target_category_id),
                'name': site.get('name', ''),
                'url': site.get('url', ''),
                'icon': '',
                'description': site.get('description', ''),
                'description_en': site.get('description_en', ''),
                'notes': f'来源：{crawl_result.get("source_name", "抓取")}',
                'order_num': new_id,
                'is_public': 1,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            target_group['sites'].append(new_site)
            existing_domains.add(domain)
            category_added[target_group['name']] = category_added.get(target_group['name'], 0) + 1
            new_id += 1
            added_count += 1

        nav_data['exportDate'] = datetime.now().strftime('%Y-%m-%d')
        save_data(nav_data)
        logs.append(f'  合并完成：新增{added_count}个，重复{duplicate_count}个，跳过{skipped_count}个')
        for cat, cnt in category_added.items():
            logs.append(f'    - {cat}: +{cnt}')

        # 2. 下载favicon
        logs.append('【2/5】开始下载favicon...')
        result = run_command([sys.executable, os.path.join(PROJECT_ROOT, 'tools', 'cache_favicons.py')])
        logs.append(f'  favicon下载: {"成功" if result.get("success") else "失败"}')
        if not result.get('success'):
            logs.append(f'  错误: {result.get("error", result.get("stderr", ""))[:200]}')

        # 3. 生成首页
        logs.append('【3/5】生成中英文首页...')
        result = run_command([sys.executable, os.path.join(PROJECT_ROOT, 'tools', 'generate_new_html.py')])
        logs.append(f'  首页生成: {"成功" if result.get("success") else "失败"}')
        if not result.get('success'):
            logs.append(f'  错误: {result.get("error", result.get("stderr", ""))[:200]}')

        # 4. 生成分类详情页
        logs.append('【4/5】生成分类详情页...')
        result = run_command([sys.executable, os.path.join(PROJECT_ROOT, 'tools', 'generate_category_pages.py')])
        logs.append(f'  分类详情页: {"成功" if result.get("success") else "失败"}')
        if not result.get('success'):
            logs.append(f'  错误: {result.get("error", result.get("stderr", ""))[:200]}')

        # 5. 更新sitemap
        logs.append('【5/5】更新sitemap...')
        result = run_command([sys.executable, os.path.join(PROJECT_ROOT, 'tools', 'update_sitemap.py')])
        logs.append(f'  sitemap: {"成功" if result.get("success") else "失败"}')

        logs.append('')
        logs.append('=== 全部完成 ===')
        logs.append(f'新增站点: {added_count}')
        logs.append(f'重复跳过: {duplicate_count}')
        logs.append(f'未映射跳过: {skipped_count}')
        logs.append('')
        logs.append('【下一步操作】')
        logs.append('1. 本地预览: python -m http.server 8000')
        logs.append('2. 提交部署: git add . && git commit -m "抓取新增站点" && git push origin master')
        logs.append('3. Cloudflare会在1-2分钟内自动部署')

        # 清除session中的抓取结果
        session.pop('crawl_result', None)

        return jsonify({
            'success': True,
            'logs': logs,
            'added': added_count,
            'duplicates': duplicate_count,
            'skipped': skipped_count
        })

    except Exception as e:
        logs.append(f'执行异常: {str(e)}')
        logs.append(traceback.format_exc())
        return jsonify({'success': False, 'logs': logs, 'error': str(e)})

# ============== 启动 ==============

if __name__ == '__main__':
    print('=' * 50)
    print('009tg导航站 - Web管理后台')
    print('=' * 50)
    print(f'项目根目录: {PROJECT_ROOT}')
    print(f'访问地址: http://127.0.0.1:5000')
    print('=' * 50)
    # 自动打开浏览器
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    app.run(host='127.0.0.1', port=5000, debug=False)
