@echo off
echo ========================================
echo   🐱 Starting Siya FREE Version 😺
echo ========================================
echo.
echo 💯 NO API COSTS! 100%% FREE!
echo.

REM Check if using Ollama
findstr /C:"USE_LOCAL_AI = True" siya_free.py >nul
if %errorlevel%==0 (
    echo Using: Ollama ^(Local AI^)
    echo Make sure Ollama is running!
    echo.
) else (
    echo Using: Groq ^(Cloud AI^)
    echo Make sure API key is configured!
    echo.
)

venv\Scripts\python.exe siya_free.py

echo.
echo Siya has closed. Goodbye! 👋
pause
