#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点有效性检测脚本

用途：
    批量检测网站列表中的站点是否可以正常访问，识别并标记无效站点。

功能概述：
    1. 从JSON数据文件中读取所有网站URL
    2. 对每个URL进行HTTP访问测试（支持超时设置）
    3. 识别无法访问的站点（超时、连接错误、HTTP错误等）
    4. 生成检测报告，列出所有无效站点
    5. 支持将无效站点从JSON数据中安全删除

使用方法：
    1. 基本检测（不删除数据）：
       python check_sites_validity.py

    2. 检测并删除无效站点：
       python check_sites_validity.py --delete

    3. 自定义超时时间（默认10秒）：
       python check_sites_validity.py --timeout 15

    4. 指定JSON文件路径：
       python check_sites_validity.py --file 完整版导航.json

主要特性：
    - 支持并发检测，提高检测效率
    - 支持自定义超时时间
    - 详细的错误日志记录
    - 生成HTML格式的检测报告
    - 支持备份原始数据
    - 安全的删除机制，避免误删
"""

import json
import requests
import argparse
import os
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse


class SiteValidator:
    """站点有效性检测器"""
    
    def __init__(self, timeout=10, max_workers=10):
        """
        初始化检测器
        
        Args:
            timeout: 请求超时时间（秒）
            max_workers: 并发线程数
        """
        self.timeout = timeout
        self.max_workers = max_workers
        self.invalid_sites = []
        self.valid_sites = []
        self.error_details = {}
        
    def check_site(self, site_info):
        """
        检测单个站点是否可访问
        
        Args:
            site_info: 网站信息字典，包含name, url等字段
            
        Returns:
            tuple: (site_info, is_valid, error_message)
        """
        url = site_info.get('url', '')
        if not url or url == '#':
            return site_info, False, "无效URL"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 发送HEAD请求（更快）
            response = requests.head(url, headers=headers, timeout=self.timeout, allow_redirects=True)
            
            # 检查HTTP状态码
            if response.status_code >= 400:
                return site_info, False, f"HTTP错误: {response.status_code}"
            
            # 检查内容类型（可选）
            content_type = response.headers.get('content-type', '')
            if 'text/html' not in content_type and 'application/json' not in content_type:
                # 可能是文件下载，尝试GET请求
                response = requests.get(url, headers=headers, timeout=self.timeout, allow_redirects=True, stream=True)
                if response.status_code >= 400:
                    return site_info, False, f"HTTP错误: {response.status_code}"
            
            return site_info, True, None
            
        except requests.exceptions.Timeout:
            return site_info, False, "连接超时"
        except requests.exceptions.ConnectionError:
            return site_info, False, "连接失败"
        except requests.exceptions.TooManyRedirects:
            return site_info, False, "重定向次数过多"
        except requests.exceptions.RequestException as e:
            return site_info, False, f"请求错误: {str(e)}"
        except Exception as e:
            return site_info, False, f"未知错误: {str(e)}"
    
    def validate_sites(self, sites):
        """
        批量检测站点
        
        Args:
            sites: 网站信息列表
            
        Returns:
            tuple: (valid_sites, invalid_sites, error_details)
        """
        print(f"开始检测 {len(sites)} 个站点...")
        print(f"超时设置: {self.timeout}秒")
        print(f"并发线程: {self.max_workers}")
        print("-" * 60)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_site = {executor.submit(self.check_site, site): site for site in sites}
            
            for i, future in enumerate(as_completed(future_to_site), 1):
                site_info, is_valid, error_msg = future.result()
                
                if is_valid:
                    self.valid_sites.append(site_info)
                    print(f"[{i}/{len(sites)}] ✓ {site_info.get('name', '未知')} - {site_info.get('url', '')}")
                else:
                    self.invalid_sites.append(site_info)
                    self.error_details[site_info.get('url', '')] = error_msg
                    print(f"[{i}/{len(sites)}] ✗ {site_info.get('name', '未知')} - {error_msg}")
        
        print("-" * 60)
        print(f"检测完成! 有效: {len(self.valid_sites)}, 无效: {len(self.invalid_sites)}")
        
        return self.valid_sites, self.invalid_sites, self.error_details
    
    def generate_report(self, output_file='site_validity_report.html'):
        """
        生成HTML格式的检测报告
        
        Args:
            output_file: 输出文件路径
        """
        html_content = f'''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>站点有效性检测报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }}
        .summary-item {{
            display: inline-block;
            margin: 0 20px 10px 0;
            font-size: 16px;
        }}
        .summary-item strong {{
            font-size: 24px;
            color: #4CAF50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .status-valid {{
            color: #4CAF50;
            font-weight: bold;
        }}
        .status-invalid {{
            color: #f44336;
            font-weight: bold;
        }}
        .error-message {{
            color: #ff9800;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>站点有效性检测报告</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="summary-item">
                总站点数: <strong>{len(self.valid_sites) + len(self.invalid_sites)}</strong>
            </div>
            <div class="summary-item">
                有效站点: <strong>{len(self.valid_sites)}</strong>
            </div>
            <div class="summary-item">
                无效站点: <strong>{len(self.invalid_sites)}</strong>
            </div>
        </div>
        
        <h2>无效站点列表</h2>
        <table>
            <tr>
                <th>序号</th>
                <th>网站名称</th>
                <th>URL</th>
                <th>错误信息</th>
            </tr>
'''
        
        for i, site in enumerate(self.invalid_sites, 1):
            url = site.get('url', '')
            error_msg = self.error_details.get(url, '未知错误')
            html_content += f'''
            <tr>
                <td>{i}</td>
                <td>{site.get('name', '未知')}</td>
                <td><a href="{url}" target="_blank">{url}</a></td>
                <td class="error-message">{error_msg}</td>
            </tr>
'''
        
        html_content += '''
        </table>
        
        <h2>有效站点列表（前100个）</h2>
        <table>
            <tr>
                <th>序号</th>
                <th>网站名称</th>
                <th>URL</th>
                <th>状态</th>
            </tr>
'''
        
        for i, site in enumerate(self.valid_sites[:100], 1):
            url = site.get('url', '')
            html_content += f'''
            <tr>
                <td>{i}</td>
                <td>{site.get('name', '未知')}</td>
                <td><a href="{url}" target="_blank">{url}</a></td>
                <td class="status-valid">✓ 正常</td>
            </tr>
'''
        
        html_content += '''
        </table>
    </div>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"检测报告已生成: {output_file}")


def extract_all_sites(data):
    """
    从JSON数据中提取所有网站
    
    Args:
        data: JSON数据字典
        
    Returns:
        list: 网站信息列表
    """
    sites = []
    
    def process_group(group):
        if 'sites' in group:
            for site in group['sites']:
                if 'url' in site and site['url']:
                    sites.append(site)
        if 'children' in group:
            for child in group['children']:
                process_group(child)
    
    for group in data.get('groups', []):
        process_group(group)
    
    return sites


def remove_invalid_sites(data, invalid_sites, output_file='完整版导航_cleaned.json'):
    """
    从JSON数据中删除无效站点
    
    Args:
        data: 原始JSON数据
        invalid_sites: 无效站点列表
        output_file: 输出文件路径
    """
    invalid_urls = {site.get('url', '') for site in invalid_sites}
    
    def process_group(group):
        if 'sites' in group:
            original_count = len(group['sites'])
            group['sites'] = [site for site in group['sites'] 
                           if site.get('url', '') not in invalid_urls]
            removed_count = original_count - len(group['sites'])
            if removed_count > 0:
                print(f"  分类 '{group.get('name', '未知')}' 删除了 {removed_count} 个无效站点")
        
        if 'children' in group:
            for child in group['children']:
                process_group(child)
    
    print(f"开始删除 {len(invalid_sites)} 个无效站点...")
    print("-" * 60)
    
    for group in data.get('groups', []):
        process_group(group)
    
    print("-" * 60)
    print(f"删除完成，保存到: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return output_file


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='站点有效性检测脚本')
    parser.add_argument('--file', default='完整版导航.json', help='JSON数据文件路径')
    parser.add_argument('--timeout', type=int, default=10, help='请求超时时间（秒）')
    parser.add_argument('--workers', type=int, default=10, help='并发线程数')
    parser.add_argument('--delete', action='store_true', help='删除无效站点')
    parser.add_argument('--output', default='site_validity_report.html', help='报告输出文件路径')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"错误: 文件 '{args.file}' 不存在")
        return
    
    # 备份原始文件
    if args.delete:
        backup_file = f"{args.file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(args.file, backup_file)
        print(f"已备份原始文件到: {backup_file}")
        print("-" * 60)
    
    # 读取JSON数据
    print(f"读取数据文件: {args.file}")
    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取所有网站
    sites = extract_all_sites(data)
    print(f"找到 {len(sites)} 个网站")
    print("-" * 60)
    
    # 创建检测器并检测
    validator = SiteValidator(timeout=args.timeout, max_workers=args.workers)
    valid_sites, invalid_sites, error_details = validator.validate_sites(sites)
    
    # 生成报告
    validator.generate_report(args.output)
    
    # 删除无效站点
    if args.delete and invalid_sites:
        print()
        print("警告: 即将删除无效站点！")
        confirm = input("确认删除? (yes/no): ")
        
        if confirm.lower() == 'yes':
            output_file = remove_invalid_sites(data, invalid_sites)
            print(f"✓ 清理后的数据已保存到: {output_file}")
        else:
            print("已取消删除操作")
    elif invalid_sites:
        print()
        print(f"发现 {len(invalid_sites)} 个无效站点")
        print("如需删除，请使用 --delete 参数")
        print("例如: python check_sites_validity.py --delete")


if __name__ == '__main__':
    main()
