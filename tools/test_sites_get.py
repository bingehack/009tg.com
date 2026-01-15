import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 创建session并配置重试
session = requests.Session()
retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# 测试金色财经（使用GET请求）
try:
    r = session.get('https://www.jinse.com', headers=headers, proxies=proxies, timeout=10, allow_redirects=True)
    print(f'金色财经（GET请求）: {r.status_code}')
except Exception as e:
    print(f'金色财经（GET请求）: 错误 - {e}')

# 测试Dwz3短链工具（使用GET请求）
try:
    r = session.get('https://dwz3.cn/', headers=headers, proxies=proxies, timeout=10, allow_redirects=True)
    print(f'Dwz3短链工具（GET请求）: {r.status_code}')
except Exception as e:
    print(f'Dwz3短链工具（GET请求）: 错误 - {e}')
