# 009tg下海导航

一个专注于创业、副业、投资、跨境电商、AI工具等领域的网址导航网站，纯静态部署在 Cloudflare Pages，支持中英文双语。

## 项目简介

009tg下海导航致力于打造国内最好的互联网优质网站网址大全，收录了全网好用强大的网站网址和软件，包括创业、副业、投资、跨境电商、营销工具、AI工具、社交媒体、独立站、广告投放、生活、休闲、办公、工具、资源等超全面的网址和职业技巧内容。

## 项目特性

- 精选优质网站，覆盖创业、副业、投资、跨境电商、AI工具等多个领域
- 中英文双语支持（`/cn/` 中文站，`/en/` 英文站）
- 分类详情页（每个分类独立页面，支持分页浏览，每页32个站点）
- **深色模式**（全站支持深色/浅色切换，自动跟随系统偏好，localStorage保存用户选择）
- **文章资讯系统**（19篇分类指南文章，列表页+详情页，中英文双语）
- **站内搜索**（实时搜索2591个站点，支持名称/描述/URL/分类匹配，关键词高亮）
- 响应式设计，支持桌面端和移动端访问
- 纯静态网站，部署简单快速（Cloudflare Pages）
- 本地 favicon 缓存，提升加载速度
- 统一数据源（`完整版导航.json`），所有页面由脚本生成
- 自动化抓取框架，支持服务端渲染站和纯JS渲染站
- **Web管理后台**（本地Flask应用，支持抓取、合并、数据管理可视化操作）

## 当前数据规模

- 分类数：105（19个一级分类 + 86个子分类）
- 站点数：2591
- 文章数：19（每个一级分类一篇指南文章）
- 页面数：260+（首页2 + 标准页面10 + 分类详情页210 + 文章页面40）
- 已抓取源站：5个（AI地带、Tbox导航、图钉AI、AIH超级导航站、zvcard导航）

## 项目结构

```
009tg.com/
├── assets/                    # 【静态资源】不随数据变化，手动维护
│   ├── css/                  # 样式文件
│   ├── js/                   # JavaScript文件
│   ├── images/               # 图片资源（logo、默认图标等）
│   │   ├── logo@2x.png       # 白色文字logo（深色背景用）
│   │   ├── logo_dark@2x.png  # 白色文字logo（深色背景用）
│   │   ├── logo_light@2x.png # 黑色文字logo（白色背景用）
│   │   ├── logo_dark_light@2x.png # 黑色文字logo（白色背景用）
│   │   └── logos/default.png # 默认站点图标
│   └── favicons/             # 【自动生成】网站favicon缓存（MD5命名PNG）
├── cn/                        # 【自动生成】中文页面
│   ├── index.html             # 中文首页
│   ├── about.html             # 关于本站（手动优化文案）
│   ├── privacy.html           # 隐私政策
│   ├── terms.html             # 服务条款
│   ├── contact.html           # 联系我们
│   ├── sitemap.html           # 网站地图
│   ├── articles.html          # 【自动生成】文章列表页
│   ├── article/               # 【自动生成】文章详情页（19个，按文章ID命名）
│   │   ├── 1.html             # 下海推荐
│   │   ├── 2.html             # AI工具
│   │   └── ...
│   └── category/              # 分类详情页（105个，按分类ID命名）
│       ├── 10.html            # AI工具（一级分类）
│       ├── 13.html            # AI写作工具（子分类）
│       └── ...
├── en/                        # 【自动生成】英文页面（结构同cn/）
│   ├── index.html
│   ├── about.html
│   ├── privacy.html
│   ├── terms.html
│   ├── contact.html
│   ├── sitemap.html
│   ├── articles.html          # 英文文章列表页
│   ├── article/               # 英文文章详情页（19个）
│   └── category/              # 105个英文分类详情页
├── data/                      # 【数据文件】
│   └── articles.json          # 文章数据（19篇，中英文双语）
├── tools/                     # 【开发工具】Python脚本
│   ├── generate_new_html.py   # 【核心】生成中英文首页（含深色模式、搜索功能）
│   ├── generate_category_pages.py # 【核心】生成中英文分类详情页（含深色模式）
│   ├── generate_standard_pages.py  # 【核心】生成标准页面（隐私/条款/联系/地图，含深色模式）
│   ├── generate_articles.py   # 【核心】生成文章列表页和详情页（含深色模式）
│   ├── generate_articles_data.py # 生成文章数据（为每个分类生成一篇文章）
│   ├── add_dark_mode_static.py # 给独立页面添加深色模式支持
│   ├── cache_favicons.py      # 【核心】批量下载favicon
│   ├── enrich_descriptions.py # 丰富站点描述（中英文）
│   ├── update_sitemap.py      # 更新sitemap.xml
│   ├── build_data.py          # 合并抓取数据到完整版导航.json
│   ├── category_mapping.yaml  # 分类映射表（抓取层与分类层解耦）
│   ├── category_translation.json # 分类中英文翻译映射
│   ├── check_sites_validity.py # 站点有效性检测
│   ├── remove_invalid_sites.py # 删除无效站点
│   ├── list_categories.py     # 查看分类结构
│   ├── web_admin/             # 【Web管理后台】Flask应用
│   │   ├── app.py             # 主程序（仪表盘/抓取/合并/数据管理）
│   │   ├── crawler_generic.py # 通用抓取脚本
│   │   ├── templates/         # HTML模板（5个页面）
│   │   ├── static/            # 静态资源（CSS/JS）
│   │   └── README.md          # Web管理后台使用说明
│   └── crawler/               # 抓取脚本目录
│       ├── crawler_utils.py   # 通用工具模块
│       ├── crawl_aididai.py   # AI地带抓取脚本
│       ├── crawl_tbox.py      # Tbox导航抓取脚本
│       ├── crawl_tudingai.py  # 图钉AI抓取脚本
│       ├── crawl_aih.py       # AIH超级导航站抓取脚本
│       ├── crawl_zvcard.py    # zvcard导航抓取脚本（WordPress+onenav主题）
│       ├── auto_categorize_zvcard.py # zvcard站点自动分类
│       └── merge_zvcard.py    # zvcard站点合并到主数据
├── index.html                  # 根目录跳转页（自动跳转到/cn/）
├── 404.html                   # 404错误页面
├── redirect.html              # 站点跳转中转页
├── robots.txt                 # 搜索引擎爬虫规则
├── sitemap.xml                # 【自动生成】网站地图（263个URL）
├── 完整版导航.json            # 【核心数据】站点数据（105分类/2591站点）
├── favicon_mapping.json       # 【自动生成】域名→favicon路径映射
├── 启动Web管理后台.bat         # Windows启动脚本（双击打开Web管理后台）
└── README.md                  # 项目说明文档
├── redirect.html              # 外链跳转中转页
├── ads.txt                    # 广告验证文件
├── sitemap.xml                # 【自动生成】网站地图
├── 完整版导航.json             # 【核心数据源】唯一数据源，手动维护
├── favicon_mapping.json       # 【自动生成】域名→本地favicon路径映射
├── README.md                   # 本文件
└── LICENSE
```

## 哪些是生成的？哪些是手动维护的？

### 自动生成的文件（不要手动编辑，会被覆盖）

| 文件/目录 | 生成脚本 | 说明 |
|-----------|---------|------|
| `cn/index.html` | `generate_new_html.py` | 中文首页 |
| `en/index.html` | `generate_new_html.py` | 英文首页 |
| `cn/category/*.html` | `generate_category_pages.py` | 105个中文分类详情页 |
| `en/category/*.html` | `generate_category_pages.py` | 105个英文分类详情页 |
| `cn/privacy.html` | `generate_standard_pages.py` | 隐私政策 |
| `en/privacy.html` | `generate_standard_pages.py` | 隐私政策 |
| `cn/terms.html` | `generate_standard_pages.py` | 服务条款 |
| `en/terms.html` | `generate_standard_pages.py` | 服务条款 |
| `cn/contact.html` | `generate_standard_pages.py` | 联系我们 |
| `en/contact.html` | `generate_standard_pages.py` | 联系我们 |
| `cn/sitemap.html` | `generate_standard_pages.py` | 网站地图 |
| `en/sitemap.html` | `generate_standard_pages.py` | 网站地图 |
| `cn/articles.html` | `generate_articles.py` | 中文文章列表页 |
| `en/articles.html` | `generate_articles.py` | 英文文章列表页 |
| `cn/article/*.html` | `generate_articles.py` | 19个中文文章详情页 |
| `en/article/*.html` | `generate_articles.py` | 19个英文文章详情页 |
| `data/articles.json` | `generate_articles_data.py` | 文章数据（19篇，中英文） |
| `sitemap.xml` | `update_sitemap.py` | 网站地图XML |
| `favicon_mapping.json` | `cache_favicons.py` | favicon映射 |
| `assets/favicons/*.png` | `cache_favicons.py` | favicon图片 |

### 手动维护的文件（核心）

| 文件 | 说明 |
|------|------|
| `完整版导航.json` | **唯一数据源**，所有站点和分类信息都在这里 |
| `cn/about.html` | 关于本站（文案手动优化，不通过脚本生成） |
| `en/about.html` | 关于本站英文版 |
| `assets/` | 静态资源（CSS/JS/图片/logo） |
| `index.html` | 根目录跳转页 |
| `404.html` | 404页面 |
| `redirect.html` | 跳转中转页 |
| `tools/` | 所有Python生成脚本 |

## 核心数据文件说明

### 完整版导航.json

网站的唯一数据源，所有HTML页面都由这个文件生成。结构如下：

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
          "description": "中文站点描述",
          "description_en": "English description",
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
- `description` 是中文描述，`description_en` 是英文描述

## 手动维护指南

### 添加新网站（手动）

1. 编辑 `完整版导航.json`，找到目标分类（按id或name）
2. 在该分类的`sites`数组中添加新站点：
```json
{
  "id": 9999,
  "group_id": 11,
  "name": "新站点名",
  "url": "https://newsite.com",
  "icon": "",
  "description": "中文描述（至少30字）",
  "description_en": "English description",
  "notes": "",
  "order_num": 999,
  "is_public": true,
  "created_at": "2026-09-07",
  "updated_at": "2026-09-07"
}
```
3. 下载favicon：`python tools/cache_favicons.py`
4. 重新生成所有页面：
```bash
python tools/generate_new_html.py
python tools/generate_category_pages.py
python tools/generate_standard_pages.py
python tools/generate_articles.py
python tools/update_sitemap.py
```
5. 本地预览：`python -m http.server 8000`
6. 提交部署：`git add . && git commit -m "添加新站点" && git push`

### 修改网站信息

1. 编辑 `完整版导航.json`，找到目标站点（按id或name）
2. 修改对应字段（name/url/description等）
3. 重新生成所有页面（同上）
4. 提交部署

### 添加新分类

1. 编辑 `完整版导航.json`，在`groups`数组中添加新分类：
```json
{
  "id": 999,
  "name": "新分类名",
  "order_num": 99,
  "parent_id": 10,
  "sites": []
}
```
2. 如果是一级分类，`parent_id` 设为 `null`
3. 在 `tools/category_translation.json` 中添加分类的英文翻译
4. 重新生成所有页面
5. 提交部署

### 删除网站

1. 编辑 `完整版导航.json`，删除目标站点
2. 重新生成所有页面
3. 提交部署

### 文章管理

文章数据存储在 `data/articles.json`，每篇文章包含中英文标题、摘要、内容、标签等字段。

**添加新文章：**
1. 编辑 `data/articles.json`，在`articles`数组中添加新文章：
```json
{
  "id": 100,
  "title": "中文标题",
  "title_en": "English Title",
  "category": "分类名",
  "category_en": "Category Name",
  "author": "Invisible Man",
  "publishDate": "2026-09-08",
  "summary": "中文摘要",
  "summary_en": "English summary",
  "content": "<h2>标题</h2><p>正文内容（支持HTML）</p>",
  "content_en": "<h2>Title</h2><p>Content in English</p>",
  "tags": ["标签1", "标签2"],
  "tags_en": ["Tag1", "Tag2"],
  "views": 0,
  "isPublic": true
}
```
2. 重新生成文章页面：`python tools/generate_articles.py`
3. 更新sitemap：`python tools/update_sitemap.py`
4. 提交部署

**批量生成分类文章：**
- 运行 `python tools/generate_articles_data.py` 可为每个一级分类自动生成一篇文章
- 生成后可手动编辑 `data/articles.json` 优化内容

### Web管理后台

本地Web管理后台提供可视化操作界面，支持抓取、合并、数据管理等功能。

**启动方式：**
- Windows：双击 `启动Web管理后台.bat`
- 或命令行：`python tools/web_admin/app.py`
- 访问地址：http://127.0.0.1:5000

**功能模块：**
1. **仪表盘**：数据统计（站点数、分类数）、分类排行Top10
2. **抓取站点**：通用抓取（输入URL自动抓取）+ 指定脚本抓取（选择已有的抓取脚本）
3. **合并生成**：分类映射、重复检测、一键合并到主数据、重新生成页面
4. **数据管理**：关键词/分类搜索站点、删除站点

**注意：** Web管理后台仅在本地运行，不会部署到线上。生成页面后仍需手动git提交部署。

## 完整操作流程

### 日常维护流程（添加/修改站点后）

```bash
# 1. 编辑完整版导航.json添加或修改网站

# 2. 下载/更新favicon
python tools/cache_favicons.py

# 3. 重新生成所有页面（5个脚本）
python tools/generate_new_html.py       # 中英文首页（含深色模式、搜索功能）
python tools/generate_category_pages.py  # 中英文分类详情页（210个，含深色模式）
python tools/generate_standard_pages.py  # 中英文标准页面（8个，含深色模式）
python tools/generate_articles.py        # 中英文文章页面（40个，含深色模式）
python tools/update_sitemap.py           # sitemap.xml（263个URL）

# 4. 本地预览
python -m http.server 8000
# 访问 http://localhost:8000 （自动跳转到/cn/）

# 5. 提交部署
git add .
git commit -m "更新站点数据"
git push origin master
```

### 抓取新站点的完整流程

```bash
# 1. 编写抓取脚本（复制模板后修改）
cp tools/crawler/_template.py tools/crawler/crawl_新站.py

# 2. 运行抓取脚本
python tools/crawler/crawl_新站.py

# 3. 在category_mapping.yaml中添加分类映射
# 编辑 tools/category_mapping.yaml，追加映射规则

# 4. 合并数据到完整版导航.json
python tools/build_data.py

# 5. 下载新站点的favicon
python tools/cache_favicons.py

# 6. 丰富站点描述（可选）
python tools/enrich_descriptions.py

# 7. 重新生成所有页面
python tools/generate_new_html.py
python tools/generate_category_pages.py
python tools/generate_standard_pages.py
python tools/update_sitemap.py

# 8. 本地预览验证
python -m http.server 8000

# 9. 提交部署
git add .
git commit -m "添加从XX站抓取的新站点"
git push origin master
```

### 清理无效站点流程

```bash
# 1. 检测站点有效性
python tools/check_sites_validity.py
# 生成检测报告

# 2. 查看检测报告，人工确认要删除的站点
# （注意：国外站点超时可能是国内网络问题，不一定是真失效）

# 3. 删除无效站点
python tools/remove_invalid_sites.py

# 4. 重新生成所有页面
python tools/generate_new_html.py
python tools/generate_category_pages.py
python tools/generate_standard_pages.py
python tools/generate_articles.py
python tools/update_sitemap.py

# 5. 提交部署
git add .
git commit -m "清理无效站点"
git push origin master
```

## 搭建相同站点（从0开始）

### 前置条件

- Python 3.8+
- Git
- GitHub账号
- Cloudflare账号

### 步骤1：获取代码

```bash
# 克隆本仓库
git clone https://github.com/bingehack/009tg.com.git
cd 009tg.com

# 或Fork后克隆自己的仓库
git clone https://github.com/你的用户名/009tg.com.git
```

### 步骤2：安装Python依赖

```bash
pip install requests beautifulsoup4 pyyaml pillow
```

### 步骤3：准备数据

有两种方式：

**方式A：使用现有数据（推荐起步）**
- 直接使用仓库中的 `完整版导航.json`（2447个站点）
- 后续按需增删修改

**方式B：从零开始**
1. 创建空的 `完整版导航.json`：
```json
{
  "groups": [],
  "version": "1.0",
  "exportDate": "2026-09-07"
}
```
2. 手动添加分类和站点，或通过抓取脚本自动添加

### 步骤4：下载favicon

```bash
python tools/cache_favicons.py
```
- 会自动下载所有站点的favicon到 `assets/favicons/`
- 下载失败的站点会使用默认图标 `assets/images/logos/default.png`
- 生成 `favicon_mapping.json` 映射文件

### 步骤5：生成所有页面

```bash
python tools/generate_new_html.py       # 中英文首页
python tools/generate_category_pages.py  # 中英文分类详情页
python tools/generate_standard_pages.py  # 中英文标准页面
python tools/update_sitemap.py           # sitemap.xml
```

### 步骤6：本地预览

```bash
python -m http.server 8000
```
访问：
- 中文版：http://localhost:8000/cn/
- 英文版：http://localhost:8000/en/
- 根目录：http://localhost:8000 （自动跳转到/cn/）

### 步骤7：部署到Cloudflare Pages

1. 推送代码到GitHub：
```bash
git add .
git commit -m "Initial commit"
git push -u origin master
```

2. 在Cloudflare Pages中连接仓库：
   - 登录 Cloudflare Dashboard → Workers & Pages → Create a project
   - Connect to Git → 选择GitHub → 选择你的仓库
   - Framework preset: None
   - Build command: 留空（纯静态）
   - Build output directory: `/`（根目录）
   - 点击 Save and Deploy

3. 配置自定义域名（可选）：
   - Pages项目 → Custom domains → Set up a custom domain
   - 输入你的域名，Cloudflare自动配置DNS

4. 自动部署：
   - 每次push到master分支，Cloudflare自动重新部署（1-2分钟）

### 步骤8：自定义修改

- **修改站点名称/Logo**：编辑 `assets/images/` 下的logo文件
- **修改配色**：编辑 `assets/css/` 下的样式文件
- **修改关于页面**：编辑 `cn/about.html` 和 `en/about.html`
- **修改联系方式/邮箱**：编辑 `tools/generate_standard_pages.py` 中的邮箱，然后重新生成
- **添加广告代码**：编辑生成脚本中的AdSense代码，然后重新生成

## 工具脚本说明

### 核心脚本（日常使用）

| 脚本 | 功能 | 用法 |
|---|---|---|
| `generate_new_html.py` | 生成中英文首页 | `python tools/generate_new_html.py` |
| `generate_category_pages.py` | 生成中英文分类详情页（210个） | `python tools/generate_category_pages.py` |
| `generate_standard_pages.py` | 生成中英文标准页面（8个） | `python tools/generate_standard_pages.py` |
| `cache_favicons.py` | 批量下载favicon | `python tools/cache_favicons.py` |
| `enrich_descriptions.py` | 丰富站点描述（中英文） | `python tools/enrich_descriptions.py` |
| `update_sitemap.py` | 更新sitemap.xml | `python tools/update_sitemap.py` |
| `build_data.py` | 合并抓取数据到完整版导航.json | `python tools/build_data.py` |
| `check_sites_validity.py` | 检测站点有效性 | `python tools/check_sites_validity.py` |
| `remove_invalid_sites.py` | 删除无效站点 | `python tools/remove_invalid_sites.py` |

### 辅助脚本

| 脚本 | 功能 |
|---|---|
| `list_categories.py` | 查看分类结构（一级/二级/站点数） |
| `cleanup_json.py` | JSON清理（删除冗余字段） |
| `verify_cleanup.py` | 数据完整性验证 |
| `check_all_favicons.py` | 检查favicon文件有效性 |
| `fix_favicon_urls.py` | 修复favicon URL格式 |

### 抓取脚本（tools/crawler/）

| 脚本 | 目标站 | 站点类型 | 新增站点 |
|---|---|---|---|
| `crawl_aididai.py` | AI地带 (aididai.cn) | 服务端渲染 | 605 |
| `crawl_tbox.py` | Tbox导航 (tboxn.com) | 服务端渲染 | 197 |
| `crawl_tudingai.py` | 图钉AI (tudingai.com) | 服务端渲染 | 183 |
| `crawl_aih.py` | AIH超级导航站 (aimomap.cn) | 纯JS渲染 | 317 |

## 部署到 Cloudflare Pages

### 部署配置

- **Framework preset**：None
- **Build command**：留空（纯静态网站，无需构建）
- **Build output directory**：`/`（根目录）
- **分支**：`master`

### 自动部署

每次推送代码到GitHub的 `master` 分支，Cloudflare会自动重新部署，通常1-2分钟内完成。

### 部署注意事项

1. **大文件**：favicon目录有上千个PNG文件，首次推送可能较慢
2. **404页面**：项目已包含404.html，Cloudflare Pages会自动使用
3. **缓存**：Cloudflare会缓存静态资源，更新后可能需要强制刷新（Ctrl+F5）
4. **.gitignore**：确保不要提交临时文件（分析脚本、临时HTML等）

## 本地预览

```bash
cd 009tg.com
python -m http.server 8000
```

访问：
- 中文版：http://localhost:8000/cn/
- 英文版：http://localhost:8000/en/
- 根目录：http://localhost:8000 （自动跳转到/cn/）

## 常见问题

### Q: 如何添加新网站？

A: 有两种方式：
1. **手动添加**：编辑 `完整版导航.json`，按照现有格式添加站点信息，然后运行4个生成脚本重新生成HTML
2. **自动抓取**：编写抓取脚本从同类导航站批量抓取，参考"抓取新站点的完整流程"

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

### Q: 修改了完整版导航.json后需要运行哪些脚本？

A: 需要运行4个脚本重新生成所有页面：
```bash
python tools/generate_new_html.py       # 中英文首页
python tools/generate_category_pages.py  # 中英文分类详情页
python tools/generate_standard_pages.py  # 中英文标准页面
python tools/update_sitemap.py           # sitemap.xml
```

### Q: 如何回滚数据？

A: build_data.py每次运行前会自动备份为 `完整版导航.json.build_backup`。如需回滚：
```bash
cp 完整版导航.json.build_backup 完整版导航.json
# 然后重新生成所有页面
```

### Q: 分类详情页的URL是什么格式？

A: 使用分类ID命名：`/cn/category/{id}.html` 和 `/en/category/{id}.html`
- 例如AI工具（id=10）：`/cn/category/10.html`
- 例如AI写作工具（id=13）：`/cn/category/13.html`

### Q: 一级分类和子分类的详情页有什么区别？

A:
- **一级分类**：显示子分类入口列表，不显示具体站点（如果没有直接站点）
- **子分类**：显示该分类下的所有站点，支持分页浏览（每页32个）

## 技术栈

- **前端框架**：Bootstrap 3.x + Xenon
- **图标库**：Font Awesome, Linecons
- **JavaScript**：jQuery, TweenMax
- **开发工具**：Python 3.x
- **依赖库**：requests, beautifulsoup4, pyyaml, pillow
- **部署平台**：Cloudflare Pages（纯静态，Git自动部署）

## 定期维护任务

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
   python tools/generate_category_pages.py
   python tools/generate_standard_pages.py
   python tools/update_sitemap.py
   ```

5. **抓取新站点**（按需）
   ```bash
   python tools/crawler/crawl_新站.py
   python tools/build_data.py
   python tools/cache_favicons.py
   python tools/generate_new_html.py
   python tools/generate_category_pages.py
   python tools/generate_standard_pages.py
   python tools/update_sitemap.py
   ```

## 授权说明

### 基础版本（免费）

本站基础版本（原始导航框架）采用 **MIT License** 开源协议，可免费使用和二次开发。

### 增强版本（商业授权）

后续所有功能增强与定制开发均为**商业授权版本，不公开源码**，包括但不限于：

- 中英文双语支持
- 分类详情页系统（210个页面）
- 自动化抓取框架（4个源站抓取脚本）
- 站点描述自动丰富（中英文）
- favicon本地缓存系统
- 站点有效性自动检测
- 标准页面生成（隐私/条款/联系/地图）
- sitemap自动更新

如需部署、定制或获取完整源码，请通过邮件联系：**invisibleman009tg@proton.me**，具体授权费用另行沟通。

## 联系方式

- 网站：https://009tg.com
- 作者：Invisible Man
- 邮箱：invisibleman009tg@proton.me

---

如果这个项目对你有帮助，请给个Star支持一下！
