# Tools 脚本说明文档

本目录包含了用于网站开发和维护的各种Python脚本工具。

## 脚本列表

### 1. check_sites_validity.py - 站点有效性检测脚本

**用途：**
批量检测网站列表中的站点是否可以正常访问，识别并标记无效站点。

**功能概述：**
- 从JSON数据文件中读取所有网站URL
- 对每个URL进行HTTP访问测试（支持超时设置）
- 识别无法访问的站点（超时、连接错误、HTTP错误等）
- 生成检测报告，列出所有无效站点
- 支持将无效站点从JSON数据中安全删除
- 支持代理配置
- 集成第三方API验证

**使用方法：**
```bash
# 基本检测（不删除数据）
python check_sites_validity.py

# 检测并删除无效站点
python check_sites_validity.py --delete

# 自定义超时时间（默认10秒）
python check_sites_validity.py --timeout 15

# 指定JSON文件路径
python check_sites_validity.py --file 完整版导航.json

# 使用代理
python check_sites_validity.py --proxy http://127.0.0.1:7890
```

**主要特性：**
- 支持并发检测，提高检测效率
- 支持多种请求方法（HEAD/GET）
- 支持SSL验证控制
- 详细的错误日志记录
- 生成HTML格式的检测报告
- 支持备份原始数据
- 安全的删除机制，避免误删
- 集成第三方API验证（downforeveryoneorjustme.com）

---

### 2. final_fix.py - HTML生成脚本

**用途：**
从JSON数据生成HTML导航页面，支持多语言和favicon缓存。

**功能概述：**
- 读取JSON格式的导航数据
- 构建分类树结构
- 生成导航菜单HTML
- 生成内容区域HTML（包含分页功能）
- 支持加载本地缓存的favicon
- 生成中文、英文版本HTML

**使用方法：**
```bash
python final_fix.py
```

**主要特性：**
- 支持响应式布局和分页功能
- 优先使用本地缓存的favicon
- 自动生成多语言版本
- 支持自定义主题和样式

---

### 3. cache_favicons.py - Favicon缓存脚本

**用途：**
批量下载并缓存网站的favicon图标到本地。

**功能概述：**
- 从JSON数据中提取所有网站URL
- 使用多个favicon源（Google、Yandex、Statvoo、FaviconExtractor）尝试下载
- 使用MD5哈希生成唯一的文件名
- 生成域名到图标的映射关系文件
- 支持断点续传（已存在的文件跳过下载）

**使用方法：**
```bash
python cache_favicons.py
```

**主要特性：**
- 支持多个favicon源，提高成功率
- 自动重试机制
- 生成映射文件便于HTML生成脚本使用
- 支持自定义超时时间
- 详细的下载日志记录

---

### 4. remove_invalid_sites.py - 删除无效站点脚本

**用途：**
从JSON数据中删除无效站点，并重新生成HTML文件。

**功能概述：**
- 从HTML报告中提取无效URL
- 自动备份原始JSON文件
- 从JSON数据中删除无效站点
- 自动重新生成HTML文件

**使用方法：**
```bash
python remove_invalid_sites.py
```

**主要特性：**
- 自动备份原始数据
- 支持从HTML报告提取URL
- 自动重新生成HTML
- 详细的删除日志

---

### 5. fix_bugs.py - Bug修复脚本

**用途：**
修复导航网站中的已知bug。

**功能概述：**
- 修复关于本站链接问题
- 修复英文版本favicon路径问题
- 修复英文版本语言切换器问题
- 自动修复所有HTML文件

**使用方法：**
```bash
python fix_bugs.py
```

**主要特性：**
- 自动修复多个已知bug
- 支持中文、英文版本
- 保持HTML结构不变

---

### 6. generate_english.py - 英文版生成脚本

**用途：**
将中文版HTML文件翻译为英文版本。

**功能概述：**
- 读取中文版HTML文件
- 使用预定义的翻译映射表替换中文内容
- 修改HTML语言属性为en
- 修复资源路径（en目录下的相对路径）
- 更新语言切换菜单

**使用方法：**
```bash
python generate_english.py
```

**主要特性：**
- 支持完整的分类名称翻译
- 自动修复资源路径
- 更新语言切换菜单状态
- 保持HTML结构和样式不变

---

### 7. cleanup_old_data.py - 旧数据清理脚本

**用途：**
清除HTML文件中的旧数据，重新生成干净的HTML文件。

**功能概述：**
- 读取JSON格式的导航数据
- 构建分类树结构
- 生成全新的HTML文件（不包含任何旧数据）
- 保存到index.html

**使用方法：**
```bash
python cleanup_old_data.py
```

**主要特性：**
- 完全重新生成HTML，确保无旧数据残留
- 保持JSON数据结构不变
- 生成干净的HTML文件

---

### 8. fix_issues.py - 问题修复脚本

**用途：**
修复导航网站中的各种问题。

**功能概述：**
- 读取JSON数据
- 构建分类树结构
- 读取原有HTML模板
- 生成新的导航菜单（只包含JSON中的数据）
- 修复HTML中的各种问题

**使用方法：**
```bash
python fix_issues.py
```

**主要特性：**
- 支持多种问题修复
- 保持HTML模板结构
- 只更新导航菜单部分

---

### 9. generate_nested_nav.py - 嵌套导航生成脚本

**用途：**
生成带有嵌套导航菜单的HTML文件。

**功能概述：**
- 读取JSON数据
- 构建分类树结构
- 读取原有HTML模板
- 生成新的嵌套导航菜单
- 替换HTML中的导航菜单部分

**使用方法：**
```bash
python generate_nested_nav.py
```

**主要特性：**
- 支持多级嵌套导航
- 保持HTML模板结构
- 只更新导航菜单部分

---

### 10. fix_html.py - HTML修复脚本

**用途：**
修复HTML文件中的资源引用路径和标题信息。

**功能概述：**
- 读取HTML文件
- 修复资源引用路径（去除../前缀）
- 更新网站标题和描述
- 保存修复后的HTML文件

**使用方法：**
```bash
python fix_html.py
```

**主要特性：**
- 自动修复资源路径
- 批量替换标题和描述
- 保持HTML结构不变

---

### 11. keep_style_generate.py - 风格保持生成脚本

**用途：**
保持原有风格生成新的导航网站。

**功能概述：**
- 读取JSON数据
- 读取原有HTML模板
- 生成新的导航菜单
- 生成新的内容区域
- 替换HTML中的对应部分

**使用方法：**
```bash
python keep_style_generate.py
```

**主要特性：**
- 保持原有HTML模板风格
- 只更新导航和内容部分
- 保持样式和布局不变

---

### 12. simple_generate.py - 简单HTML生成脚本

**用途：**
生成简单版本的HTML导航文件。

**功能概述：**
- 读取JSON数据
- 创建简单的HTML模板
- 生成导航菜单和内容区域
- 保存为HTML文件

**使用方法：**
```bash
python simple_generate.py
```

**主要特性：**
- 生成简洁的HTML结构
- 不依赖复杂的模板
- 适合快速测试和预览

---

### 13. generate_new_html.py - 新HTML生成脚本

**用途：**
生成新的导航网站HTML文件。

**功能概述：**
- 读取JSON数据
- 生成导航菜单
- 生成内容区域
- 保存为HTML文件

**使用方法：**
```bash
python generate_new_html.py
```

**主要特性：**
- 生成完整的HTML结构
- 支持自定义导航菜单
- 生成内容区域

---

### 14. convert_json_to_html.py - JSON转HTML脚本

**用途：**
将JSON格式的导航数据转换为HTML页面。

**功能概述：**
- 读取JSON数据
- 读取HTML模板
- 生成导航菜单
- 生成内容区域
- 替换HTML模板中的占位符

**使用方法：**
```bash
python convert_json_to_html.py
```

**主要特性：**
- 支持完整的JSON数据转换
- 保持HTML模板结构
- 生成导航和内容区域

---

### 15. test_sites.py - 站点测试脚本

**用途：**
测试站点访问情况。

**使用方法：**
```bash
python test_sites.py
```

---

### 16. test_sites_get.py - GET方法测试脚本

**用途：**
使用GET方法测试站点访问。

**使用方法：**
```bash
python test_sites_get.py
```

---

### 17. test_sites_no_proxy.py - 无代理测试脚本

**用途：**
不使用代理测试站点访问。

**使用方法：**
```bash
python test_sites_no_proxy.py
```

---

### 18. add_default_src.py - 添加默认src属性脚本

**用途：**
为使用Google favicon服务的图片添加默认src属性，避免显示小地球图标。

**功能概述：**
- 扫描HTML文件中的Google favicon服务URL
- 为这些图片添加默认src属性指向本地默认图片
- 修复Google favicon服务超时导致的图标显示问题

**使用方法：**
```bash
python add_default_src.py
```

---

### 19. fix_javascript_escape.py - 修复JavaScript模板变量转义脚本

**用途：**
修复动态生成的img标签中的转义变量问题。

**功能概述：**
- 修复JavaScript模板字符串中的转义变量（如`\${site.icon}`）
- 确保变量能够正确插值到动态生成的HTML中

**使用方法：**
```bash
python fix_javascript_escape.py
```

---

### 20. fix_javascript_img.py - 修复动态生成的img标签脚本

**用途：**
为JavaScript动态生成的img标签添加src属性。

**功能概述：**
- 为JavaScript代码中动态生成的img标签添加src属性
- 确保懒加载的图片能够正确显示

**使用方法：**
```bash
python fix_javascript_img.py
```

---

### 21. fix_favicon_urls.py - 修复favicon URL格式脚本

**用途：**
修复JSON数据文件中错误的faviconextractor.com URL格式。

**功能概述：**
- 将错误的URL格式`https://www.faviconextractor.com/favicon/{domain}?larger=true`
- 修复为正确的URL格式`https://www.faviconextractor.com/api/favicon/{domain}`
- 自动备份原始JSON文件

**使用方法：**
```bash
python fix_favicon_urls.py
```

---

### 22. fix_url_format.py - 修复URL格式脚本

**用途：**
修复JSON数据文件中的URL格式，去掉路径部分，只保留域名。

**功能概述：**
- 将包含路径的URL（如`https://echodata.work/home.html`）
- 修复为只包含域名的格式（如`https://echodata.work`）
- 自动备份原始JSON文件

**使用方法：**
```bash
python fix_url_format.py
```

---

### 23. check_png_file.py - 检查PNG文件有效性脚本

**用途：**
检查指定的PNG文件是否有效。

**功能概述：**
- 验证PNG文件的文件头是否正确
- 输出验证结果

**使用方法：**
```bash
python check_png_file.py <文件路径>
```

---

## 使用建议

### 日常维护流程：
1. 使用 `check_sites_validity.py` 定期检测站点有效性
2. 发现无效站点后，使用 `remove_invalid_sites.py` 删除
3. 使用 `cache_favicons.py` 更新favicon缓存
4. 使用 `final_fix.py` 重新生成HTML文件
5. 如有bug，使用 `fix_bugs.py` 修复

### 首次部署流程：
1. 准备JSON数据文件（完整版导航.json）
2. 运行 `cache_favicons.py` 下载favicon
3. 运行 `final_fix.py` 生成HTML文件
4. 将生成的HTML文件部署到服务器

### 数据更新流程：
1. 更新JSON数据文件
2. 运行 `check_sites_validity.py` 检测新添加的站点
3. 运行 `cache_favicons.py` 更新favicon
4. 运行 `final_fix.py` 重新生成HTML
5. 提交代码到GitHub触发自动部署

## 注意事项

1. 所有脚本都需要Python 3.x环境
2. 运行脚本前请确保JSON数据文件存在
3. 删除操作会自动创建备份文件
4. 建议在测试环境中先运行脚本，确认无误后再在生产环境使用
5. 某些脚本需要网络连接（如favicon下载、站点检测）

## 依赖库

所有脚本依赖以下Python库：
- `json` - JSON数据处理
- `os` - 文件系统操作
- `requests` - HTTP请求（需要安装：`pip install requests`）
- `re` - 正则表达式
- `hashlib` - 哈希计算
- `urllib.parse` - URL解析
- `shutil` - 文件操作
- `datetime` - 时间处理
- `concurrent.futures` - 并发处理

安装依赖：
```bash
pip install requests
```

## 版本历史

- v2.0 - 添加站点有效性检测、删除无效站点、bug修复脚本
- v1.1 - 添加站点有效性检测脚本
- v1.0 - 初始版本，包含所有基础脚本

## 联系方式

如有问题或建议，请联系：
- 网站：https://009tg.com
- 作者：Invisible Man
