@echo off
chcp 65001 >nul
title 009tg导航站 - Web管理后台
echo ==================================================
echo   009tg导航站 - Web管理后台
echo ==================================================
echo.
echo 正在启动...
echo.
echo 启动后将自动打开浏览器
echo 访问地址: http://127.0.0.1:5000
echo.
echo 关闭此窗口即可停止服务
echo ==================================================
echo.

cd /d "%~dp0"
python tools\web_admin\app.py

if errorlevel 1 (
    echo.
    echo 启动失败！请检查：
    echo 1. 是否已安装Python
    echo 2. 是否已安装Flask: pip install flask
    echo 3. 是否在项目根目录运行
    echo.
    pause
)
