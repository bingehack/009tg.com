# tools/crawler/ - 导航站抓取脚本

用于从同类导航站批量抓取站点数据，输出到 `raw/` 目录，再由 `build_data.py` 合并到 `完整版导航.json`。

## 已完成的抓取源站

| 脚本 | 目标站 | 站点类型 | 数据获取方式 | 新增站点 |
|---|---|---|---|---|
| `crawl_aididai.py` | AI地带 (aididai.cn) | 服务端渲染 | HTML解析+详情页base64解码 | 605 |
| `crawl_tbox.py` | Tbox导航 (tboxn.com) | 服务端渲染 | HTML解析+data-url属性 | 197 |
| `crawl_tudingai.py` | 图钉AI (tudingai.com) | 服务端渲染 | HTML解析+data-url属性 | 183 |
| `crawl_aih.py` | AIH超级导航站 (aimomap.cn) | 纯JS渲染 | 直接下载data.json | 317 |

## 两种站点类型的处理方式

### 类型A：服务端渲染站

HTML中直接包含工具卡片，用BeautifulSoup解析即可。

**判断方法**：在浏览器中查看页面源代码（Ctrl+U），搜索工具名称，如果能找到就是服务端渲染。

**常见结构**：
- 工具卡片：`a.sites-body`、`div.site-card`、`div.tool-item` 等
- 真实URL：可能在 `data-url` 属性、`href` 属性、或需要访问详情页解码
- 分类容器：`div.content-card`、`div.category` 等

**示例**（Tbox/图钉AI）：
```python
# 工具卡片直接包含真实URL
for site_a in card.find_all('a', class_='sites-body'):
    name = site_a.find('h3', class_='item-title').get_text(strip=True)
    url = site_a.get('data-url', '')  # 直接从data-url属性获取
```

**示例**（AI地带，需要访问详情页）：
```python
# 卡片链接是内部详情页，需要访问详情页解码真实URL
# 详情页"打开网站"按钮包含 /go/?url=base64(真实URL)
import base64
detail_html = fetch_page(detail_url)
go_link = detail_soup.find('a', href=lambda h: h and '/go/?url=' in h)
encoded_url = go_link['href'].split('/go/?url=')[1]
real_url = base64.b64decode(encoded_url).decode('utf-8')
```

### 类型B：纯JS渲染站

HTML中没有工具内容，靠JS动态加载。需要找到数据源。

**判断方法**：页面源代码中找不到工具名称，只有空的容器和JS脚本。

**解决方案（按优先级）**：

1. **检查独立JSON数据文件**
   - 常见文件名：`data.json`、`sites.json`、`api/data`、`/api/sites`
   - 在HTML的script标签中搜索 `DATA_URL`、`data.json`、`fetch(` 等关键词
   - 直接用requests下载JSON文件，json.loads解析

2. **检查HTML中内联的JS变量**
   - 搜索 `const allSites = [`、`var data = [`、`window.__DATA__ =` 等
   - 用正则提取JS变量中的JSON数据

3. **用浏览器开发者工具抓API**
   - F12 → Network → XHR/Fetch，刷新页面
   - 找到返回站点数据的API请求
   - 直接调用API获取数据

4. **Selenium/Playwright（最后手段）**
   - 以上都不行才考虑，因为需要安装浏览器驱动，运行慢

**示例**（AIH超级导航站）：
```python
# HTML中发现 const AppConfig = { DATA_URL: 'data.json' }
# 直接下载data.json
import requests
r = requests.get('https://www.aimomap.cn/data.json')
data = r.json()  # 直接是分类+站点的列表
for category in data:
    cat_name = category['category']
    for sub in category.get('subcategories', []):
        for site in sub['sites']:
            name = site['name']
            url = site['url']
            description = site['description']
```

## 目录结构

```
tools/crawler/
├── README.md              # 本文件
├── crawler_utils.py       # 通用工具模块（请求、去重、输出等）
├── _template.py           # 抓取脚本模板（复制后修改）
└── crawl_*.py             # 各目标站的抓取脚本（基于模板创建）
```

## 依赖安装

```bash
pip install requests beautifulsoup4
```

## 工作流程

```
抓取脚本(crawl_*.py) → raw/目录 → build_data.py → 完整版导航.json → generate_new_html.py → index.html
```

1. **抓取脚本** 从目标导航站抓取分类和站点，去重后输出到 `raw/` 目录
2. **build_data.py** 扫描 `raw/` 目录，合并去重后写入 `完整版导航.json`
3. **generate_new_html.py** 从 JSON 生成 HTML

## 编写新抓取脚本的步骤

### 1. 分析目标站结构

先确定是服务端渲染还是纯JS渲染，参考上方"两种站点类型的处理方式"。

### 2. 复制模板

```bash
cp tools/crawler/_template.py tools/crawler/crawl_目标站名称.py
```

### 3. 修改 CONFIG 配置区

```python
CONFIG = {
    'source_name': '目标站名称',        # 来源标识（用于输出文件名）
    'base_url': 'https://www.example.com',  # 目标站首页（服务端渲染）
    # 或
    'data_url': 'https://www.example.com/data.json',  # 数据文件URL（纯JS渲染）
    'output_dir': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'raw'),
}
```

注意：**分类映射不在抓取脚本中维护**，统一在 `tools/category_mapping.yaml` 中配置。抓取脚本只负责按源站的原始分类名输出raw文件，build_data.py会根据映射表自动归类。

### 4. 实现数据解析逻辑

根据站点类型实现不同的解析逻辑：

**服务端渲染站**：
- 用 `fetch_page()` 下载HTML
- 用 BeautifulSoup 解析分类容器和工具卡片
- 提取名称、URL、描述
- 清理URL追踪参数和名称标记

**纯JS渲染站**：
- 用 requests 直接下载JSON数据文件
- 用 json.loads() 解析
- 遍历分类和站点

### 5. 运行

```bash
python tools/crawler/crawl_目标站名称.py
```

### 6. 添加分类映射

编辑 `tools/category_mapping.yaml`，在末尾追加：

```yaml
目标站名称:
  源分类名1: 目标分类名1
  源分类名2: 目标分类名2
```

### 7. 合并并生成

```bash
python tools/build_data.py       # 合并raw/到完整版导航.json
python tools/cache_favicons.py   # 下载favicon
python tools/generate_new_html.py # 生成HTML
```

## 通用工具模块 (crawler_utils.py)

### 常用函数

| 函数 | 说明 |
|---|---|
| `fetch_page(url, timeout, retries, delay_range)` | 抓取网页，带重试和随机UA |
| `polite_sleep(delay_range)` | 礼貌延迟 |
| `get_domain(url)` | 提取域名（小写，去www） |
| `normalize_url(url)` | 规范化URL |
| `is_valid_site_url(url)` | 判断是否为有效工具站（过滤内容站） |
| `clean_text(text)` | 清洗文本（去HTML标签、多余空格） |
| `truncate_text(text, max_len)` | 截断文本 |
| `load_existing_domains()` | 加载完整版导航.json中已有域名 |
| `load_raw_domains()` | 加载raw/目录中待合并域名 |
| `save_raw_output(category, sites, source_name, parent_category)` | 保存为raw格式JSON |
| `print_crawl_summary(...)` | 打印抓取统计 |

### 去重机制

抓取脚本会自动加载两个去重池：
1. `完整版导航.json` 中已有的站点域名
2. `raw/` 目录中已抓取但尚未合并的站点域名

避免重复抓取和重复添加。

## 输出格式

抓取结果输出到 `raw/` 目录，文件名格式：`{source_name}_{category_name}.json`

文件内容为标准 raw 格式，可直接被 `build_data.py` 合并：

```json
{
  "category": "AI常用工具",
  "parent_category": "下海推荐",
  "source": "ai_tools_cn",
  "updated_at": "2026-09-04",
  "sites": [
    {
      "name": "站点名",
      "url": "https://example.com",
      "description": "站点描述",
      "icon": "",
      "tags": [],
      "status": "verified"
    }
  ]
}
```

## 完整使用流程

```bash
# 1. 运行抓取脚本
python tools/crawler/crawl_ai_tools_cn.py

# 2. 检查 raw/ 目录的输出
ls raw/

# 3. 合并数据到完整版导航.json
python tools/build_data.py

# 4. 下载新站点的 favicon
python tools/cache_favicons.py

# 5. 重新生成 HTML
python tools/generate_new_html.py

# 6. 提交部署
git add .
git commit -m "添加从xxx抓取的新站点"
git push
```

## 注意事项

1. **遵守目标站的 robots.txt 和使用条款**，不要对小站造成过大压力
2. **请求延迟** 默认 1-3 秒，不要调得太低
3. **分类映射** 建议在抓取前做好，避免输出到错误的分类
4. **人工抽检** 抓取完成后建议抽检 10-20% 的站点，确认描述和分类正确
5. **去重** 脚本会自动去重，但如果目标站本身有重复站点，可能需要人工清理
6. **icon 字段** 抓取时如果能拿到图标URL就填，留空则由 cache_favicons.py 自动下载
