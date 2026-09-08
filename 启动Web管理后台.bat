@echo off
title 009tg Web Admin
echo ============================================
echo   009tg Navigation - Web Admin Panel
echo ============================================
echo.
echo Starting server...
echo URL: http://127.0.0.1:5000
echo Close this window to stop the server.
echo ============================================
echo.

cd /d "%~dp0"

REM Try to find python
where python >nul 2>&1
if %errorlevel%==0 (
    python tools\web_admin\app.py
) else (
    where py >nul 2>&1
    if %errorlevel%==0 (
        py tools\web_admin\app.py
    ) else (
        echo.
        echo ERROR: Python not found!
        echo Please install Python 3.8+ from https://python.org
        echo.
        pause
    )
)

if errorlevel 1 (
    echo.
    echo ============================================
    echo Server stopped with error.
    echo ============================================
    echo.
    echo Common issues:
    echo 1. Flask not installed: run "pip install flask"
    echo 2. Port 5000 in use: close other apps using port 5000
    echo 3. Missing dependencies: run "pip install flask requests beautifulsoup4 pillow pyyaml"
    echo.
    pause
)
