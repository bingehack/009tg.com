@echo off
title 009tg Web Admin Panel
color 0A

echo ============================================
echo   009tg Navigation - Web Admin Panel
echo ============================================
echo.

REM Switch to script directory
cd /d "%~dp0"
echo Working directory: %CD%
echo.

REM Find Python
set PYTHON_CMD=
where python >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python
    echo Found Python: python
) else (
    where py >nul 2>&1
    if %errorlevel%==0 (
        set PYTHON_CMD=py
        echo Found Python: py
    )
)

if "%PYTHON_CMD%"=="" (
    echo.
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
%PYTHON_CMD% -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Flask not found, installing...
    %PYTHON_CMD% -m pip install flask requests beautifulsoup4 pillow pyyaml
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies.
        echo Please run manually: pip install flask requests beautifulsoup4 pillow pyyaml
        echo.
        pause
        exit /b 1
    )
)

echo Dependencies OK.
echo.
echo ============================================
echo Starting server...
echo URL: http://127.0.0.1:5000
echo Close this window to stop the server.
echo ============================================
echo.

REM Start the server
%PYTHON_CMD% tools\web_admin\app.py

echo.
echo ============================================
echo Server has stopped.
echo ============================================
echo.
pause
