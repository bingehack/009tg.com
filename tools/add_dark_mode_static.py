#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给独立HTML页面添加深色模式支持
处理：about.html, 404.html, redirect.html
"""

import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 深色模式CSS
DARK_MODE_CSS = '''
    <style>
        /* ========== 深色模式主题变量 ========== */
        :root {
            --bg-main: #f4f4f4;
            --bg-content: #ffffff;
            --bg-sidebar: #303641;
            --bg-card: #ffffff;
            --bg-card-hover: #f8f9fa;
            --bg-navbar: #ffffff;
            --bg-input: #ffffff;
            --text-primary: #373e4a;
            --text-secondary: #6c757d;
            --text-muted: #979898;
            --border-color: #e4e6e9;
            --border-card: #e4e6e9;
            --link-color: #337ab7;
            --link-hover: #23527c;
            --shadow-card: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.15);
        }
        [data-theme="dark"] {
            --bg-main: #1a1d23;
            --bg-content: #22262e;
            --bg-sidebar: #16181d;
            --bg-card: #2a2f38;
            --bg-card-hover: #333945;
            --bg-navbar: #22262e;
            --bg-input: #2a2f38;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --text-muted: #707070;
            --border-color: #3a3f48;
            --border-card: #3a3f48;
            --link-color: #5dade2;
            --link-hover: #85c1e9;
            --shadow-card: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.5);
        }
        [data-theme="dark"] body {
            background-color: var(--bg-main) !important;
            color: var(--text-primary) !important;
        }
        [data-theme="dark"] .main-content {
            background-color: var(--bg-content) !important;
        }
        [data-theme="dark"] .navbar.user-info-navbar {
            background-color: var(--bg-navbar) !important;
            border-bottom-color: var(--border-color) !important;
        }
        [data-theme="dark"] .user-info-menu a {
            color: var(--text-primary) !important;
        }
        [data-theme="dark"] .user-info-menu a:hover {
            color: var(--link-color) !important;
        }
        [data-theme="dark"] .panel {
            background-color: var(--bg-card) !important;
            border-color: var(--border-card) !important;
        }
        [data-theme="dark"] .panel-heading {
            background-color: var(--bg-card) !important;
            border-bottom-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }
        [data-theme="dark"] .panel-title,
        [data-theme="dark"] .panel h4 {
            color: var(--text-primary) !important;
        }
        [data-theme="dark"] .panel-body {
            color: var(--text-secondary) !important;
        }
        [data-theme="dark"] .panel-body p,
        [data-theme="dark"] .panel-body li,
        [data-theme="dark"] .panel-body span {
            color: var(--text-secondary) !important;
        }
        [data-theme="dark"] .panel-body a {
            color: var(--link-color) !important;
        }
        [data-theme="dark"] .panel-body a:hover {
            color: var(--link-hover) !important;
        }
        [data-theme="dark"] .panel-body h1,
        [data-theme="dark"] .panel-body h2,
        [data-theme="dark"] .panel-body h3,
        [data-theme="dark"] .panel-body h4,
        [data-theme="dark"] .panel-body h5,
        [data-theme="dark"] .panel-body h6 {
            color: var(--text-primary) !important;
        }
        [data-theme="dark"] .text-gray,
        [data-theme="dark"] .text-muted {
            color: var(--text-muted) !important;
        }
        [data-theme="dark"] .breadcrumb {
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
        }
        [data-theme="dark"] .breadcrumb a {
            color: var(--link-color) !important;
        }
        [data-theme="dark"] .main-footer,
        [data-theme="dark"] footer {
            background-color: var(--bg-sidebar) !important;
            color: var(--text-secondary) !important;
        }
        [data-theme="dark"] .main-footer a,
        [data-theme="dark"] footer a {
            color: var(--link-color) !important;
        }
        [data-theme="dark"] .table {
            color: var(--text-primary) !important;
        }
        [data-theme="dark"] .table td,
        [data-theme="dark"] .table th {
            border-color: var(--border-color) !important;
            background-color: var(--bg-card) !important;
        }
        [data-theme="dark"] .well {
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }
        [data-theme="dark"] .alert-info {
            background-color: #1e3a5f !important;
            border-color: #2c5282 !important;
            color: #90cdf4 !important;
        }
        [data-theme="dark"] .alert-warning {
            background-color: #5f4a1e !important;
            border-color: #82682c !important;
            color: #f6e05e !important;
        }
        [data-theme="dark"] .alert-success {
            background-color: #1e5f3a !important;
            border-color: #2c8252 !important;
            color: #9ae6b4 !important;
        }
        [data-theme="dark"] .alert-danger {
            background-color: #5f1e1e !important;
            border-color: #822c2c !important;
            color: #feb2b2 !important;
        }
        [data-theme="dark"] .form-control,
        [data-theme="dark"] input,
        [data-theme="dark"] select,
        [data-theme="dark"] textarea {
            background-color: var(--bg-input) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }
        [data-theme="dark"] .horizontal-menu {
            background-color: var(--bg-sidebar) !important;
        }
        [data-theme="dark"] .navbar-brand .logo img {
            filter: brightness(1.5);
        }
        [data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3,
        [data-theme="dark"] h4, [data-theme="dark"] h5, [data-theme="dark"] h6 {
            color: var(--text-primary) !important;
        }
        /* 主题切换按钮 */
        .theme-toggle-btn {
            cursor: pointer;
            padding: 8px 12px;
            border-radius: 4px;
            transition: all 0.3s ease;
            background: transparent;
            border: none;
            font-size: 16px;
            color: inherit;
        }
        .theme-toggle-btn:hover {
            background-color: rgba(0,0,0,0.05);
        }
        [data-theme="dark"] .theme-toggle-btn:hover {
            background-color: rgba(255,255,255,0.1);
        }
    </style>
'''

# 主题切换JS
DARK_MODE_JS = '''
    <!-- 深色模式主题切换 -->
    <script>
        function initTheme() {
            var savedTheme = localStorage.getItem('theme');
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
                updateThemeIcon(savedTheme);
            } else {
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    document.documentElement.setAttribute('data-theme', 'dark');
                    updateThemeIcon('dark');
                }
            }
        }
        function toggleTheme() {
            var currentTheme = document.documentElement.getAttribute('data-theme');
            var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        }
        function updateThemeIcon(theme) {
            var icon = document.getElementById('theme-icon');
            if (icon) {
                if (theme === 'dark') {
                    icon.className = 'fa-sun-o';
                    icon.parentElement.title = '切换到浅色模式';
                } else {
                    icon.className = 'fa-moon-o';
                    icon.parentElement.title = '切换到深色模式';
                }
            }
        }
        initTheme();
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                if (!localStorage.getItem('theme')) {
                    if (e.matches) {
                        document.documentElement.setAttribute('data-theme', 'dark');
                        updateThemeIcon('dark');
                    } else {
                        document.documentElement.removeAttribute('data-theme');
                        updateThemeIcon('light');
                    }
                }
            });
        }
    </script>
'''

# 主题切换按钮（放在horizontal-menu中）
THEME_TOGGLE_BTN = '''
                <ul class="user-info-menu right-links list-inline list-unstyled" style="float: right; margin-top: 15px; margin-right: 20px;">
                    <li>
                        <button class="theme-toggle-btn" onclick="toggleTheme()" title="切换深色/浅色模式">
                            <i class="fa-moon-o" id="theme-icon"></i>
                        </button>
                    </li>
                </ul>
'''


def add_dark_mode_to_file(filepath):
    """给单个HTML文件添加深色模式支持"""
    if not os.path.exists(filepath):
        print(f"  文件不存在: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经添加了深色模式
    if 'data-theme="dark"' in content:
        print(f"  已包含深色模式，跳过: {filepath}")
        return True

    modified = False

    # 1. 在</head>之前添加CSS
    if '</head>' in content:
        content = content.replace('</head>', DARK_MODE_CSS + '\n</head>', 1)
        modified = True
        print(f"  已添加CSS")

    # 2. 在horizontal-menu的navbar-inner中添加切换按钮
    # 找到 <div class="navbar-mobile-clear"></div> 之前插入
    if 'navbar-mobile-clear' in content:
        content = content.replace(
            '<div class="navbar-mobile-clear"></div>',
            THEME_TOGGLE_BTN + '\n            <div class="navbar-mobile-clear"></div>',
            1
        )
        modified = True
        print(f"  已添加切换按钮")

    # 3. 在</body>之前添加JS
    if '</body>' in content:
        content = content.replace('</body>', DARK_MODE_JS + '\n</body>', 1)
        modified = True
        print(f"  已添加JS")

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  已保存: {filepath}")
        return True
    else:
        print(f"  未修改: {filepath}")
        return False


def main():
    files_to_process = [
        os.path.join(PROJECT_ROOT, 'cn', 'about.html'),
        os.path.join(PROJECT_ROOT, 'en', 'about.html'),
        os.path.join(PROJECT_ROOT, '404.html'),
        os.path.join(PROJECT_ROOT, 'redirect.html'),
    ]

    print("=" * 60)
    print("给独立页面添加深色模式支持")
    print("=" * 60)

    for filepath in files_to_process:
        print(f"\n处理: {filepath}")
        add_dark_mode_to_file(filepath)

    print("\n" + "=" * 60)
    print("处理完成！")


if __name__ == '__main__':
    main()
