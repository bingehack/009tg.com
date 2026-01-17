# 009tg下海导航

一个专注于创业、副业、投资、跨境电商等领域的网址导航网站。

## 项目简介

009tg下海导航致力于打造国内最好的互联网上优质网站网址大全，收录了全网好用强大的网站网址和软件，包括创业、副业、投资、跨境电商、营销工具、AI工具、社交媒体、独立站、广告投放、生活、休闲、办公、工具、资源等超全面的网址和职业技巧内容，让您的上网体验更便捷更放心。

## 项目特性

- 🎯 精选优质网站，覆盖创业、副业、投资、跨境电商等多个领域
- 📱 响应式设计，支持桌面端和移动端访问
- 🌍 多语言支持（中文、英文）
- 🚀 基于Bootstrap前端框架，轻量高效
- 📦 纯静态网站，部署简单快速
- 🔍 站点有效性检测，确保链接可用
- 🎨 本地favicon缓存，提升加载速度

## 项目结构

```
009tg.com/
├── assets/              # 静态资源文件
│   ├── css/            # 样式文件
│   ├── js/             # JavaScript文件
│   ├── images/         # 图片资源
│   └── favicons/      # 网站图标缓存
├── cn/                 # 中文版本
│   ├── index.html      # 中文首页
│   └── about.html     # 关于页面
├── en/                 # 英文版本
│   ├── index.html      # 英文首页
│   └── about.html     # 关于页面
├── tools/              # 开发工具脚本
│   ├── README.md       # 工具说明文档
│   ├── generate_new_html.py  # HTML生成脚本
│   ├── cache_favicons.py  # Favicon缓存脚本
│   ├── check_sites_validity.py  # 站点有效性检测
│   ├── add_default_src.py  # 为Google favicon服务添加默认src属性
│   ├── fix_javascript_escape.py  # 修复JavaScript模板变量转义
│   ├── fix_javascript_img.py  # 修复动态生成的img标签
│   └── ...           # 其他工具脚本
├── index.html          # 根目录首页（中文）
├── 404.html           # 404错误页面
├── README.md           # 项目说明文档
├── 完整版导航.json     # 网站数据源
└── favicon_mapping.json # Favicon映射文件
```

## 快速开始

### 本地运行

```bash
# 使用Python内置服务器
cd 009tg.com
python -m http.server 8000

# 访问
# 中文版：http://localhost:8000
# 英文版：http://localhost:8000/en/
```

### 添加新网站

1. 编辑 `完整版导航.json` 文件
2. 运行工具脚本更新网站：

```bash
# 1. 检测新添加的站点是否有效
python tools/check_sites_validity.py

# 2. 下载新站点的favicon
python tools/cache_favicons.py

# 3. 重新生成HTML文件
python tools/generate_new_html.py
```

## 工具脚本使用

项目提供了多个工具脚本用于网站维护，所有脚本都包含详细的使用说明。

### 核心工具脚本

#### 1. HTML生成脚本

**[generate_new_html.py](tools/generate_new_html.py)** - 生成新的导航网站HTML文件

```bash
python tools/generate_new_html.py
```

功能：
- 读取JSON数据生成完整的HTML结构
- 支持多级分类导航菜单
- 生成内容区域（支持翻页功能）
- 使用本地缓存的favicon
- 自动备份现有的index.html文件

#### 2. Favicon缓存脚本

**[cache_favicons.py](tools/cache_favicons.py)** - 批量下载并缓存网站图标

```bash
python tools/cache_favicons.py
```

功能：
- 从JSON数据中提取所有网站URL
- 使用多个favicon源（Google、Yandex、Statvoo、FaviconExtractor）尝试下载
- 使用MD5哈希生成唯一的文件名
- 生成域名到图标的映射关系文件
- 支持断点续传（已存在的文件跳过下载）

#### 3. 站点有效性检测脚本

**[check_sites_validity.py](tools/check_sites_validity.py)** - 检测网站链接是否有效

```bash
# 基本检测（不删除数据）
python tools/check_sites_validity.py

# 检测并删除无效站点
python tools/check_sites_validity.py --delete

# 自定义超时时间（默认10秒）
python tools/check_sites_validity.py --timeout 15

# 指定JSON文件路径
python tools/check_sites_validity.py --file 完整版导航.json
```

功能：
- 批量检测网站列表中的站点是否可以正常访问
- 对每个URL进行HTTP访问测试（支持超时设置）
- 识别无法访问的站点（超时、连接错误、HTTP错误等）
- 生成检测报告，列出所有无效站点
- 支持将无效站点从JSON数据中安全删除

#### 4. 删除无效站点脚本

**[remove_invalid_sites.py](tools/remove_invalid_sites.py)** - 从JSON数据中删除无效站点

```bash
python tools/remove_invalid_sites.py
```

功能：
- 从HTML报告中提取无效URL
- 自动备份原始JSON文件
- 从JSON数据中删除无效站点
- 自动重新生成HTML文件

注意：需要先运行 check_sites_validity.py 生成 connection_failed_sites.html 报告

#### 5. 检查所有favicon脚本

**[check_all_favicons.py](tools/check_all_favicons.py)** - 扫描并检查所有favicon文件的有效性

```bash
python tools/check_all_favicons.py
```

功能：
- 扫描assets/favicons目录
- 检查所有PNG文件的有效性
- 删除无效的PNG文件

### HTML修复工具脚本

#### 6. 修复favicon URL格式

**[fix_favicon_urls.py](tools/fix_favicon_urls.py)** - 修复JSON数据文件中的favicon URL格式

```bash
python tools/fix_favicon_urls.py
```

功能：
- 将错误的URL格式`https://www.faviconextractor.com/favicon/{domain}?larger=true`
- 修复为正确的格式`https://www.faviconextractor.com/api/favicon/{domain}`

#### 7. 添加默认src属性

**[add_default_src.py](tools/add_default_src.py)** - 为使用Google favicon服务的图片添加默认src属性

```bash
python tools/add_default_src.py
```

功能：
- 修复Google favicon服务超时导致的图标显示问题
- 为懒加载图片提供fallback
- 支持多个HTML文件（index.html, cn/index.html, en/index.html）

#### 8. 修复JavaScript转义变量

**[fix_javascript_escape.py](tools/fix_javascript_escape.py)** - 修复动态生成的img标签中的转义变量问题

```bash
python tools/fix_javascript_escape.py
```

功能：
- 移除错误的反斜杠转义
- 支持多个HTML文件（index.html, cn/index.html, en/index.html）

#### 9. 修复JavaScript动态生成的img标签

**[fix_javascript_img.py](tools/fix_javascript_img.py)** - 为JavaScript动态生成的img标签添加src属性

```bash
python tools/fix_javascript_img.py
```

功能：
- 为懒加载图片添加src属性
- 支持多个HTML文件（index.html, cn/index.html, en/index.html）

### 测试脚本

test_scripts目录包含一些测试和临时脚本，用于开发和调试：

- **[check_sites.py](tools/test_scripts/check_sites.py)** - 检查特定站点
- **[check_png.py](tools/test_scripts/check_png.py)** - 检查PNG文件头
- **[check_png_file.py](tools/test_scripts/check_png_file.py)** - 检查PNG文件有效性
- **[fix_url_format.py](tools/test_scripts/fix_url_format.py)** - 修复JSON数据文件中的URL格式
- **[fix_html.py](tools/test_scripts/fix_html.py)** - 修复HTML文件中的资源引用路径和标题信息
- **[fix_issues.py](tools/test_scripts/fix_issues.py)** - 修复导航网站中的各种问题
- **[simple_generate.py](tools/test_scripts/simple_generate.py)** - 生成简单版本的HTML导航文件
- **[keep_style_generate.py](tools/test_scripts/keep_style_generate.py)** - 保持原有风格生成新的导航网站
- **[convert_json_to_html.py](tools/test_scripts/convert_json_to_html.py)** - 将JSON格式的导航数据转换为HTML页面
- **[fix_all_html.py](tools/test_scripts/fix_all_html.py)** - 为所有HTML文件中的懒加载图片添加src属性
- **[fix_lazy_loading.py](tools/test_scripts/fix_lazy_loading.py)** - 为HTML文件中的懒加载图片添加src属性
- **[fix_bugs.py](tools/test_scripts/fix_bugs.py)** - 修复3个bug（关于本站链接、favicon路径、语言切换器）
- **[generate_nested_nav.py](tools/test_scripts/generate_nested_nav.py)** - 生成带有嵌套导航菜单的HTML文件
- **[generate_english.py](tools/test_scripts/generate_english.py)** - 将中文版HTML文件翻译为英文版本

### 常用命令

```bash
# 检测站点有效性
python tools/check_sites_validity.py

# 删除无效站点
python tools/remove_invalid_sites.py

# 更新favicon缓存
python tools/cache_favicons.py

# 重新生成HTML
python tools/generate_new_html.py

# 修复已知问题
python tools/add_default_src.py
python tools/fix_javascript_escape.py
python tools/fix_javascript_img.py
```

## 部署到Cloudflare Pages

### 前置条件

1. **GitHub账号**：确保你有GitHub账号
2. **代码仓库**：将本项目代码推送到GitHub仓库
3. **Cloudflare账号**：确保你有Cloudflare账号

### 部署步骤

#### 步骤1：创建GitHub仓库

1. 访问 [GitHub](https://github.com/new) 创建新仓库
2. 仓库名称：`009tg.com`
3. 设置为Public公开仓库
4. 点击"Create repository"创建仓库

#### 步骤2：推送代码到GitHub

```bash
# 初始化Git仓库（如果还没有）
cd 009tg.com
git init
git add .
git commit -m "Initial commit"

# 配置远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/你的GitHub用户名/009tg.com.git

# 推送到GitHub
git push -u origin master
```

#### 步骤3：在Cloudflare Pages中连接仓库

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 **Workers & Pages** → **Create a project**
3. 点击 **Connect to Git**
4. 选择 **GitHub**，授权Cloudflare访问你的GitHub账号
5. 选择你创建的仓库
6. 点击 **Begin setup** 开始部署

#### 步骤4：配置自定义域名

1. 在Cloudflare Pages项目中，点击 **Custom domains**
2. 添加你的自定义域名，例如：`009tg.com`
3. 按照提示配置DNS记录：
   - 添加CNAME记录指向你的Pages域名
   - 或使用Cloudflare提供的Nameservers

4. 等待SSL证书自动生成（通常需要几分钟）

#### 步骤5：验证部署

1. 访问你的自定义域名：`https://009tg.com`
2. 确认网站正常访问
3. 每次推送代码到GitHub，Cloudflare会自动重新部署

### 自动部署

Cloudflare Pages支持自动部署，当你推送代码到GitHub时：

- Cloudflare会自动检测到新的提交
- 自动构建和部署网站
- 通常在1-2分钟内完成部署
- 可以在Cloudflare Dashboard查看部署日志

## 技术栈

- **前端框架**：Bootstrap 3.x
- **样式框架**：Xenon
- **图标库**：Font Awesome, Linecons
- **JavaScript**：jQuery, TweenMax, Lozad (懒加载)
- **开发工具**：Python 3.x

## 维护指南

### 定期维护任务

1. **站点有效性检测**（每周）
   ```bash
   python tools/check_sites_validity.py
   ```

2. **删除无效站点**（根据检测结果）
   ```bash
   python tools/remove_invalid_sites.py
   ```

3. **更新favicon缓存**（每月）
   ```bash
   python tools/cache_favicons.py
   ```

4. **重新生成HTML**（数据更新后）
   ```bash
   python tools/generate_new_html.py
   ```

### 数据更新流程

1. 编辑 `完整版导航.json` 添加或修改网站
2. 运行 `check_sites_validity.py` 验证新站点
3. 运行 `cache_favicons.py` 下载favicon
4. 运行 `generate_new_html.py` 重新生成HTML
5. 提交代码到GitHub触发自动部署

## 最新修复

### 2026-01-17

- **添加Google AdSense代码**：在所有网页的`<head>`标签之间添加了AdSense代码，包括index.html、cn/index.html、en/index.html、redirect.html等所有HTML文件
- **更新HTML生成脚本**：修改generate_new_html.py，确保新生成的HTML文件自动包含AdSense代码
- **修复英文版内容问题**：发现英文版index.html包含中文内容，运行generate_english.py脚本生成正确的英文版本
- **修复英文版图标路径**：更新generate_english.py脚本，修复JavaScript数据中的图标路径（从"assets/favicons/"改为"../assets/favicons/"）
- **修复cn/index.html图标路径**：创建fix_cn_paths.py脚本，修复cn/index.html中的资源路径和JavaScript图标路径
- **修复redirect.html链接**：修复cn/index.html和en/index.html中的redirect.html链接路径，确保正确跳转到根目录的redirect.html页面
- **优化多语言版本路径管理**：统一处理根目录、cn/、en/三个版本的资源路径，确保图标和链接正常工作
- **优化所有Python脚本的使用说明**：为所有工具脚本添加了详细的使用说明文档，包括用途、功能概述、使用方法和主要特性
- **更新README.md文档**：完善了工具脚本使用说明，添加了核心工具脚本、HTML修复工具脚本和测试脚本的详细说明
- **添加脚本文档注释**：所有Python脚本都包含了标准化的文档注释，便于理解和使用

### 2026-01-16

- **修复faviconextractor.com API格式错误**：将错误的URL格式`https://www.faviconextractor.com/favicon/{domain}?larger=true`修复为正确的`https://www.faviconextractor.com/api/favicon/{domain}`
- **修复JSON数据中的URL格式**：将包含路径的URL（如`https://echodata.work/home.html`）修复为只包含域名的格式（如`https://echodata.work`）
- **修复Google favicon服务超时问题**：为使用Google favicon服务的图片添加默认src属性，避免显示小地球图标
- **修复JavaScript模板变量转义**：修复动态生成的img标签中的转义变量问题
- **修复不分页分类的显示问题**：JavaScript代码现在会跳过`data-pagination="False"`的分类，保留静态HTML内容
- **优化HTML生成脚本**：使用本地favicon文件而不是在线服务，提升加载速度
- **成功缓存1164个favicon**：使用修复后的API格式成功下载了所有网站的favicon图标

## 常见问题

### Q: 如何添加新网站？

A: 编辑 `完整版导航.json` 文件，按照现有格式添加网站信息，然后运行 `python tools/generate_new_html.py` 重新生成HTML。

### Q: 网站图标不显示怎么办？

A: 运行 `python tools/cache_favicons.py` 重新下载favicon，或者手动将图标文件放到 `assets/favicons/` 目录。

### Q: 如何检测无效链接？

A: 运行 `python tools/check_sites_validity.py`，脚本会检测所有站点并生成报告。

### Q: 英文版本如何更新？

A: 运行 `python tools/generate_new_html.py` 会生成中文版本的HTML文件。英文版本需要单独维护。

## License

本项目采用 MIT License 开源协议。

> 本项目开源的目的是让大家能够在本站的基础之上有所启发，做出更多新的东西。如果你使用这个开源项目，请**注明**本项目开源地址。

## 联系方式

- 网站：https://009tg.com
- 作者：Invisible Man

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
