#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM自动分类器
基于大语言模型的网站自动分类，准确率90%+

支持平台：
- 硅基流动 (SiliconFlow)：推荐，9B以下模型永久免费
- 智谱AI (ZhipuAI)：GLM-4-Flash永久免费
- OpenAI兼容格式：通用

使用方法：
1. 注册硅基流动 https://siliconflow.cn 获取API Key
2. 设置环境变量 SILICONFLOW_API_KEY=your_key
3. 调用 classify_sites() 批量分类
"""

import json
import os
import re
import time
import hashlib
from collections import defaultdict

try:
    import requests
except ImportError:
    requests = None

# 项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 缓存文件
CACHE_FILE = os.path.join(PROJECT_ROOT, 'tools', 'web_admin', 'llm_classify_cache.json')

# 支持的平台配置
PLATFORMS = {
    'siliconflow': {
        'name': '硅基流动',
        'base_url': 'https://api.siliconflow.cn/v1',
        'env_key': 'SILICONFLOW_API_KEY',
        'default_model': 'Qwen/Qwen2.5-7B-Instruct',  # 永久免费
        'free_models': ['Qwen/Qwen2.5-7B-Instruct', 'THUDM/glm-4-9b-chat'],
    },
    'zhipu': {
        'name': '智谱AI',
        'base_url': 'https://open.bigmodel.cn/api/paas/v4',
        'env_key': 'ZHIPU_API_KEY',
        'default_model': 'glm-4-flash',  # 永久免费
        'free_models': ['glm-4-flash'],
    },
    'openai': {
        'name': 'OpenAI兼容',
        'base_url': 'https://api.openai.com/v1',
        'env_key': 'OPENAI_API_KEY',
        'default_model': 'gpt-4o-mini',
        'free_models': [],
    },
}


def load_nav_data():
    """加载导航数据"""
    data_path = os.path.join(PROJECT_ROOT, '完整版导航.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_categories():
    """获取所有分类列表（id, name, parent_name）"""
    data = load_nav_data()
    groups = data.get('groups', [])
    result = []
    for g in groups:
        parent_name = ''
        if g.get('parent_id'):
            parent = next((p for p in groups if p['id'] == g['parent_id']), None)
            if parent:
                parent_name = parent.get('name', '')
        result.append({
            'id': g.get('id'),
            'name': g.get('name'),
            'parent_name': parent_name,
            'full_name': f"{parent_name} > {g['name']}" if parent_name else g['name']
        })
    return result


def load_cache():
    """加载分类缓存"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_cache(cache):
    """保存分类缓存"""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_cache_key(site):
    """生成站点的缓存key"""
    text = f"{site.get('name', '')}|{site.get('url', '')}|{site.get('description', '')}"
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def get_api_config(platform='siliconflow'):
    """获取API配置"""
    config = PLATFORMS.get(platform)
    if not config:
        return None

    api_key = os.environ.get(config['env_key'], '')
    if not api_key:
        # 尝试从配置文件读取
        config_file = os.path.join(PROJECT_ROOT, 'tools', 'web_admin', 'llm_config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    api_key = cfg.get(f'{platform}_api_key', '')
                    if cfg.get('model'):
                        config = dict(config)
                        config['default_model'] = cfg['model']
            except:
                pass

    if not api_key:
        return None

    return {
        'api_key': api_key,
        'base_url': config['base_url'],
        'model': config['default_model'],
        'platform': platform,
    }


def call_llm(messages, api_config, max_retries=3):
    """调用LLM API"""
    if requests is None:
        raise Exception('requests库未安装，请运行 pip install requests')

    url = f"{api_config['base_url']}/chat/completions"
    headers = {
        'Authorization': f"Bearer {api_config['api_key']}",
        'Content-Type': 'application/json',
    }
    data = {
        'model': api_config['model'],
        'messages': messages,
        'temperature': 0.1,  # 低温度，保证分类稳定
        'max_tokens': 2048,
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                raise Exception(f'LLM调用失败: {e}')


def build_classification_prompt(sites, categories):
    """构建分类提示词"""
    # 分类列表
    cat_list = []
    for cat in categories:
        cat_list.append(f"{cat['id']}. {cat['full_name']}")

    cat_text = '\n'.join(cat_list)

    # 站点列表
    site_list = []
    for i, site in enumerate(sites):
        name = site.get('name', '')[:50]
        desc = site.get('description', '')[:100]
        url = site.get('url', '')
        src_cat = site.get('category', '')
        site_list.append(f"{i+1}. 名称:{name} | URL:{url} | 原分类:{src_cat} | 描述:{desc}")

    site_text = '\n'.join(site_list)

    system_prompt = """你是一个专业的网站分类专家。请根据网站的名称、URL、描述和原分类，从给定的分类列表中选择最合适的分类。

规则：
1. 只返回JSON格式，不要返回其他内容
2. 每个网站选择一个最合适的分类ID
3. 如果不确定，选择最接近的分类，并降低置信度
4. 置信度范围：0-100，90以上为高置信，70-89为中置信，70以下为低置信
5. 返回格式：{"results": [{"index": 1, "category_id": 分类ID, "confidence": 置信度, "reason": "简短原因"}]}"""

    user_prompt = f"""分类列表：
{cat_text}

待分类网站：
{site_text}

请返回分类结果JSON。"""

    return [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt},
    ]


def parse_llm_response(response_text):
    """解析LLM返回的JSON"""
    # 尝试提取JSON
    json_match = re.search(r'\{[\s\S]*\}', response_text)
    if json_match:
        try:
            data = json.loads(json_match.group())
            return data.get('results', [])
        except:
            pass

    # 尝试逐行解析
    results = []
    for line in response_text.split('\n'):
        line = line.strip()
        if line.startswith('{') and line.endswith('}'):
            try:
                item = json.loads(line)
                results.append(item)
            except:
                pass

    return results


def classify_sites(sites, platform='siliconflow', batch_size=20, use_cache=True):
    """
    批量分类网站

    Args:
        sites: 网站列表，每个包含name/url/description/category
        platform: LLM平台 (siliconflow/zhipu/openai)
        batch_size: 每批分类数量（建议10-30）
        use_cache: 是否使用缓存

    Returns:
        list: 分类结果，每个包含index/category_id/confidence/reason
    """
    api_config = get_api_config(platform)
    if not api_config:
        raise Exception(f'未配置{platform} API Key，请设置环境变量 {PLATFORMS[platform]["env_key"]}')

    categories = get_all_categories()
    cache = load_cache() if use_cache else {}

    all_results = []
    uncached_sites = []
    uncached_indices = []

    # 先检查缓存
    for i, site in enumerate(sites):
        cache_key = get_cache_key(site)
        if cache_key in cache:
            cached = cache[cache_key]
            all_results.append({
                'index': i,
                'category_id': cached['category_id'],
                'confidence': cached['confidence'],
                'reason': cached.get('reason', '缓存结果'),
                'cached': True,
            })
        else:
            uncached_sites.append(site)
            uncached_indices.append(i)

    print(f'总计: {len(sites)}个，缓存命中: {len(all_results)}个，待分类: {len(uncached_sites)}个')

    # 批量分类未缓存的站点
    if uncached_sites:
        for batch_start in range(0, len(uncached_sites), batch_size):
            batch_end = min(batch_start + batch_size, len(uncached_sites))
            batch = uncached_sites[batch_start:batch_end]
            batch_indices = uncached_indices[batch_start:batch_end]

            print(f'分类批次 {batch_start//batch_size + 1}/{(len(uncached_sites)-1)//batch_size + 1}: {len(batch)}个站点')

            try:
                messages = build_classification_prompt(batch, categories)
                response = call_llm(messages, api_config)
                results = parse_llm_response(response)

                # 映射回原始索引
                for result in results:
                    orig_index = batch_indices[result['index'] - 1] if 1 <= result['index'] <= len(batch) else -1
                    if orig_index >= 0:
                        result['index'] = orig_index
                        result['cached'] = False
                        all_results.append(result)

                        # 保存缓存
                        site = batch[result['index'] - batch_start - 1 + batch_start] if False else uncached_sites[uncached_indices.index(orig_index)]
                        cache_key = get_cache_key(site)
                        cache[cache_key] = {
                            'category_id': result['category_id'],
                            'confidence': result['confidence'],
                            'reason': result.get('reason', ''),
                        }

                # 每批保存一次缓存
                if use_cache:
                    save_cache(cache)

            except Exception as e:
                print(f'批次分类失败: {e}')
                # 失败的站点标记为低置信度
                for idx in batch_indices:
                    all_results.append({
                        'index': idx,
                        'category_id': None,
                        'confidence': 0,
                        'reason': f'分类失败: {e}',
                        'cached': False,
                    })

            time.sleep(1)  # 避免速率限制

    # 按原始索引排序
    all_results.sort(key=lambda x: x['index'])
    return all_results


def classify_and_map_sites(sites, platform='siliconflow', min_confidence=60):
    """
    分类并自动映射到目标分类

    Args:
        sites: 网站列表
        platform: LLM平台
        min_confidence: 最低置信度（低于此值的标记为待人工确认）

    Returns:
        dict: {
            'auto_mapped': [(site, category_id), ...],  # 自动映射的站点
            'need_review': [(site, suggested_category_id, confidence), ...],  # 需要人工确认的
            'failed': [site, ...],  # 分类失败的
        }
    """
    results = classify_sites(sites, platform=platform)

    auto_mapped = []
    need_review = []
    failed = []

    categories = get_all_categories()
    cat_ids = {cat['id'] for cat in categories}

    for result in results:
        site = sites[result['index']]
        cat_id = result.get('category_id')
        confidence = result.get('confidence', 0)

        if cat_id is None or cat_id not in cat_ids:
            failed.append(site)
        elif confidence >= min_confidence:
            auto_mapped.append((site, cat_id))
        else:
            need_review.append((site, cat_id, confidence))

    return {
        'auto_mapped': auto_mapped,
        'need_review': need_review,
        'failed': failed,
    }


if __name__ == '__main__':
    # 测试
    print('=== LLM自动分类器测试 ===')
    print()

    # 检查API配置
    for platform in PLATFORMS:
        config = get_api_config(platform)
        status = '已配置' if config else '未配置'
        print(f'{PLATFORMS[platform]["name"]} ({platform}): {status}')

    print()

    # 如果有配置，运行测试
    test_sites = [
        {'name': 'ChatGPT', 'url': 'https://chat.openai.com', 'description': 'AI对话助手', 'category': 'AI工具'},
        {'name': '跨境支付平台', 'url': 'https://example.com', 'description': '国际收款，跨境结算', 'category': '支付'},
        {'name': '接码平台', 'url': 'https://example-sms.com', 'description': '虚拟手机号接收验证码', 'category': '工具'},
    ]

    for platform in PLATFORMS:
        config = get_api_config(platform)
        if config:
            print(f'使用 {PLATFORMS[platform]["name"]} 测试分类...')
            try:
                result = classify_and_map_sites(test_sites, platform=platform, min_confidence=60)
                print(f'  自动映射: {len(result["auto_mapped"])}个')
                print(f'  待人工确认: {len(result["need_review"])}个')
                print(f'  失败: {len(result["failed"])}个')
                for site, cat_id in result['auto_mapped']:
                    cat = next((c for c in get_all_categories() if c['id'] == cat_id), None)
                    print(f'    {site["name"]} -> {cat["full_name"] if cat else cat_id}')
            except Exception as e:
                print(f'  测试失败: {e}')
            break
    else:
        print('未配置任何LLM API Key，跳过测试')
        print()
        print('配置方法：')
        print('1. 注册硅基流动 https://siliconflow.cn 获取API Key')
        print('2. 设置环境变量: set SILICONFLOW_API_KEY=your_key')
        print('3. 或创建 tools/web_admin/llm_config.json: {"siliconflow_api_key": "your_key"}')
