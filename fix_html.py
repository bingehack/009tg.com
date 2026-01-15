#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML文件中的资源引用路径和标题信息
"""

def fix_html():
    """修复HTML文件"""
    
    # 读取HTML文件
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修复资源引用路径 - 去除../前缀
    content = content.replace('../assets/', 'assets/')
    
    # 2. 更新网站标题和描述
    content = content.replace('WebStack.cc - 设计师网址导航', '我的导航 - 跨境电商工具导航')
    content = content.replace('UI设计,UI设计素材,设计导航,网址导航,设计资源,创意导航,创意网站导航,设计师网址大全,设计素材大全,设计师导航,UI设计资源,优秀UI设计欣赏,设计师导航,设计师网址大全,设计师网址导航,产品经理网址导航,交互设计师网址导航,www.webstack.cc', '跨境电商,营销工具,AI工具,社交媒体,独立站,广告投放')
    content = content.replace('WebStack - 收集国内外优秀设计网站、UI设计资源网站、灵感创意网站、素材资源网站，定时更新分享优质产品设计书签。www.webstack.cc', '我的导航 - 收集国内外优秀的跨境电商工具、营销资源、AI工具、社交媒体平台等。')
    
    # 3. 保存修复后的HTML文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("HTML文件修复完成！")

if __name__ == '__main__':
    fix_html()
