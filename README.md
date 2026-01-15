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

## 部署到Cloudflare Pages

### 前置条件

1. **GitHub账号**：确保你有GitHub账号
2. **代码仓库**：将本项目代码推送到GitHub仓库
3. **Cloudflare账号**：确保你有Cloudflare账号

### 部署步骤

#### 步骤1：创建GitHub仓库

1. 访问 [GitHub](https://github.com/new) 创建新仓库
2. 仓库名称：`009tg.github.io`（推荐，用于Cloudflare Pages）
3. 设置为Public公开仓库
4. 点击"Create repository"创建仓库

#### 步骤2：推送代码到GitHub

```bash
# 如果还没有初始化Git仓库
cd "d:\测试文档\url\000\WebStackPage.github.io"
git init
git add .
git commit -m "Initial commit"

# 配置远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/你的GitHub用户名/009tg.github.io.git

# 推送到GitHub
git push -u origin master
```

#### 步骤3：在Cloudflare Pages中连接仓库

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 **Workers & Pages** → **Create a project**
3. 点击 **Connect to Git**
4. 选择 **GitHub**，授权Cloudflare访问你的GitHub账号
5. 选择你创建的 `009tg.github.io` 仓库
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
- **JavaScript**：jQuery, TweenMax

## 本地运行

```bash
# 使用Python内置服务器
cd "d:\测试文档\url\000\WebStackPage.github.io"
python -m http.server 8000

# 或使用其他静态服务器
# npx http-server
# php -S localhost:8000
```

然后访问：http://localhost:8000

## License

本项目采用 MIT License 开源协议。

> 本项目开源的目的是让大家能够在本站的基础之上有所启发，做出更多新的东西。如果你使用这个开源项目，请**注明**本项目开源地址。

## 联系方式

- 网站：https://009tg.com
- 作者：Invisible Man

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
