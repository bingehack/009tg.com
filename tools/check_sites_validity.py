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

# 抑制SSL警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SiteValidator:
    """站点有效性检测器"""
    
    def __init__(self, timeout=10, max_workers=10, proxies=None):
        """
        初始化检测器
        
        Args:
            timeout: 请求超时时间（秒）
            max_workers: 并发线程数
            proxies: 代理设置，格式：{'http': 'http://proxy:port', 'https': 'http://proxy:port'}
        """
        self.timeout = timeout
        self.max_workers = max_workers
        self.proxies = proxies
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
        
        # 提取主域名（去掉路径后缀）
        from urllib.parse import urlparse
        parsed = urlparse(url)
        main_url = f"{parsed.scheme}://{parsed.netloc}/"
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # 尝试多种方法访问站点
        methods = [
            ('HEAD', False),
            ('GET', False),
            ('HEAD', True),  # 禁用SSL验证
            ('GET', True)    # 禁用SSL验证
        ]
        
        for method, verify_ssl in methods:
            try:
                if method == 'HEAD':
                    response = requests.head(main_url, headers=headers, timeout=self.timeout, 
                                          allow_redirects=True, proxies=self.proxies, verify=verify_ssl)
                else:
                    response = requests.get(main_url, headers=headers, timeout=self.timeout, 
                                         allow_redirects=True, proxies=self.proxies, verify=verify_ssl)
                
                # 检查HTTP状态码
                if response.status_code >= 400:
                    if method == 'HEAD' and not verify_ssl:
                        continue  # 尝试下一个方法
                    return site_info, False, f"HTTP错误: {response.status_code}"
                
                # 检查内容类型（可选）
                content_type = response.headers.get('content-type', '')
                if 'text/html' not in content_type and 'application/json' not in content_type:
                    if method == 'HEAD' and not verify_ssl:
                        continue  # 尝试下一个方法
                    # 可能是文件下载，尝试GET请求
                    response = requests.get(main_url, headers=headers, timeout=self.timeout, 
                                         allow_redirects=True, stream=True, proxies=self.proxies, verify=verify_ssl)
                    if response.status_code >= 400:
                        continue  # 尝试下一个方法
                
                return site_info, True, None
                
            except requests.exceptions.Timeout:
                if method != 'GET' or verify_ssl:
                    continue  # 尝试下一个方法
                return site_info, False, "连接超时"
            except requests.exceptions.SSLError as e:
                if verify_ssl:
                    continue  # 已经禁用了SSL验证还是失败，尝试下一个方法
                continue  # 尝试禁用SSL验证
            except requests.exceptions.ConnectionError:
                if method != 'GET' or verify_ssl:
                    continue  # 尝试下一个方法
                return site_info, False, "连接失败"
            except requests.exceptions.TooManyRedirects:
                return site_info, False, "重定向次数过多"
            except requests.exceptions.RequestException as e:
                if method != 'GET' or verify_ssl:
                    continue  # 尝试下一个方法
                return site_info, False, f"请求错误: {str(e)}"
            except Exception as e:
                if method != 'GET' or verify_ssl:
                    continue  # 尝试下一个方法
                return site_info, False, f"未知错误: {str(e)}"
        
        # 所有方法都失败
        return site_info, False, "所有访问方法均失败"
    
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
    
    def check_with_third_party_api(self, url):
        """
        使用第三方API检测站点是否真的无法访问
        
        Args:
            url: 网站URL
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # 构建API请求URL
            api_url = f"https://downforeveryoneorjustme.com/api/httpcheck/{url}"
            
            headers = {
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'priority': 'u=1, i',
                'referer': f'https://downforeveryoneorjustme.com/{url}?proto=https',
                'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
                'x-requested-with': 'svelte'
            }
            
            response = requests.get(api_url, headers=headers, timeout=10)
            
            # 检查响应状态码
            if response.status_code != 200:
                return None, f"API返回HTTP错误: {response.status_code}"
            
            # 检查响应内容
            if not response.text.strip():
                return None, f"API返回空响应"
            
            # 尝试解析JSON
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                # JSON解析失败，返回响应内容的前100个字符用于调试
                return None, f"API返回非JSON格式: {response.text[:100]}"
            
            # 检查API返回结果
            if data.get('isDown', False):
                # 站点确实无法访问
                return False, f"第三方API确认无法访问 (HTTP {data.get('statusCode', 'N/A')})"
            else:
                # 站点可以访问
                return True, None
                
        except requests.exceptions.Timeout:
            return None, f"API请求超时"
        except requests.exceptions.RequestException as e:
            return None, f"API请求错误: {str(e)}"
        except Exception as e:
            return None, f"API检测失败: {str(e)}"
    
    def verify_connection_failed_sites(self):
        """
        使用第三方API验证连接失败的站点
        
        Returns:
            tuple: (confirmed_failed_sites, recovered_sites)
        """
        connection_failed_sites = []
        for site in self.invalid_sites:
            url = site.get('url', '')
            error_msg = self.error_details.get(url, '')
            if error_msg == "连接失败" or error_msg == "所有访问方法均失败":
                connection_failed_sites.append(site)
        
        confirmed_failed_sites = []
        recovered_sites = []
        
        print(f"\n开始使用第三方API验证 {len(connection_failed_sites)} 个连接失败站点...")
        print("-" * 60)
        
        for i, site in enumerate(connection_failed_sites, 1):
            url = site.get('url', '')
            name = site.get('name', '未知')
            
            is_valid, api_error = self.check_with_third_party_api(url)
            
            if is_valid is False:
                # 第三方API确认无法访问
                confirmed_failed_sites.append(site)
                print(f"[{i}/{len(connection_failed_sites)}] ✗ {name} - {api_error}")
            elif is_valid is True:
                # 第三方API确认可以访问，恢复为有效站点
                recovered_sites.append(site)
                # 从无效站点列表中移除
                self.invalid_sites.remove(site)
                self.valid_sites.append(site)
                # 更新错误详情
                self.error_details[url] = "第三方API确认可访问（已恢复）"
                print(f"[{i}/{len(connection_failed_sites)}] ✓ {name} - 第三方API确认可访问")
            else:
                # API检测失败，保留原状态
                confirmed_failed_sites.append(site)
                print(f"[{i}/{len(connection_failed_sites)}] ? {name} - {api_error}")
        
        print("-" * 60)
        print(f"验证完成！确认失败: {len(confirmed_failed_sites)}, 恢复有效: {len(recovered_sites)}")
        
        return confirmed_failed_sites, recovered_sites
    
    def generate_connection_failed_report(self, output_file='connection_failed_sites.html', confirmed_failed_sites=None):
        """
        生成连接失败站点的HTML报告
        
        Args:
            output_file: 输出文件路径
            confirmed_failed_sites: 确认失败的站点列表（如果为None，则使用self.invalid_sites）
        """
        # 如果没有提供确认失败的站点列表，则从self.invalid_sites中筛选
        if confirmed_failed_sites is None:
            confirmed_failed_sites = []
            for site in self.invalid_sites:
                url = site.get('url', '')
                error_msg = self.error_details.get(url, '')
                if error_msg == "连接失败" or error_msg == "所有访问方法均失败":
                    confirmed_failed_sites.append(site)
        
        html_content = f'''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>连接失败站点报告</title>
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
            border-bottom: 2px solid #f44336;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #ffebee;
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
            color: #f44336;
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
            background-color: #f44336;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .error-message {{
            color: #ff9800;
            font-size: 12px;
            font-weight: bold;
        }}
        .note {{
            background-color: #fff3e0;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
            border-left: 4px solid #ff9800;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>连接失败站点报告</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="note">
            <strong>注意：</strong>本报告列出了所有"连接失败"和"所有访问方法均失败"的站点。这些站点可能已经失效或无法访问。请手动验证后决定是否删除。
        </div>
        
        <div class="summary">
            <div class="summary-item">
                连接失败站点数: <strong>{len(confirmed_failed_sites)}</strong>
            </div>
            <div class="summary-item">
                总无效站点数: <strong>{len(self.invalid_sites)}</strong>
            </div>
        </div>
        
        <h2>连接失败站点列表</h2>
        <table>
            <tr>
                <th>序号</th>
                <th>网站名称</th>
                <th>URL</th>
                <th>错误信息</th>
            </tr>
'''
        
        for i, site in enumerate(confirmed_failed_sites, 1):
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
    </div>
</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"连接失败站点报告已生成: {output_file}")
        return len(confirmed_failed_sites)

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


def remove_invalid_sites(data, invalid_sites, output_file='完整版导航_cleaned.json', error_details=None):
    """
    从JSON数据中删除无效站点
    
    Args:
        data: 原始JSON数据
        invalid_sites: 无效站点列表
        output_file: 输出文件路径
        error_details: 错误详情字典，用于筛选特定类型的错误
    """
    invalid_urls = {site.get('url', '') for site in invalid_sites}
    
    # 如果指定了error_details，只删除"连接失败"和"所有访问方法均失败"的站点
    if error_details:
        connection_failed_urls = {
            url for url, error in error_details.items() 
            if error == "连接失败" or error == "所有访问方法均失败"
        }
        invalid_urls = connection_failed_urls
        print(f"筛选：只删除'连接失败'和'所有访问方法均失败'的站点，共 {len(invalid_urls)} 个")
        print("-" * 60)
    
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
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 切换到项目根目录
    os.chdir(project_root)
    
    parser = argparse.ArgumentParser(description='站点有效性检测脚本')
    parser.add_argument('--file', default='完整版导航.json', help='JSON数据文件路径')
    parser.add_argument('--timeout', type=int, default=10, help='请求超时时间（秒）')
    parser.add_argument('--workers', type=int, default=10, help='并发线程数')
    parser.add_argument('--delete', action='store_true', help='删除无效站点')
    parser.add_argument('--output', default='site_validity_report.html', help='报告输出文件路径')
    parser.add_argument('--proxy', help='代理地址，格式：http://proxy:port 或 socks5://proxy:port')
    
    args = parser.parse_args()
    
    # 设置代理
    proxies = None
    if args.proxy:
        proxies = {
            'http': args.proxy,
            'https': args.proxy
        }
        print(f"使用指定代理: {args.proxy}")
        print("-" * 60)
    else:
        # 自动检测Windows系统代理
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
            proxy_enable, _ = winreg.QueryValueEx(key, 'ProxyEnable')
            if proxy_enable == 1:
                proxy_server, _ = winreg.QueryValueEx(key, 'ProxyServer')
                if proxy_server:
                    # 处理可能的协议前缀
                    if not proxy_server.startswith('http') and not proxy_server.startswith('socks'):
                        proxy_server = 'http://' + proxy_server
                    proxies = {
                        'http': proxy_server,
                        'https': proxy_server
                    }
                    print(f"检测到Windows系统代理已启用: {proxy_server}")
                    print("-" * 60)
                winreg.CloseKey(key)
            winreg.CloseKey(registry)
        except ImportError:
            print("非Windows系统，跳过系统代理检测")
        except Exception as e:
            print(f"检测系统代理失败: {e}，将不使用代理")
    
    if not proxies:
        print("未使用代理（国外站点可能因网络问题检测为超时）")
        print("-" * 60)
    
    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"错误: 文件 '{args.file}' 不存在")
        return
    
    # 读取JSON数据
    print(f"读取数据文件: {args.file}")
    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取所有网站
    sites = extract_all_sites(data)
    print(f"找到 {len(sites)} 个网站")
    print("-" * 60)
    
    # 创建检测器并检测
    validator = SiteValidator(timeout=args.timeout, max_workers=args.workers, proxies=proxies)
    valid_sites, invalid_sites, error_details = validator.validate_sites(sites)
    
    # 使用第三方API验证连接失败的站点
    confirmed_failed_sites, recovered_sites = validator.verify_connection_failed_sites()
    
    # 生成完整检测报告
    validator.generate_report(args.output)
    
    # 生成连接失败站点报告（使用确认失败的站点列表）
    validator.generate_connection_failed_report('connection_failed_sites.html', confirmed_failed_sites)
    
    # 显示摘要信息
    print()
    print("=" * 60)
    print("检测完成！")
    print(f"总站点数: {len(sites)}")
    print(f"有效站点: {len(validator.valid_sites)}")
    print(f"无效站点: {len(validator.invalid_sites)}")
    print(f"第三方API确认失败: {len(confirmed_failed_sites)}")
    print(f"第三方API恢复有效: {len(recovered_sites)}")
    print("=" * 60)
    print()
    print("已生成以下报告：")
    print(f"1. 完整检测报告: {args.output}")
    print(f"2. 连接失败站点报告: connection_failed_sites.html")
    print()
    print("请查看 'connection_failed_sites.html' 文件，确认后决定是否删除。")


if __name__ == '__main__':
    main()
