# 测试脚本说明

本目录包含各种测试和临时修复脚本，用于开发和调试过程中的特定问题。

## 脚本列表

### PNG文件检查脚本

- **check_png.py**
  - 用途：快速检查单个PNG文件的有效性
  - 使用方法：直接运行脚本，检查指定的PNG文件头
  - 说明：用于调试PNG文件格式问题

- **check_png_file.py**
  - 用途：检查指定PNG文件是否有效
  - 使用方法：`python check_png_file.py <文件路径>`
  - 说明：验证PNG文件的文件头签名

### 网站检查脚本

- **check_sites.py**
  - 用途：检查JSON数据中特定条件的网站
  - 使用方法：直接运行脚本
  - 说明：用于查找特定名称或URL模式的网站

### HTML修复脚本

- **fix_all_html.py**
  - 用途：为所有HTML文件中的懒加载图片添加src属性
  - 使用方法：直接运行脚本
  - 说明：修复index.html、cn/index.html、en/index.html

- **fix_bugs.py**
  - 用途：修复3个特定的bug（关于本站链接、favicon路径、语言切换器）
  - 使用方法：直接运行脚本
  - 说明：针对英文版本的问题修复

- **fix_html.py**
  - 用途：修复HTML文件中的资源引用路径和标题信息
  - 使用方法：直接运行脚本
  - 说明：修复资源路径和更新网站标题

- **fix_issues.py**
  - 用途：修复导航网站中的各种问题
  - 使用方法：直接运行脚本
  - 说明：构建分类树并修复导航菜单

- **fix_lazy_loading.py**
  - 用途：为index.html中的懒加载图片添加src属性
  - 使用方法：直接运行脚本
  - 说明：只修复根目录的index.html

- **fix_url_format.py**
  - 用途：修复JSON数据文件中的URL格式，去掉路径部分
  - 使用方法：直接运行脚本
  - 说明：将URL从`https://echodata.work/home.html`改为`https://echodata.work`

### HTML生成脚本

- **generate_english.py**
  - 用途：将中文版HTML文件翻译为英文版本
  - 使用方法：直接运行脚本
  - 说明：使用预定义的翻译映射表替换中文内容

- **generate_nested_nav.py**
  - 用途：生成带有嵌套导航菜单的HTML文件
  - 使用方法：直接运行脚本
  - 说明：支持多级嵌套导航结构

- **keep_style_generate.py**
  - 用途：保持原有风格生成新的导航网站
  - 使用方法：直接运行脚本
  - 说明：只更新导航和内容部分，保持样式不变

- **simple_generate.py**
  - 用途：简单的HTML生成脚本
  - 使用方法：直接运行脚本
  - 说明：基础的HTML生成功能

- **convert_json_to_html.py**
  - 用途：将JSON数据转换为HTML格式
  - 使用方法：直接运行脚本
  - 说明：基础的JSON到HTML转换

## 注意事项

1. 这些脚本主要用于开发和调试，可能需要根据实际情况进行修改
2. 运行前请确保已正确配置Python环境和依赖库
3. 部分脚本可能会修改现有的HTML文件，建议先备份
4. 这些脚本不再用于生产环境的HTML生成，请使用tools目录下的主要脚本

## 主要脚本目录

对于生产环境的HTML生成和维护，请使用tools目录下的主要脚本：

- `generate_new_html.py` - 主要的HTML生成脚本
- `cache_favicons.py` - Favicon缓存脚本
- `check_sites_validity.py` - 站点有效性检测
- `remove_invalid_sites.py` - 删除无效站点
- `fix_favicon_urls.py` - 修复faviconextractor.com API URL格式
- `fix_javascript_escape.py` - 修复JavaScript模板变量转义
- `fix_javascript_img.py` - 修复动态生成的img标签
- `add_default_src.py` - 为Google favicon服务添加默认src属性
