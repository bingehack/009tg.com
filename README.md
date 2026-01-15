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
WebStackPage.github.io/
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
│   ├── final_fix.py    # HTML生成脚本
│   ├── cache_favicons.py  # Favicon缓存脚本
│   ├── check_sites_validity.py  # 站点有效性检测
│   ├── fix_bugs.py     # Bug修复脚本
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
cd WebStackPage.github.io
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
python tools/final_fix.py
```

## 工具脚本使用

项目提供了多个工具脚本用于网站维护，详细说明请查看 [tools/README.md](tools/README.md)。

### 常用命令

```bash
# 检测站点有效性
python tools/check_sites_validity.py

# 删除无效站点
python tools/remove_invalid_sites.py

# 更新favicon缓存
python tools/cache_favicons.py

# 重新生成HTML
python tools/final_fix.py

# 修复已知bug
python tools/fix_bugs.py
```

## 部署到Cloudflare Pages

### 前置条件

1. **GitHub账号**：确保你有GitHub账号
2. **代码仓库**：将本项目代码推送到GitHub仓库
3. **Cloudflare账号**：确保你有Cloudflare账号

### 部署步骤

#### 步骤1：创建GitHub仓库

1. 访问 [GitHub](https://github.com/new) 创建新仓库
2. 仓库名称：`WebStackPage.github.io` 或 `009tg.com`
3. 设置为Public公开仓库
4. 点击"Create repository"创建仓库

#### 步骤2：推送代码到GitHub

```bash
# 初始化Git仓库（如果还没有）
cd WebStackPage.github.io
git init
git add .
git commit -m "Initial commit"

# 配置远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/你的GitHub用户名/WebStackPage.github.io.git

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
   python tools/final_fix.py
   ```

### 数据更新流程

1. 编辑 `完整版导航.json` 添加或修改网站
2. 运行 `check_sites_validity.py` 验证新站点
3. 运行 `cache_favicons.py` 下载favicon
4. 运行 `final_fix.py` 重新生成HTML
5. 提交代码到GitHub触发自动部署

## 常见问题

### Q: 如何添加新网站？

A: 编辑 `完整版导航.json` 文件，按照现有格式添加网站信息，然后运行 `python tools/final_fix.py` 重新生成HTML。

### Q: 网站图标不显示怎么办？

A: 运行 `python tools/cache_favicons.py` 重新下载favicon，或者手动将图标文件放到 `assets/favicons/` 目录。

### Q: 如何检测无效链接？

A: 运行 `python tools/check_sites_validity.py`，脚本会检测所有站点并生成报告。

### Q: 英文版本如何更新？

A: 运行 `python tools/final_fix.py` 会同时生成中文和英文版本的HTML文件。

## License

本项目采用 MIT License 开源协议。

> 本项目开源的目的是让大家能够在本站的基础之上有所启发，做出更多新的东西。如果你使用这个开源项目，请**注明**本项目开源地址。

## 联系方式

- 网站：https://009tg.com
- 作者：Invisible Man

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
