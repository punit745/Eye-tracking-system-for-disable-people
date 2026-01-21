# Installation Guide

## Quick Start

### Linux/Mac
```bash
./setup.sh
source venv/bin/activate
python src/main.py
```

### Windows
```cmd
setup.bat
venv\Scripts\activate.bat
python src\main.py
```

## Detailed Installation

### Prerequisites
- Python 3.7 or higher
- Webcam
- 4GB RAM (minimum)
- Windows 10/11, Linux, or macOS

### Step 1: Clone Repository
```bash
git clone https://github.com/punit745/Eye-tracking-system-for-disable-people.git
cd Eye-tracking-system-for-disable-people
```

### Step 2: Install Dependencies

#### Using Setup Script (Recommended)
**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

#### Manual Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate.bat
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
# Test camera
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL'); cap.release()"

# Test dependencies
python -c "import mediapipe; import pyautogui; print('All dependencies installed successfully')"
```

### Step 4: Run Application
```bash
python src/main.py
```

## Docker Installation

### Build and Run
```bash
# Build image
docker-compose build

# Run container
xhost +local:docker
docker-compose up
```

### Stop
```bash
docker-compose down
```

## Troubleshooting Installation

### Issue: pip install fails
**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Try installing dependencies one by one
pip install opencv-python
pip install mediapipe
pip install pyautogui
```

### Issue: Camera not accessible
**Linux:**
```bash
# Add user to video group
sudo usermod -a -G video $USER
# Logout and login again
```

**Windows:**
- Check camera permissions in Settings > Privacy > Camera

### Issue: MediaPipe installation fails
**Solution:**
```bash
# Install build tools
# Linux:
sudo apt-get install python3-dev build-essential
# Mac:
xcode-select --install
```

## Uninstallation

### Remove Virtual Environment
```bash
# Deactivate first
deactivate

# Remove directory
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
```

### Remove Application
```bash
cd ..
rm -rf Eye-tracking-system-for-disable-people  # Linux/Mac
rmdir /s Eye-tracking-system-for-disable-people  # Windows
```
