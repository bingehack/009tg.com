#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日轮询抓取脚本
从源站列表中选择2-3个站点抓取，自动分类映射+去重+合并+生成页面

用法：
  python daily_crawl_poll.py                  # 默认抓取2个站点
  python daily_crawl_poll.py --count 3        # 指定抓取3个站点
  python daily_crawl_poll.py --dry-run        # 试运行，不实际修改数据
  python daily_crawl_poll.py --force-domain example.com  # 强制抓取指定站点
"""

import sys
import os
import json
import time
import argparse
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import urlparse

# 项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'tools'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'tools', 'web_admin'))

try:
    from auto_mapper import auto_map_all_sites, auto_map_category, get_all_categories_with_info
    AUTO_MAPPER_AVAILABLE = True
except ImportError:
    AUTO_MAPPER_AVAILABLE = False
    print('警告: auto_mapper模块不可用，将使用简单映射')

try:
    from llm_classifier import classify_and_map_sites, get_api_config
    LLM_AVAILABLE = get_api_config('siliconflow') is not None or get_api_config('zhipu') is not None
except ImportError:
    LLM_AVAILABLE = False
    print('提示: llm_classifier模块未配置API Key，将使用关键词匹配分类')


def load_nav_data():
    """加载导航数据"""
    with open(os.path.join(PROJECT_ROOT, '完整版导航.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def save_nav_data(data):
    """保存导航数据"""
    with open(os.path.join(PROJECT_ROOT, '完整版导航.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_sources():
    """加载源站列表"""
    path = os.path.join(PROJECT_ROOT, 'nav_sources.json')
    if not os.path.exists(path):
        return {'sites': {}}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_sources(data):
    """保存源站列表"""
    path = os.path.join(PROJECT_ROOT, 'nav_sources.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_domain(url):
    """提取域名"""
    try:
        domain = urlparse(url).hostname.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return ''


def select_sites(sources_data, count=2, force_domain=None):
    """选择要抓取的站点"""
    sites = sources_data.get('sites', {})
    now = datetime.now()

    # 强制抓取指定站点
    if force_domain:
        if force_domain in sites:
            return [force_domain]
        else:
            print(f'错误: 源站列表中没有 {force_domain}')
            return []

    # 评分排序：优先抓取pending，其次是超过7天没抓的
    scored = []
    for domain, info in sites.items():
        status = info.get('status', 'pending')
        last_crawled = info.get('last_crawled')

        # 计算分数
        score = 0
        if status == 'pending':
            score += 100  # 未抓取过的优先
        elif status == 'failed':
            score += 30   # 失败过的降低优先级
        elif status == 'crawled':
            score += 10

        # 距离上次抓取时间越久，分数越高
        if last_crawled:
            try:
                last_time = datetime.strptime(last_crawled, '%Y-%m-%d %H:%M:%S')
                days_ago = (now - last_time).days
                score += min(days_ago, 30)  # 最多加30分
            except:
                pass
        else:
            score += 20  # 没抓过的加分

        scored.append((domain, score))

    # 按分数降序，取前count个
    scored.sort(key=lambda x: x[1], reverse=True)
    selected = [domain for domain, _ in scored[:count]]

    return selected


# 专用抓取脚本映射（域名 -> 脚本路径）
SPECIAL_CRAWLERS = {
    'zvcard.com': 'tools/crawler/crawl_zvcard.py',
    'tboxn.com': 'tools/crawler/crawl_tbox.py',
    'tudingai.com': 'tools/crawler/crawl_tudingai.py',
    'aidh.cn': 'tools/crawler/crawl_aih.py',
    'ainav.cn': 'tools/crawler/crawl_aididai.py',
}


def crawl_site(url, domain=''):
    """用通用或专用抓取脚本抓取单个站点"""
    print(f'\n  抓取: {url}')

    # 检查是否有专用脚本
    crawler_path = None
    for special_domain, script_path in SPECIAL_CRAWLERS.items():
        if special_domain in domain or special_domain in url:
            full_path = os.path.join(PROJECT_ROOT, script_path)
            if os.path.exists(full_path):
                crawler_path = full_path
                print(f'  使用专用脚本: {script_path}')
                break

    if not crawler_path:
        crawler_path = os.path.join(PROJECT_ROOT, 'tools', 'web_admin', 'crawler_generic.py')
        print(f'  使用通用抓取脚本')

    try:
        cmd = [sys.executable, crawler_path]
        # 通用脚本需要传URL参数
        if 'crawler_generic' in crawler_path:
            cmd.append(url)
        # zvcard专用脚本使用快速模式
        elif 'crawl_zvcard' in crawler_path:
            cmd.extend(['--mode', 'quick'])

        result = subprocess.run(
            cmd,
            capture_output=True, text=True, encoding='utf-8',
            errors='replace', timeout=180, cwd=PROJECT_ROOT
        )

        # 解析CRAWL_RESULT
        stdout = result.stdout
        for line in stdout.strip().split('\n'):
            line = line.strip()
            if line.startswith('CRAWL_RESULT:'):
                try:
                    data = json.loads(line.replace('CRAWL_RESULT:', ''))
                    if 'sites' in data and len(data['sites']) > 0:
                        return data
                except:
                    pass

        print(f'  抓取失败或无数据')
        if result.stderr:
            print(f'  错误: {result.stderr[:200]}')
        return None

    except subprocess.TimeoutExpired:
        print(f'  抓取超时')
        return None
    except Exception as e:
        print(f'  抓取异常: {e}')
        return None


def merge_sites(crawl_data, dry_run=False):
    """合并抓取数据到导航站"""
    sites = crawl_data.get('sites', [])
    if not sites:
        return 0, 0

    nav_data = load_nav_data()
    groups = nav_data.get('groups', [])
    existing_domains = set()
    existing_ids = set()

    for g in groups:
        for s in g.get('sites', []):
            domain = get_domain(s.get('url', ''))
            if domain:
                existing_domains.add(domain)
            if s.get('id'):
                existing_ids.add(s['id'])

    # 自动分类映射（优先使用LLM，准确率90%+）
    mappings = {}
    llm_mapped_urls = {}  # LLM分类的站点URL到分类ID的映射

    if LLM_AVAILABLE:
        print('  使用LLM自动分类（准确率90%+）...')
        try:
            llm_result = classify_and_map_sites(sites, platform='siliconflow', min_confidence=60)

            # LLM自动映射的站点
            for site, cat_id in llm_result['auto_mapped']:
                llm_mapped_urls[site.get('url', '')] = cat_id
                cat_info = next((c for c in get_all_categories_with_info() if c['id'] == cat_id), None)
                cat_name = cat_info['full_name'] if cat_info else str(cat_id)
                print(f'    LLM映射: {site["name"][:20]} -> {cat_name}')

            print(f'  LLM分类完成: 自动映射{len(llm_result["auto_mapped"])}个，待确认{len(llm_result["need_review"])}个，失败{len(llm_result["failed"])}个')

            # 待确认和失败的站点，回退到关键词匹配
            sites_for_keyword = [site for site, _, _ in llm_result['need_review']] + llm_result['failed']
        except Exception as e:
            print(f'  LLM分类失败，回退到关键词匹配: {e}')
            sites_for_keyword = sites
    else:
        sites_for_keyword = sites

    # 关键词匹配（LLM的补充）
    if AUTO_MAPPER_AVAILABLE and sites_for_keyword:
        print('  使用关键词匹配分类（LLM补充）...')
        categories = get_all_categories_with_info()

        # 按原分类分组
        by_source_cat = defaultdict(list)
        for site in sites_for_keyword:
            src_cat = site.get('category', '未分类')
            by_source_cat[src_cat].append(site)

        for src_cat, cat_sites in by_source_cat.items():
            if src_cat == '未分类' or src_cat == '':
                # 对于未分类的站点，逐个映射
                site_mappings = {}
                for site in cat_sites:
                    recs = auto_map_category(
                        site.get('name', ''),
                        site.get('description', ''),
                        src_cat,
                        categories
                    )
                    if recs and recs[0]['score'] >= 0.6:
                        best = recs[0]
                        target_id = best['category_id']
                        if target_id not in site_mappings:
                            site_mappings[target_id] = []
                        site_mappings[target_id].append(site)
                        print(f'    关键词映射: {site["name"][:20]} -> {best["full_name"]} ({best["score"]*100:.0f}%)')

                if site_mappings:
                    best_target = max(site_mappings.items(), key=lambda x: len(x[1]))[0]
                    mappings[src_cat] = best_target
                    mappings['_uncategorized_sites'] = site_mappings
            else:
                # 有明确原分类的，按分组投票映射
                auto_result = auto_map_all_sites(cat_sites, categories)
                info = auto_result.get(src_cat, {})
                if info.get('best_match') and info['best_match']['score'] >= 0.6:
                    mappings[src_cat] = info['best_match']['category_id']
                    print(f'    关键词映射: {src_cat} -> {info["best_match"]["full_name"]} ({info["best_match"]["score"]*100:.0f}%)')
                elif info.get('best_match'):
                    print(f'    跳过映射(置信度不足): {src_cat} -> {info["best_match"]["full_name"]} ({info["best_match"]["score"]*100:.0f}%)')

    new_id = max(existing_ids) + 1 if existing_ids else 1
    added = 0
    duplicates = 0
    skipped_no_mapping = 0

    # 未分类站点的逐个映射结果
    uncategorized_mappings = mappings.pop('_uncategorized_sites', {})
    # 构建未分类站点URL到目标分类的映射
    uncategorized_url_map = {}
    for target_id, site_list in uncategorized_mappings.items():
        for site in site_list:
            uncategorized_url_map[site.get('url', '')] = target_id

    for site in sites:
        url = site.get('url', '')
        domain = get_domain(url)

        # 重复检测
        if domain and domain in existing_domains:
            duplicates += 1
            continue

        # 分类映射（优先LLM，其次关键词匹配）
        target_cat_id = llm_mapped_urls.get(url)

        if not target_cat_id:
            src_cat = site.get('category', '未分类')
            # 对于未分类站点，使用逐个映射结果
            if src_cat == '未分类' or src_cat == '':
                target_cat_id = uncategorized_url_map.get(url)
            else:
                target_cat_id = mappings.get(src_cat)

        if not target_cat_id:
            # 没有映射的跳过
            skipped_no_mapping += 1
            continue

        # 找到目标分类
        target_group = next((g for g in groups if g['id'] == int(target_cat_id)), None)
        if not target_group:
            continue

        if dry_run:
            added += 1
            continue

        # 添加站点
        new_site = {
            'id': new_id,
            'group_id': int(target_cat_id),
            'name': site.get('name', ''),
            'url': url,
            'icon': '',
            'description': site.get('description', ''),
            'description_en': site.get('description_en', ''),
            'notes': f'来源：{crawl_data.get("source_name", "轮询抓取")}',
            'order_num': new_id,
            'is_public': 1,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        target_group['sites'].append(new_site)
        existing_domains.add(domain)
        new_id += 1
        added += 1

    if not dry_run and added > 0:
        nav_data['exportDate'] = datetime.now().strftime('%Y-%m-%d')
        save_nav_data(nav_data)

    return added, duplicates, skipped_no_mapping


def generate_pages():
    """生成所有页面"""
    scripts = [
        ('tools/cache_favicons.py', '下载favicon'),
        ('tools/generate_new_html.py', '生成首页'),
        ('tools/generate_category_pages.py', '生成分类页'),
        ('tools/generate_site_detail_pages.py', '生成详情页'),
        ('tools/update_sitemap.py', '更新sitemap'),
    ]

    for script_path, desc in scripts:
        full_path = os.path.join(PROJECT_ROOT, script_path)
        if not os.path.exists(full_path):
            print(f'  跳过（不存在）: {desc}')
            continue

        print(f'  {desc}...')
        try:
            result = subprocess.run(
                [sys.executable, full_path],
                capture_output=True, text=True, encoding='utf-8',
                errors='replace', timeout=300, cwd=PROJECT_ROOT
            )
            if result.returncode == 0:
                print(f'    ✓ 完成')
            else:
                print(f'    ✗ 失败: {result.stderr[:100]}')
        except Exception as e:
            print(f'    ✗ 异常: {e}')


def git_commit(added_count):
    """git提交"""
    try:
        subprocess.run(['git', 'add', '-A'], cwd=PROJECT_ROOT, capture_output=True)
        commit_msg = f'每日自动抓取更新: 新增{added_count}个站点 ({datetime.now().strftime("%Y-%m-%d")})'
        result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd=PROJECT_ROOT, capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f'  ✓ 已提交: {commit_msg}')
            # 推送
            push_result = subprocess.run(
                ['git', 'push', 'origin', 'master'],
                cwd=PROJECT_ROOT, capture_output=True, text=True
            )
            if push_result.returncode == 0:
                print(f'  ✓ 已推送到GitHub')
            else:
                print(f'  ✗ 推送失败: {push_result.stderr[:100]}')
        else:
            print(f'  无变化或提交失败')
    except Exception as e:
        print(f'  Git异常: {e}')


def main():
    parser = argparse.ArgumentParser(description='每日轮询抓取脚本')
    parser.add_argument('--count', type=int, default=2, help='每次抓取站点数（默认2）')
    parser.add_argument('--dry-run', action='store_true', help='试运行，不修改数据')
    parser.add_argument('--force-domain', type=str, default=None, help='强制抓取指定域名')
    parser.add_argument('--no-git', action='store_true', help='不执行git提交')
    parser.add_argument('--no-generate', action='store_true', help='不生成页面')
    args = parser.parse_args()

    print('=' * 60)
    print('每日轮询抓取')
    print('=' * 60)
    print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'模式: {"试运行" if args.dry_run else "正式"}')
    print(f'抓取数量: {args.count}')
    print()

    # 1. 加载源站列表
    sources_data = load_sources()
    total_sources = len(sources_data.get('sites', {}))
    print(f'源站总数: {total_sources}')

    if total_sources == 0:
        print('错误: 源站列表为空，请先运行 discover_nav_sites.py 发现源站')
        return

    # 2. 选择要抓取的站点
    selected = select_sites(sources_data, args.count, args.force_domain)
    print(f'选中站点: {len(selected)}个')
    for domain in selected:
        info = sources_data['sites'].get(domain, {})
        print(f'  - {domain}: {info.get("title", "无标题")[:40]}')

    # 3. 逐个抓取
    total_added = 0
    total_duplicates = 0
    total_skipped = 0

    for domain in selected:
        info = sources_data['sites'].get(domain, {})
        url = info.get('url', f'https://{domain}')

        print(f'\n--- [{domain}] ---')

        # 抓取
        crawl_data = crawl_site(url, domain)

        if not crawl_data or not crawl_data.get('sites'):
            # 抓取失败
            info['status'] = 'failed'
            info['last_crawled'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            info['crawl_count'] = info.get('crawl_count', 0) + 1
            sources_data['sites'][domain] = info
            print(f'  状态: 失败')
            continue

        sites_count = len(crawl_data['sites'])
        print(f'  抓取到: {sites_count}个站点')

        # 合并
        added, duplicates, skipped = merge_sites(crawl_data, args.dry_run)
        total_added += added
        total_duplicates += duplicates
        total_skipped += skipped
        print(f'  新增: {added}个，重复: {duplicates}个，未映射跳过: {skipped}个')

        # 更新源站状态
        info['status'] = 'crawled'
        info['last_crawled'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info['crawl_count'] = info.get('crawl_count', 0) + 1
        info['sites_found'] = sites_count
        info['last_added'] = added
        sources_data['sites'][domain] = info

    # 4. 保存源站列表
    if not args.dry_run:
        sources_data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_sources(sources_data)

    # 5. 生成页面
    print(f'\n=== 生成页面 ===')
    if not args.dry_run and not args.no_generate and total_added > 0:
        generate_pages()
    else:
        print(f'  跳过（{("试运行" if args.dry_run else "无新增站点" if total_added == 0 else "指定不生成")}）')

    # 6. Git提交
    print(f'\n=== Git提交 ===')
    if not args.dry_run and not args.no_git and total_added > 0:
        git_commit(total_added)
    else:
        print(f'  跳过（{("试运行" if args.dry_run else "无新增站点" if total_added == 0 else "指定不提交")}）')

    # 7. 总结
    print()
    print('=' * 60)
    print('执行完成!')
    print('=' * 60)
    print(f'  抓取站点: {len(selected)}个')
    print(f'  新增站点: {total_added}个')
    print(f'  重复跳过: {total_duplicates}个')
    print(f'  未映射跳过: {total_skipped}个')
    print()
    if total_added > 0 and not args.dry_run:
        print('  Cloudflare将在1-2分钟内自动部署')


if __name__ == '__main__':
    main()
