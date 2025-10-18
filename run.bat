@echo off
REM A simple script to set up and run The Telegraphist on Windows.

echo --- Setting up The Telegraphist ---
echo This may take a moment on the first run...

REM Check if Python is installed
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH. Please install Python to continue.
    pause
    exit /b 1
)

REM Create the virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

REM Activate the virtual environment
call .venv\Scripts\activate

REM Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt > nul

REM Run the game
echo Setup complete. Launching The Telegraphist...
echo Press CTRL+C to exit the game at any time.
timeout /t 1 /nobreak > nul
python main.py

REM Deactivate the environment
call venv\Scripts\deactivate

echo --- Thank you for playing! ---
pause