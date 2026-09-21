@echo off
chcp 65001 >nul
setlocal
set PYTHONIOENCODING=utf-8
title Siya Pro - Floating Reactive Cat
cd /d "%~dp0"

echo.
echo ========================================================
echo   Siya PRO - Floating Calico Cat Assistant (Always Ready!)
echo ========================================================
echo.
echo   Interactions:
echo     - SINGLE CLICK  = Meow + random cute animation
echo     - DOUBLE CLICK  = Open chat panel
echo     - DRAG          = Move cat anywhere on screen
echo     - RIGHT-CLICK   = Menu (sounds, resize, animations, tasks)
echo     - MOUSE WHEEL   = Resize cat instantly
echo     - HOVER MOUSE   = Zoom + purr
echo.

REM --- Check / generate sprites ---
if not exist "cat_sprites\cat_normal.png" (
    echo [Build] Creating 15+ pro cat expression sprites for the first time...
    python -c "import sys; sys.stdout.reconfigure(errors='replace',encoding='utf-8'); from generate_pro_cat import generate_all; from pathlib import Path; generate_all(Path('cat_sprites'))" 2>nul
    echo.
)

REM --- Auto install Pillow if missing ---
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo [Install] Missing Pillow, installing now...
    pip install Pillow 2>nul
    echo.
)

echo [Launch] Starting Siya floating cat...
echo.
python siya_floating.py
