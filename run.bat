@echo off
REM Run script for Eye Tracking System (Windows)

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run application
echo Starting Eye Tracking System...
python src\main.py %*
