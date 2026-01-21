#!/bin/bash
# Run script for Eye Tracking System

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run application
echo "Starting Eye Tracking System..."
python src/main.py "$@"
