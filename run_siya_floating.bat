@echo off
chcp 65001 >nul
title 🐱 Siya Floating - Reactive Cat Assistant
cd /d "%~dp0"

echo.
echo ============================================
echo   🐱 SIYA FLOATING CAT ASSISTANT 🐱
echo ============================================
echo.

REM Check if cat image exists, generate if not
if not exist "cat_image.png" (
    echo 🎨 Cat image not found. Creating beautiful cartoon cat...
    echo.
    python setup_floating_cat.py
    echo.
)

REM Check if Pillow is installed
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install Pillow requests
    echo.
)

echo 🚀 Launching Siya Floating Cat...
echo 💡 TIPS:
echo    • Click the cat to open/close chat
echo    • Right-click for MENU
echo    • Drag cat anywhere on screen
echo    • Type 'help' to see all commands
echo    • Type 'what can you do' for full feature list
echo.
echo 🐱 Your reactive cat is ready! Meow!
echo.

python siya_floating.py
