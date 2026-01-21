@echo off
REM Setup script for Eye Tracking System (Windows)

echo =======================================
echo Eye Tracking System Setup
echo =======================================
echo.

REM Check Python
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create directories
echo.
echo Creating directories...
if not exist logs mkdir logs
if not exist calibration_data mkdir calibration_data
if not exist config mkdir config

REM Check for webcam
echo.
echo Checking for webcam...
python -c "import cv2; cap = cv2.VideoCapture(0); print('Webcam found!' if cap.isOpened() else 'Webcam not found'); cap.release()"

echo.
echo =======================================
echo Setup Complete!
echo =======================================
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Run: python src\main.py
echo.
echo For examples:
echo   - Basic tracking: python examples\basic_tracking.py
echo   - Mouse control: python examples\mouse_control.py
echo.
pause
