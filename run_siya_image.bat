@echo off
echo ========================================
echo   🎨 Starting Siya Image Version 🐱
echo ========================================
echo.
echo ✨ Beautiful Animated Cat Interface!
echo 💯 100%% FREE!
echo.

REM Check if cat image exists
if exist cat_image.png (
    echo ✅ Cat image found!
) else (
    echo 💡 No cat image - will create placeholder
    echo.
    echo To use your own cat:
    echo 1. Save as cat_source.png
    echo 2. Run: python setup_cat_image.py
)

echo.
echo Starting...
echo.

venv\Scripts\python.exe siya_image.py

echo.
echo Siya has closed. Goodbye! 👋
pause
