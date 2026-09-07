# 009tg导航站 - 代码测试案例

## 测试范围

| 模块 | 脚本/文件 | 测试重点 |
|---|---|---|
| 数据层 | 完整版导航.json、raw/、category_mapping.yaml | 格式、完整性、一致性 |
| 构建层 | build_data.py | 合并、分类映射、去重、id分配、备份 |
| 生成层 | generate_new_html.py | HTML生成、分类树、分页、转义、备份 |
| 资源层 | cache_favicons.py | 下载、跳过、默认图标、MD5命名、映射保存 |
| 工具层 | crawler_utils.py | fetch_page、get_domain、normalize_url、去重、输出 |
| 抓取层 | crawl_*.py (4个) | 语法、配置、输出格式 |
| 维护层 | check_sites_validity.py、remove_invalid_sites.py、list_categories.py | 语法、基本功能 |

---

## 一、数据完整性测试

### TC-DATA-001: JSON格式有效性
- **前置条件**: 完整版导航.json存在
- **测试步骤**: 用json.load加载文件
- **预期结果**: 加载成功，无JSON语法错误
- **优先级**: P0

### TC-DATA-002: 分类id唯一性
- **前置条件**: 完整版导航.json加载成功
- **测试步骤**: 提取所有group的id，检查是否有重复
- **预期结果**: 所有分类id唯一，无重复
- **优先级**: P0

### TC-DATA-003: 站点id唯一性
- **前置条件**: 完整版导航.json加载成功
- **测试步骤**: 提取所有site的id，检查是否有重复
- **预期结果**: 所有站点id唯一，无重复
- **优先级**: P0

### TC-DATA-004: parent_id引用有效性
- **前置条件**: 完整版导航.json加载成功
- **测试步骤**: 检查每个group的parent_id是否为null或指向存在的分类id
- **预期结果**: 所有parent_id有效，无悬空引用
- **优先级**: P0

### TC-DATA-005: 站点url非空
- **前置条件**: 完整版导航.json加载成功
- **测试步骤**: 检查每个site的url字段是否非空
- **预期结果**: 所有站点url非空
- **优先级**: P0

### TC-DATA-006: 站点group_id与所在分类一致
- **前置条件**: 完整版导航.json加载成功
- **测试步骤**: 遍历每个group下的site，检查site.group_id是否等于group.id
- **预期结果**: 所有站点group_id与所在分类id一致
- **优先级**: P1

### TC-DATA-007: 一级分类无直接站点（除特殊分类）
- **前置条件**: 完整版导航.json加载成功
- **测试步骤**: 检查parent_id为null的分类是否有直接站点
- **预期结果**: 一级分类sites为空（站点都在子分类下）
- **优先级**: P2

### TC-DATA-008: category_mapping.yaml格式有效性
- **前置条件**: tools/category_mapping.yaml存在
- **测试步骤**: 用yaml.safe_load加载文件
- **预期结果**: 加载成功，包含_default配置和各源站映射
- **优先级**: P0

### TC-DATA-009: raw目录文件格式有效性
- **前置条件**: raw/目录存在
- **测试步骤**: 遍历raw/下所有.json文件（_开头除外），用json.load加载
- **预期结果**: 所有文件加载成功，包含category和sites字段
- **优先级**: P1

---

## 二、build_data.py 测试

### TC-BUILD-001: 语法检查
- **测试步骤**: python -m py_compile tools/build_data.py
- **预期结果**: 编译成功，无语法错误
- **优先级**: P0

### TC-BUILD-002: 正常合并（已有raw文件）
- **前置条件**: raw/目录有有效raw文件，完整版导航.json有备份
- **测试步骤**: 运行python tools/build_data.py
- **预期结果**: 运行成功，输出处理文件数、匹配分类数、新增站点数，最终验证分类数和站点数
- **优先级**: P0

### TC-BUILD-003: 自动备份机制
- **前置条件**: build_data.py运行前
- **测试步骤**: 检查完整版导航.json.build_backup是否在运行后更新
- **预期结果**: 运行前自动备份原文件为.build_backup
- **优先级**: P1

### TC-BUILD-004: 分类映射-精确匹配
- **前置条件**: category_mapping.yaml有映射规则
- **测试步骤**: 运行build_data.py，检查输出中"匹配到现有分类"的分类
- **预期结果**: 映射表中目标分类名存在的，都匹配到现有分类id
- **优先级**: P0

### TC-BUILD-005: 分类映射-降级全局匹配
- **前置条件**: 映射表中目标分类名在多个父分类下存在
- **测试步骤**: 运行build_data.py，检查是否创建了重复分类
- **预期结果**: 不创建重复分类，降级全局匹配到第一个同名分类
- **优先级**: P0

### TC-BUILD-006: 域名去重-已有数据去重
- **前置条件**: 完整版导航.json已有某域名
- **测试步骤**: raw/中有相同域名的站点，运行build_data.py
- **预期结果**: 重复域名被跳过，不重复添加
- **优先级**: P0

### TC-BUILD-007: 域名去重-raw内去重
- **前置条件**: 同一raw文件或不同raw文件中有相同域名
- **测试步骤**: 运行build_data.py
- **预期结果**: raw内重复域名只添加一次
- **优先级**: P1

### TC-BUILD-008: 自动分配id不重复
- **前置条件**: build_data.py运行后
- **测试步骤**: 检查所有新增站点的id是否与已有id重复
- **预期结果**: 新增站点id唯一，不与已有id冲突
- **优先级**: P0

### TC-BUILD-009: 未映射分类兜底
- **前置条件**: category_mapping.yaml中某源站分类未配置映射
- **测试步骤**: 运行build_data.py
- **预期结果**: 未映射分类进入_default.fallback_category
- **优先级**: P1

---

## 三、generate_new_html.py 测试

### TC-GEN-001: 语法检查
- **测试步骤**: python -m py_compile tools/generate_new_html.py
- **预期结果**: 编译成功
- **优先级**: P0

### TC-GEN-002: 正常生成HTML
- **测试步骤**: 运行python tools/generate_new_html.py
- **预期结果**: 运行成功，生成index.html，文件大小>0
- **优先级**: P0

### TC-GEN-003: 自动备份机制
- **测试步骤**: 运行generate_new_html.py前检查index.html.backup
- **预期结果**: 运行前自动备份原index.html为index.html.backup
- **优先级**: P1

### TC-GEN-004: favicon映射读取
- **前置条件**: favicon_mapping.json存在
- **测试步骤**: 运行generate_new_html.py，检查生成的HTML中站点icon字段
- **预期结果**: 站点icon使用favicon_mapping中的路径，而非默认路径
- **优先级**: P0

### TC-GEN-005: 分类树构建（一级/二级）
- **测试步骤**: 运行generate_new_html.py，检查HTML中导航菜单
- **预期结果**: 一级分类和二级分类正确嵌套显示
- **优先级**: P1

### TC-GEN-006: 分页逻辑（>18站点分页）
- **前置条件**: 某分类站点数>18
- **测试步骤**: 运行generate_new_html.py，检查该分类的data-pagination属性
- **预期结果**: >18站点的分类data-pagination="true"，<=18的为"false"
- **优先级**: P1

### TC-GEN-007: 特殊字符转义
- **前置条件**: 某站点名称或描述含引号、尖括号、&等特殊字符
- **测试步骤**: 运行generate_new_html.py，检查HTML中该站点数据
- **预期结果**: 特殊字符正确转义，不破坏HTML/JS结构
- **优先级**: P0

### TC-GEN-008: 空站点分类处理
- **前置条件**: 某分类sites为空
- **测试步骤**: 运行generate_new_html.py
- **预期结果**: 空分类不报错，正常生成（可能不显示或显示空）
- **优先级**: P2

### TC-GEN-009: HTML中站点数与JSON一致
- **测试步骤**: 统计完整版导航.json站点数，统计HTML中allSitesData的站点数
- **预期结果**: 两者一致
- **优先级**: P0

---

## 四、cache_favicons.py 测试

### TC-FAV-001: 语法检查
- **测试步骤**: python -m py_compile tools/cache_favicons.py
- **预期结果**: 编译成功
- **优先级**: P0

### TC-FAV-002: 默认图标路径正确
- **测试步骤**: 检查cache_favicons.py中default_icon_path
- **预期结果**: 路径为"assets/images/logos/default.png"（非../开头）
- **优先级**: P0

### TC-FAV-003: 已存在文件跳过
- **前置条件**: assets/favicons/已有某域名的PNG
- **测试步骤**: 运行cache_favicons.py，检查该域名是否跳过下载
- **预期结果**: 已存在的文件跳过，不重复下载
- **优先级**: P1

### TC-FAV-004: 下载失败使用默认图标
- **前置条件**: 某域名所有favicon源都无法访问
- **测试步骤**: 运行cache_favicons.py，检查该域名favicon文件
- **预期结果**: 复制默认图标到该域名favicon路径，不报错
- **优先级**: P0

### TC-FAV-005: MD5文件名生成
- **测试步骤**: 检查favicon文件名是否为32位十六进制MD5
- **预期结果**: 所有favicon文件名为MD5哈希.png
- **优先级**: P1

### TC-FAV-006: 映射文件保存
- **测试步骤**: 运行cache_favicons.py后检查favicon_mapping.json
- **预期结果**: 映射文件更新，包含所有站点域名→路径映射
- **优先级**: P0

### TC-FAV-007: 所有站点都有favicon文件
- **测试步骤**: 遍历完整版导航.json所有站点，检查favicon_mapping中有对应域名，且文件存在
- **预期结果**: 所有站点都有favicon映射，且对应文件存在（真实下载或默认图标）
- **优先级**: P0

---

## 五、crawler_utils.py 测试

### TC-UTIL-001: 语法检查
- **测试步骤**: python -m py_compile tools/crawler/crawler_utils.py
- **预期结果**: 编译成功
- **优先级**: P0

### TC-UTIL-002: get_domain - 正常URL
- **测试步骤**: 调用get_domain("https://www.example.com/path")
- **预期结果**: 返回"example.com"（去www，小写）
- **优先级**: P0

### TC-UTIL-003: get_domain - 带端口
- **测试步骤**: 调用get_domain("https://example.com:8080/path")
- **预期结果**: 返回"example.com"（去端口）
- **优先级**: P1

### TC-UTIL-004: normalize_url - 补全协议
- **测试步骤**: 调用normalize_url("example.com")
- **预期结果**: 返回"https://example.com"（补全https）
- **优先级**: P1

### TC-UTIL-005: is_valid_site_url - 有效URL
- **测试步骤**: 调用is_valid_site_url("https://www.example.com")
- **预期结果**: 返回True
- **优先级**: P0

### TC-UTIL-006: is_valid_site_url - 无效URL
- **测试步骤**: 调用is_valid_site_url("not-a-url")、is_valid_site_url("")
- **预期结果**: 返回False
- **优先级**: P0

### TC-UTIL-007: load_existing_domains
- **测试步骤**: 调用load_existing_domains()
- **预期结果**: 返回域名集合，数量>0，与完整版导航.json站点数一致
- **优先级**: P1

### TC-UTIL-008: save_raw_output - 输出格式
- **测试步骤**: 调用save_raw_output保存测试数据，检查输出文件
- **预期结果**: 文件包含category、source、sites等字段，sites中每个站点有name、url、description
- **优先级**: P0

### TC-UTIL-009: fetch_page - 正常请求
- **测试步骤**: 调用fetch_page("https://www.baidu.com")
- **预期结果**: 返回HTML内容，非空
- **优先级**: P1

### TC-UTIL-010: fetch_page - 超时重试
- **测试步骤**: 调用fetch_page("https://10.255.255.1", timeout=1, retries=2)
- **预期结果**: 重试指定次数后返回None，不抛异常
- **优先级**: P1

---

## 六、抓取脚本测试

### TC-CRAWL-001: 语法检查（4个脚本）
- **测试步骤**: 对crawl_aididai.py、crawl_tbox.py、crawl_tudingai.py、crawl_aih.py分别执行py_compile
- **预期结果**: 全部编译成功
- **优先级**: P0

### TC-CRAWL-002: 配置完整性
- **测试步骤**: 检查每个抓取脚本的CONFIG区
- **预期结果**: 包含source_name、输出目录配置，URL配置正确
- **优先级**: P1

### TC-CRAWL-003: 输出文件格式
- **前置条件**: 各抓取脚本已运行过，raw/有输出文件
- **测试步骤**: 检查raw/下各源站的JSON文件格式
- **预期结果**: 所有文件包含category和sites字段，sites中每个站点有name、url、description
- **优先级**: P0

### TC-CRAWL-004: 去重功能
- **测试步骤**: 检查raw/中是否有重复域名（同一源站内）
- **预期结果**: 同一源站内无重复域名
- **优先级**: P1

### TC-CRAWL-005: URL清理
- **测试步骤**: 检查raw/中站点URL是否含明显追踪参数（utm_、ref等）
- **预期结果**: 大部分URL已清理追踪参数（crawl_tudingai和crawl_aih有清理逻辑）
- **优先级**: P2

---

## 七、维护脚本测试

### TC-MAINT-001: 语法检查
- **测试步骤**: 对check_sites_validity.py、remove_invalid_sites.py、list_categories.py、cleanup_json.py、verify_cleanup.py执行py_compile
- **预期结果**: 全部编译成功
- **优先级**: P0

### TC-MAINT-002: list_categories.py正常运行
- **测试步骤**: 运行python tools/list_categories.py
- **预期结果**: 输出分类结构，无报错
- **优先级**: P1

### TC-MAINT-003: remove_invalid_sites.py正则匹配http和https
- **测试步骤**: 检查remove_invalid_sites.py中正则表达式
- **预期结果**: 正则同时匹配http://和https://
- **优先级**: P1

---

## 八、端到端流程测试

### TC-E2E-001: 完整流程（抓取→合并→favicon→生成）
- **前置条件**: 有一个测试用raw文件
- **测试步骤**:
  1. 运行build_data.py合并
  2. 运行cache_favicons.py下载favicon
  3. 运行generate_new_html.py生成HTML
- **预期结果**: 三步全部成功，最终HTML包含新增站点，favicon正常
- **优先级**: P0

### TC-E2E-002: 数据一致性（JSON→HTML）
- **测试步骤**: 统计完整版导航.json站点数和分类数，统计生成的HTML中allSitesData的站点数和分类数
- **预期结果**: 两者完全一致
- **优先级**: P0

### TC-E2E-003: 幂等性（重复运行build_data.py）
- **测试步骤**: 连续运行两次build_data.py
- **预期结果**: 第二次运行新增站点数为0，不重复添加
- **优先级**: P0

### TC-E2E-004: 幂等性（重复运行generate_new_html.py）
- **测试步骤**: 连续运行两次generate_new_html.py
- **预期结果**: 两次生成的HTML内容一致（除时间戳外）
- **优先级**: P1

---

## 测试执行记录

| 测试案例 | 结果 | 备注 |
|---|---|---|
| TC-DATA-001 | | |
| TC-DATA-002 | | |
| ... | | |

## 发现的Bug汇总

| Bug编号 | 严重度 | 模块 | 描述 | 状态 |
|---|---|---|---|---|
| | | | | |
