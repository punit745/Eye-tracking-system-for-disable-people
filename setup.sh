#!/bin/bash
# Setup script for Eye Tracking System

echo "======================================="
echo "Eye Tracking System Setup"
echo "======================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "Found: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p logs
mkdir -p calibration_data
mkdir -p config

# Check for webcam
echo ""
echo "Checking for webcam..."
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Webcam found!' if cap.isOpened() else 'Webcam not found'); cap.release()"

echo ""
echo "======================================="
echo "Setup Complete!"
echo "======================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python src/main.py"
echo ""
echo "For examples:"
echo "  - Basic tracking: python examples/basic_tracking.py"
echo "  - Mouse control: python examples/mouse_control.py"
echo ""
