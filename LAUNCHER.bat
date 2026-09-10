@echo off
title Siya AI Cat Assistant - Launcher
color 0B

:MENU
cls
echo ========================================
echo       🐱 SIYA AI CAT ASSISTANT 😺
echo ========================================
echo.
echo Choose your version:
echo.
echo 1. IMAGE VERSION (Best Visuals!) 🎨
echo    - Animated cat image
echo    - 6 reactive animations
echo    - Use your own cat photo!
echo    - FREE with Ollama/Groq
echo.
echo 2. FREE VERSION (Recommended!) 🆓
echo    - Giant emoji cat
echo    - No API costs
echo    - Uses Ollama or Groq
echo.
echo 3. ADVANCED VERSION (OpenAI) 💰
echo    - Voice input/output
echo    - Requires OpenAI credits
echo    - ASCII art cat
echo.
echo 4. BASIC VERSION (OpenAI) 💰
echo    - Simple interface
echo    - Requires OpenAI credits
echo.
echo 5. Exit
echo.
echo ========================================

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto IMAGE
if "%choice%"=="2" goto FREE
if "%choice%"=="3" goto ADVANCED
if "%choice%"=="4" goto BASIC
if "%choice%"=="5" goto EXIT
echo Invalid choice! Please try again.
timeout /t 2 >nul
goto MENU

:IMAGE
cls
echo ========================================
echo   🎨 Starting IMAGE Version 🐱
echo ========================================
echo.
echo Using: siya_image.py
echo Beautiful animated cat image!
echo.
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
venv\Scripts\python.exe siya_image.py
goto END

:FREE
cls
echo ========================================
echo   🆓 Starting FREE Version 😺
echo ========================================
echo.
echo Using: siya_free.py
echo No API costs!
echo.
venv\Scripts\python.exe siya_free.py
goto END

:ADVANCED
cls
echo ========================================
echo   💰 Starting Advanced Version
echo ========================================
echo.
echo WARNING: Requires OpenAI credits!
echo Using: siya_advanced.py
echo.
venv\Scripts\python.exe siya_advanced.py
goto END

:BASIC
cls
echo ========================================
echo   💰 Starting Basic Version
echo ========================================
echo.
echo WARNING: Requires OpenAI credits!
echo Using: siya.py
echo.
venv\Scripts\python.exe siya.py
goto END

:END
echo.
echo Siya has closed. Goodbye! 👋
echo.
pause
goto MENU

:EXIT
cls
echo.
echo Thanks for using Siya! 😺
echo.
timeout /t 1 >nul
exit
