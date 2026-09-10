@echo off
echo Installing Siya dependencies...
echo.

venv\Scripts\pip.exe install pyttsx3
venv\Scripts\pip.exe install --upgrade openai python-dotenv sounddevice scipy

echo.
echo Installation complete!
echo Run: python siya.py
pause
