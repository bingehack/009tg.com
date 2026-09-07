# 009tg下海导航

一个专注于创业、副业、投资、跨境电商、AI工具等领域的网址导航网站，纯静态部署在 Cloudflare Pages。

## 项目简介

009tg下海导航致力于打造国内最好的互联网优质网站网址大全，收录了全网好用强大的网站网址和软件，包括创业、副业、投资、跨境电商、营销工具、AI工具、社交媒体、独立站、广告投放、生活、休闲、办公、工具、资源等超全面的网址和职业技巧内容。

## 项目特性

- 精选优质网站，覆盖创业、副业、投资、跨境电商、AI工具等多个领域
- 响应式设计，支持桌面端和移动端访问
- 纯静态网站，部署简单快速（Cloudflare Pages）
- 本地 favicon 缓存，提升加载速度
- 三层分离数据架构（raw/ → build_data.py → 完整版导航.json → generate_new_html.py）
- 统一分类映射表，抓取层与分类层解耦
- 自动化抓取框架，支持服务端渲染站和纯JS渲染站

## 当前数据规模

- 分类数：105
- 站点数：2447
- 已抓取源站：4个（AI地带、Tbox导航、图钉AI、AIH超级导航站）

## 项目结构

```
009tg.com/
├── assets/                    # 静态资源文件
│   ├── css/                  # 样式文件
│   ├── js/                   # JavaScript文件
│   ├── images/               # 图片资源（含默认图标 default.png）
│   │   └── logos/            # 设计类网站图标
│   └── favicons/             # 网站favicon缓存（MD5命名PNG）
├── raw/                       # 抓取原始数据（按源站+分类分文件）
│   ├── README.md
│   ├── _template.json
│   ├── AI地带_*.json          # AI地带抓取结果（17个分类）
│   ├── Tbox导航_*.json        # Tbox导航抓取结果（16个分类）
│   ├── 图钉AI导航_*.json      # 图钉AI抓取结果（22个分类）
│   └── AIH超级导航站_*.json   # AIH抓取结果（22个分类）
├── tools/                     # 开发工具脚本
│   ├── README.md
│   ├── build_data.py          # 【核心】合并raw/数据到完整版导航.json
│   ├── generate_new_html.py   # 【核心】从JSON生成HTML
│   ├── cache_favicons.py      # 【核心】批量下载favicon
│   ├── category_mapping.yaml  # 【核心】统一分类映射表
│   ├── check_sites_validity.py # 站点有效性检测
│   ├── remove_invalid_sites.py # 删除无效站点
│   ├── list_categories.py     # 查看分类结构
│   ├── cleanup_json.py        # JSON清理（删除冗余字段）
│   ├── verify_cleanup.py      # 数据完整性验证
│   ├── check_all_favicons.py  # 检查favicon文件有效性
│   ├── fix_favicon_urls.py    # 修复favicon URL格式
│   ├── add_default_src.py     # 为图片添加默认src属性
│   ├── fix_javascript_escape.py # 修复JS转义变量
│   ├── fix_javascript_img.py  # 修复JS动态生成的img标签
│   └── crawler/               # 抓取脚本目录
│       ├── README.md
│       ├── crawler_utils.py   # 通用工具模块（请求、去重、输出等）
│       ├── _template.py       # 抓取脚本模板
│       ├── crawl_aididai.py   # AI地带抓取脚本
│       ├── crawl_tbox.py      # Tbox导航抓取脚本
│       ├── crawl_tudingai.py  # 图钉AI抓取脚本
│       └── crawl_aih.py       # AIH超级导航站抓取脚本
├── index.html                  # 生成的首页（中文）
├── 404.html                   # 404错误页面
├── redirect.html              # 跳转页面
├── 完整版导航.json             # 【核心】网站数据源（合并后的完整数据）
├── favicon_mapping.json       # 域名→本地favicon路径映射
├── README.md                   # 本文件
└── LICENSE
```

## 三层分离数据架构

```
抓取脚本(crawl_*.py) → raw/目录(按分类分文件) → build_data.py(按映射表归类合并) → 完整版导航.json → generate_new_html.py → index.html
```

### 各层职责

1. **raw/ 层**：抓取脚本输出的原始数据，每个源站每个分类一个JSON文件，便于追溯和增量更新
2. **build_data.py**：扫描raw/下所有JSON，按`category_mapping.yaml`映射表归类，域名双重去重，自动分配id，合并到完整版导航.json
3. **完整版导航.json**：合并后的完整数据，是HTML生成的唯一数据源
4. **generate_new_html.py**：读取完整版导航.json和favicon_mapping.json，生成index.html

### 为什么这样设计

- **可追溯**：每个站点都能追溯到来源（raw/文件名）
- **增量更新**：新增抓取源站只需添加raw文件，不影响已有数据
- **分类集中管理**：所有分类映射在category_mapping.yaml，新增源站只需追加映射规则
- **去重安全**：build_data.py按域名双重去重（已有数据+raw内），不会重复添加

## 核心数据文件说明

### 完整版导航.json

网站的唯一数据源，结构如下：

```json
{
  "groups": [
    {
      "id": 10,
      "name": "AI工具",
      "order_num": 1,
      "parent_id": null,
      "sites": []
    },
    {
      "id": 11,
      "name": "AI常用工具",
      "order_num": 1,
      "parent_id": 10,
      "sites": [
        {
          "id": 1,
          "group_id": 11,
          "name": "站点名",
          "url": "https://example.com",
          "icon": "assets/favicons/xxx.png",
          "description": "站点描述",
          "notes": "",
          "order_num": 1,
          "is_public": true,
          "created_at": "2026-01-01",
          "updated_at": "2026-01-01"
        }
      ]
    }
  ],
  "version": "1.0",
  "exportDate": "2026-09-05"
}
```

- `parent_id: null` 表示一级分类
- `parent_id: 10` 表示父分类是id=10的分类
- 一级分类的`sites`通常为空，站点都放在子分类下

### category_mapping.yaml

统一分类映射表，抓取层与分类层解耦的核心。结构如下：

```yaml
_default:
  parent_category: AI工具
  fallback_category: AI常用工具

AI地带:
  AI写作工具: AI写作工具
  AI视频工具: AI视频工具
  ...

Tbox导航:
  AI工具: AI常用工具
  多媒体工具: 素材编辑
  ...

图钉AI导航:
  聊天机器: AI对话
  图像绘画: AI图像工具
  ...

AIH超级导航站:
  写作辅助: AI写作工具
  办公效率: AI办公工具
  ...
```

- `_default.parent_category`：新建分类时的默认父分类
- `_default.fallback_category`：未匹配分类时的兜底分类
- 每个源站下列出"源分类名: 目标分类名"
- 目标分类名必须是完整版导航.json中已存在的分类名
- build_data.py会先按"父分类+分类名"精确匹配，失败时降级全局匹配

### favicon_mapping.json

域名到本地favicon路径的映射：

```json
{
  "example.com": "assets/favicons/abc123.png",
  "another.com": "assets/favicons/def456.png"
}
```

- generate_new_html.py读取此映射，为每个站点设置icon字段
- 下载失败的站点会复制默认图标`assets/images/logos/default.png`

## 工具脚本说明

### 核心脚本（日常使用）

| 脚本 | 功能 | 用法 |
|---|---|---|
| `build_data.py` | 合并raw/数据到完整版导航.json | `python tools/build_data.py` |
| `generate_new_html.py` | 从JSON生成HTML | `python tools/generate_new_html.py` |
| `cache_favicons.py` | 批量下载favicon（多源重试+默认图标兜底） | `python tools/cache_favicons.py` |
| `check_sites_validity.py` | 检测站点有效性（并发+超时+第三方API验证） | `python tools/check_sites_validity.py` |
| `remove_invalid_sites.py` | 从JSON删除无效站点（需先生成检测报告） | `python tools/remove_invalid_sites.py` |

### 辅助脚本

| 脚本 | 功能 |
|---|---|
| `list_categories.py` | 查看分类结构（一级/二级/站点数） |
| `cleanup_json.py` | JSON清理（删除冗余的顶层sites和configs字段） |
| `verify_cleanup.py` | 数据完整性验证 |
| `check_all_favicons.py` | 检查favicon文件有效性，删除无效PNG |
| `fix_favicon_urls.py` | 修复favicon URL格式 |
| `add_default_src.py` | 为懒加载图片添加默认src属性 |
| `fix_javascript_escape.py` | 修复JS模板变量转义 |
| `fix_javascript_img.py` | 修复JS动态生成的img标签 |

### 抓取脚本（tools/crawler/）

| 脚本 | 目标站 | 站点类型 | 数据获取方式 | 新增站点 |
|---|---|---|---|---|
| `crawl_aididai.py` | AI地带 (aididai.cn) | 服务端渲染 | HTML解析+详情页base64解码 | 605 |
| `crawl_tbox.py` | Tbox导航 (tboxn.com) | 服务端渲染 | HTML解析+data-url属性 | 197 |
| `crawl_tudingai.py` | 图钉AI (tudingai.com) | 服务端渲染 | HTML解析+data-url属性 | 183 |
| `crawl_aih.py` | AIH超级导航站 (aimomap.cn) | 纯JS渲染 | 直接下载data.json | 317 |

通用工具模块 `crawler_utils.py` 提供：
- `fetch_page()`：抓取网页，带随机UA、重试、编码检测
- `get_domain()`：提取域名（小写，去www）
- `normalize_url()`：规范化URL
- `is_valid_site_url()`：判断是否为有效工具站
- `load_existing_domains()`：加载已有域名去重池
- `save_raw_output()`：保存为标准raw格式JSON
- `print_crawl_summary()`：打印抓取统计

## 完整操作流程

### 日常维护流程（添加/修改站点后）

```bash
# 1. 编辑完整版导航.json添加或修改网站
# （或通过抓取脚本自动添加）

# 2. 检测新站点有效性（可选）
python tools/check_sites_validity.py

# 3. 下载/更新favicon
python tools/cache_favicons.py

# 4. 重新生成HTML
python tools/generate_new_html.py

# 5. 本地预览
python -m http.server 8000
# 访问 http://localhost:8000

# 6. 提交部署
git add .
git commit -m "更新站点数据"
git push
```

### 抓取新站点的完整流程

```bash
# 1. 编写抓取脚本（参考下方"新增抓取源站步骤"）
# 复制模板后修改
cp tools/crawler/_template.py tools/crawler/crawl_新站.py

# 2. 运行抓取脚本
python tools/crawler/crawl_新站.py
# 输出到 raw/新站_分类名.json

# 3. 在category_mapping.yaml中添加分类映射
# 编辑 tools/category_mapping.yaml，追加：
# 新站:
#   源分类名: 目标分类名

# 4. 合并数据到完整版导航.json
python tools/build_data.py
# 会自动备份为 完整版导航.json.build_backup

# 5. 下载新站点的favicon
python tools/cache_favicons.py

# 6. 重新生成HTML
python tools/generate_new_html.py

# 7. 本地预览验证
python -m http.server 8000

# 8. 提交部署
git add .
git commit -m "添加从XX站抓取的新站点"
git push
```

### 清理无效站点流程

```bash
# 1. 检测站点有效性
python tools/check_sites_validity.py
# 生成 site_validity_report.html 和 connection_failed_sites.html

# 2. 查看检测报告，确认要删除的站点
# （注意：国外站点超时可能是国内网络问题，不一定是真失效）

# 3. 删除无效站点
python tools/remove_invalid_sites.py
# 自动备份、删除、重新生成HTML

# 4. 提交部署
git add .
git commit -m "清理无效站点"
git push
```

## 新增抓取源站步骤

### 步骤1：分析目标站结构

先确定目标站的数据获取方式：

**类型A：服务端渲染站**（HTML中直接包含工具卡片）
- 用浏览器查看页面源代码，搜索工具名称
- 如果能在HTML中找到，就是服务端渲染
- 需要分析：分类容器选择器、工具卡片选择器、名称/描述/URL的获取方式

**类型B：纯JS渲染站**（HTML中没有工具内容，靠JS动态加载）
- 页面源代码中找不到工具名称
- 解决方案：
  1. 检查是否有独立的JSON数据文件（如data.json、api/data）
  2. 检查HTML中是否有内联的JS变量（如`const allSites = [...]`）
  3. 用浏览器开发者工具Network面板抓API请求
  4. 以上都不行才考虑Selenium/Playwright

### 步骤2：复制模板并修改

```bash
cp tools/crawler/_template.py tools/crawler/crawl_目标站.py
```

修改内容：
1. **CONFIG区**：source_name、base_url（或data_url）
2. **数据获取逻辑**：
   - 服务端渲染：用fetch_page下载HTML，BeautifulSoup解析
   - 纯JS渲染：直接用requests下载JSON文件，json.loads解析
3. **解析函数**：提取分类名、站点名、URL、描述
4. **URL清理**：去除追踪参数（utm_、ref、channel等）
5. **名称清理**：去除推荐标记（"荐"、"新"等）

### 步骤3：添加分类映射

编辑 `tools/category_mapping.yaml`，在末尾追加：

```yaml
目标站名称:
  源分类名1: 目标分类名1
  源分类名2: 目标分类名2
  ...
```

- 目标分类名必须是完整版导航.json中已存在的分类
- 不确定的分类可以先映射到兜底分类（AI常用工具），后续人工调整
- 运行build_data.py时会显示每个分类的匹配结果，便于检查

### 步骤4：测试运行

```bash
# 语法检查
python -m py_compile tools/crawler/crawl_目标站.py

# 运行抓取
python tools/crawler/crawl_目标站.py

# 检查raw/输出
ls raw/目标站_*.json
```

### 步骤5：合并验证

```bash
# 合并
python tools/build_data.py
# 检查输出：匹配现有分类数、新建分类数、成功添加数

# 下载favicon
python tools/cache_favicons.py

# 生成HTML
python tools/generate_new_html.py

# 本地预览
python -m http.server 8000
```

## 部署到 Cloudflare Pages

### 前置条件

1. GitHub账号
2. Cloudflare账号
3. 项目代码已推送到GitHub仓库

### 部署步骤

#### 步骤1：推送代码到GitHub

```bash
cd 009tg.com
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/009tg.com.git
git push -u origin master
```

#### 步骤2：在Cloudflare Pages中连接仓库

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 **Workers & Pages** → **Create a project**
3. 点击 **Connect to Git**
4. 选择 **GitHub**，授权Cloudflare访问你的GitHub账号
5. 选择你的仓库（009tg.com）
6. 点击 **Begin setup**

#### 步骤3：配置构建参数

由于是纯静态网站，不需要构建命令：

- **Framework preset**：None
- **Build command**：留空
- **Build output directory**：`/`（根目录）

点击 **Save and Deploy** 开始部署。

#### 步骤4：配置自定义域名

1. 在Cloudflare Pages项目中，点击 **Custom domains**
2. 点击 **Set up a custom domain**
3. 输入你的域名，例如：`009tg.com`
4. Cloudflare会自动配置DNS记录（如果域名在Cloudflare管理）
5. 如果域名不在Cloudflare，需要手动添加CNAME记录指向你的Pages域名
6. 等待SSL证书自动生成（通常几分钟）

#### 步骤5：验证部署

1. 访问你的自定义域名：`https://009tg.com`
2. 确认网站正常访问，所有链接和图标正常

### 自动部署

Cloudflare Pages支持Git自动部署：
- 每次推送代码到GitHub的master分支，Cloudflare会自动重新部署
- 通常1-2分钟内完成
- 可以在Cloudflare Dashboard → Pages项目 → Deployments查看部署历史和日志

### 部署注意事项

1. **.gitignore**：确保不要提交临时文件（分析脚本、临时HTML等）
2. **大文件**：favicon目录可能有上千个PNG文件，首次推送可能较慢
3. **404页面**：项目已包含404.html，Cloudflare Pages会自动使用
4. **缓存**：Cloudflare会缓存静态资源，更新后可能需要强制刷新（Ctrl+F5）

## 本地预览

```bash
cd 009tg.com
python -m http.server 8000
```

访问：
- 中文版：http://localhost:8000

## 常见问题

### Q: 如何添加新网站？

A: 有两种方式：
1. **手动添加**：编辑 `完整版导航.json`，按照现有格式添加站点信息，然后运行 `python tools/generate_new_html.py` 重新生成HTML
2. **自动抓取**：编写抓取脚本从同类导航站批量抓取，参考"新增抓取源站步骤"

### Q: 网站图标不显示（破裂）怎么办？

A: 按以下步骤排查：
1. 运行 `python tools/cache_favicons.py` 重新下载favicon
2. 检查 `assets/images/logos/default.png` 默认图标是否存在
3. 检查 `favicon_mapping.json` 中对应域名的映射路径是否正确
4. 检查 `assets/favicons/` 下对应的PNG文件是否存在
5. 重新生成HTML：`python tools/generate_new_html.py`

注意：cache_favicons.py下载失败的站点会自动复制默认图标，不会出现破裂。

### Q: 如何检测无效链接？

A: 运行 `python tools/check_sites_validity.py`，脚本会检测所有站点并生成报告。注意：国外站点超时可能是国内网络问题，不一定是真失效，建议人工确认后再删除。

### Q: 抓取脚本运行很慢怎么办？

A: 抓取速度主要取决于目标站的响应速度和反爬策略。可以：
1. 调整crawler_utils.py中fetch_page的timeout和retries参数
2. 调整请求延迟（默认1-3秒）
3. 对于纯JS渲染站，直接下载JSON文件比解析HTML快得多
4. 后台运行：`python tools/crawler/crawl_xxx.py &`

### Q: build_data.py 出现分类重复创建怎么办？

A: 检查category_mapping.yaml中的目标分类名是否与完整版导航.json中的分类名完全一致（包括空格、大小写）。build_data.py会先按"父分类+分类名"精确匹配，失败时降级全局匹配。如果仍然创建了重复分类，说明目标分类名拼写错误。

### Q: 如何回滚数据？

A: build_data.py每次运行前会自动备份为 `完整版导航.json.build_backup`。如需回滚：
```bash
cp 完整版导航.json.build_backup 完整版导航.json
python tools/generate_new_html.py
```

其他备份文件：
- `完整版导航.json.cleanup_backup`：清理前的完整备份
- `完整版导航.json.premapping_backup`：方案2实施前备份
- `完整版导航.json.fingerprint_backup`：分类调整前备份

## 技术栈

- **前端框架**：Bootstrap 3.x + Xenon
- **图标库**：Font Awesome, Linecons
- **JavaScript**：jQuery, TweenMax, Lozad（懒加载）
- **开发工具**：Python 3.x
- **依赖库**：requests, beautifulsoup4, pyyaml
- **部署平台**：Cloudflare Pages

## 维护指南

### 定期维护任务

1. **站点有效性检测**（每月）
   ```bash
   python tools/check_sites_validity.py
   ```

2. **删除无效站点**（根据检测结果，人工确认后）
   ```bash
   python tools/remove_invalid_sites.py
   ```

3. **更新favicon缓存**（新增站点后）
   ```bash
   python tools/cache_favicons.py
   ```

4. **重新生成HTML**（数据更新后）
   ```bash
   python tools/generate_new_html.py
   ```

5. **抓取新站点**（按需）
   ```bash
   python tools/crawler/crawl_新站.py
   python tools/build_data.py
   python tools/cache_favicons.py
   python tools/generate_new_html.py
   ```

## License

本项目采用 MIT License 开源协议。

> 本项目开源的目的是让大家能够在本站的基础之上有所启发，做出更多新的东西。如果你使用这个开源项目，请**注明**本项目开源地址。

## 联系方式

- 网站：https://009tg.com
- 作者：Invisible Man

---

如果这个项目对你有帮助，请给个Star支持一下！
