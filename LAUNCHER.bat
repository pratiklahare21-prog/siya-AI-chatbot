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
echo 1. FREE VERSION (Recommended!) 🆓
echo    - No API costs
echo    - Emoji cat expressions
echo    - Uses Ollama or Groq
echo.
echo 2. Advanced Version (OpenAI) 💰
echo    - Requires OpenAI credits
echo    - Voice input/output
echo    - ASCII art cat
echo.
echo 3. Basic Version (OpenAI) 💰
echo    - Requires OpenAI credits
echo    - Simple interface
echo.
echo 4. Exit
echo.
echo ========================================

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto FREE
if "%choice%"=="2" goto ADVANCED
if "%choice%"=="3" goto BASIC
if "%choice%"=="4" goto EXIT
echo Invalid choice! Please try again.
timeout /t 2 >nul
goto MENU

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
