import requests

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

# 测试金色财经（不使用代理）
try:
    r = requests.head('https://www.jinse.com', headers=headers, timeout=10)
    print(f'金色财经（无代理）: {r.status_code}')
except Exception as e:
    print(f'金色财经（无代理）: 错误 - {e}')

# 测试Dwz3短链工具（不使用代理）
try:
    r = requests.head('https://dwz3.cn/', headers=headers, timeout=10)
    print(f'Dwz3短链工具（无代理）: {r.status_code}')
except Exception as e:
    print(f'Dwz3短链工具（无代理）: 错误 - {e}')
