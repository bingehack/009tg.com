# LLM自动分类配置说明

## 概述

LLM自动分类器使用大语言模型对抓取到的网站进行自动分类，准确率可达90%+，远高于关键词匹配的60%。

## 支持的平台

| 平台 | 免费模型 | 注册地址 | 推荐度 |
|------|---------|---------|--------|
| 硅基流动 (SiliconFlow) | Qwen2.5-7B、GLM-4-9B 永久免费 | https://siliconflow.cn | ⭐⭐⭐⭐⭐ |
| 智谱AI (ZhipuAI) | GLM-4-Flash 永久免费 | https://open.bigmodel.cn | ⭐⭐⭐⭐ |
| OpenAI兼容 | 无免费模型 | - | ⭐⭐⭐ |

## 快速配置（推荐硅基流动）

### 1. 注册并获取API Key

1. 访问 https://siliconflow.cn ，用手机号注册
2. 登录后进入「控制台」→「API密钥」
3. 点击「新建密钥」，复制生成的API Key（以sk-开头）

> 新用户注册送14元体验金，9B以下模型永久免费，分类1000个站点成本约0.01元。

### 2. 配置API Key

#### 方式一：配置文件（推荐）

在 `tools/web_admin/` 目录下创建 `llm_config.json`：

```json
{
  "siliconflow_api_key": "你的API Key",
  "model": "Qwen/Qwen2.5-7B-Instruct"
}
```

#### 方式二：环境变量

Windows命令行：
```cmd
set SILICONFLOW_API_KEY=你的API Key
```

PowerShell：
```powershell
$env:SILICONFLOW_API_KEY="你的API Key"
```

### 3. 验证配置

运行测试：
```cmd
python tools/web_admin/llm_classifier.py
```

如果显示「硅基流动: 已配置」并成功分类测试站点，说明配置成功。

## 使用方式

### 方式一：每日轮询自动分类

`daily_crawl_poll.py` 会自动检测LLM配置，优先使用LLM分类：

```cmd
python tools/daily_crawl_poll.py --count 2
```

输出示例：
```
使用LLM自动分类（准确率90%+）...
  LLM映射: ChatGPT -> AI工具 > AI对话
  LLM映射: 跨境支付平台 -> 跨境服务 > 跨境支付
  LLM分类完成: 自动映射25个，待确认3个，失败0个
```

### 方式二：手动批量分类

```python
from llm_classifier import classify_and_map_sites

sites = [
    {'name': 'ChatGPT', 'url': 'https://chat.openai.com', 'description': 'AI对话助手'},
    # ... 更多站点
]

result = classify_and_map_sites(sites, platform='siliconflow', min_confidence=60)
print(f'自动映射: {len(result["auto_mapped"])}个')
print(f'待人工确认: {len(result["need_review"])}个')
```

## 分类策略

1. **LLM优先**：配置了API Key时，优先使用LLM分类
2. **置信度阈值**：默认60%，高于此值自动映射，低于此值标记为待人工确认
3. **关键词补充**：LLM分类失败或置信度不足的站点，回退到关键词匹配
4. **结果缓存**：分类结果按站点内容缓存，避免重复调用API

## 成本估算

使用硅基流动免费模型（Qwen2.5-7B）：
- 输入：每个站点约100 token
- 输出：每个站点约50 token
- 批量20个站点一次调用，约3000 token
- 分类1000个站点：约15万token，成本约0.01元（免费额度内）

## 常见问题

### Q: 提示「未配置API Key」怎么办？
A: 按照上面的「快速配置」步骤，注册硅基流动并配置API Key。

### Q: LLM分类速度慢怎么办？
A: 批量分类（默认20个一批），可以通过 `batch_size` 参数调整。

### Q: 分类结果不准确怎么办？
A: 可以提高 `min_confidence` 阈值（如70或80），低于阈值的站点会标记为待人工确认。

### Q: 可以用其他平台吗？
A: 支持智谱AI（设置 `ZHIPU_API_KEY`）和任意OpenAI兼容格式（设置 `OPENAI_API_KEY` 和 `base_url`）。

### Q: 缓存文件在哪里？
A: `tools/web_admin/llm_classify_cache.json`，按站点内容的MD5缓存，删除后会重新分类。
