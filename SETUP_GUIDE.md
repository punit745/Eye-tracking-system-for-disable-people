# 🚀 Step-by-Step Setup Guide

## Complete Procedure to Run the Eye Tracking System Locally

This guide will walk you through the complete setup process from scratch to running the eye tracking system on your local machine.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Clone the Repository](#step-1-clone-the-repository)
3. [Step 2: Set Up Python Environment](#step-2-set-up-python-environment)
4. [Step 3: Install Dependencies](#step-3-install-dependencies)
5. [Step 4: Verify Installation](#step-4-verify-installation)
6. [Step 5: Run the Application](#step-5-run-the-application)
7. [Step 6: Calibrate the System](#step-6-calibrate-the-system)
8. [Step 7: Start Using the System](#step-7-start-using-the-system)
9. [Quick Setup (Using Scripts)](#quick-setup-using-scripts)
10. [Docker Setup (Alternative)](#docker-setup-alternative)
11. [Troubleshooting](#troubleshooting)
12. [Next Steps](#next-steps)

---

## Prerequisites

Before starting, ensure you have the following:

### Required:
- ✅ **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- ✅ **Webcam** (built-in or external)
- ✅ **4GB RAM** (minimum)
- ✅ **Internet connection** (for downloading dependencies)

### Operating System:
- Windows 10/11
- Linux (Ubuntu 18.04 or later)
- macOS (10.14 or later)

### Recommended:
- Good lighting in your workspace
- Comfortable seating with camera at eye level
- 50-70cm distance from camera

---

## Step 1: Clone the Repository

### Option A: Using Git Command Line

Open your terminal (Linux/Mac) or Command Prompt (Windows) and run:

```bash
git clone https://github.com/punit745/Eye-tracking-system-for-disable-people.git
cd Eye-tracking-system-for-disable-people
```

### Option B: Download as ZIP

1. Go to [GitHub Repository](https://github.com/punit745/Eye-tracking-system-for-disable-people)
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your preferred location
5. Open terminal/command prompt in the extracted folder

**✅ Verification:** You should see files like `README.md`, `requirements.txt`, `setup.sh`, etc.

---

## Step 2: Set Up Python Environment

### Check Python Installation

First, verify Python is installed:

#### On Windows:
```cmd
python --version
```

#### On Linux/Mac:
```bash
python3 --version
```

**Expected Output:** `Python 3.8.x` or higher

> **Note:** If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/)

### Create Virtual Environment

Creating a virtual environment keeps dependencies isolated:

#### On Windows:
```cmd
python -m venv venv
```

#### On Linux/Mac:
```bash
python3 -m venv venv
```

**✅ Verification:** A new `venv` folder should appear in your project directory.

### Activate Virtual Environment

#### On Windows:
```cmd
venv\Scripts\activate
```

#### On Linux/Mac:
```bash
source venv/bin/activate
```

**✅ Verification:** Your command prompt should now show `(venv)` at the beginning.

---

## Step 3: Install Dependencies

### Upgrade pip (Recommended)

First, ensure you have the latest pip version:

```bash
pip install --upgrade pip
```

### Install Project Dependencies

Install all required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

This will install:
- OpenCV (for computer vision)
- MediaPipe (for face detection)
- PyAutoGUI (for mouse control)
- PyQt5 (for GUI)
- And other necessary libraries

**⏱️ Time:** This may take 5-10 minutes depending on your internet speed.

**✅ Verification:** All packages should install without errors.

---

## Step 4: Verify Installation

Let's verify that everything is installed correctly:

### Test 1: Check Python Dependencies

```bash
python -c "import cv2, mediapipe, pyautogui, numpy, PyQt5; print('✅ All core dependencies installed successfully!')"
```

**Expected Output:** `✅ All core dependencies installed successfully!`

### Test 2: Check Camera Access

```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('✅ Camera detected!' if cap.isOpened() else '❌ Camera not found'); cap.release()"
```

**Expected Output:** `✅ Camera detected!`

> **Note:** If camera is not detected, see [Troubleshooting](#troubleshooting) section.

### Test 3: Run Basic Tracking Example

```bash
python examples/basic_tracking.py
```

**Expected Behavior:**
- A window should open showing your webcam feed
- Green dots should appear on your face (facial landmarks)
- Press `Q` to quit

**✅ Verification:** If you see facial landmarks tracking your face, the system is working!

---

## Step 5: Run the Application

Now let's run the main application:

```bash
python src/main.py
```

**What to Expect:**
- A window will open showing your webcam feed
- You'll see interface elements and status messages
- The system will start tracking your face and eyes
- Don't worry if the cursor doesn't move yet - calibration is needed first

**🎯 Keep the application running** for the next steps.

---

## Step 6: Calibrate the System

**⚠️ IMPORTANT:** Calibration is essential for accurate eye tracking!

### Start Calibration

While the application is running:

1. **Press the `C` key** to start calibration
2. A calibration screen will appear with numbered points

### Follow the Calibration Points

1. **Point 1-9 will appear one by one**
2. **Look directly at each point** when it appears
3. **Keep your gaze steady** for 2 seconds on each point
4. **Don't move your head** - only move your eyes
5. The system will automatically move to the next point

### Calibration Tips:
- Sit comfortably and maintain the same position
- Ensure good lighting on your face
- Keep your head still during calibration
- Follow each point with your eyes only
- Be patient - good calibration = better accuracy

**✅ Verification:** After completing all 9 points, you should see a "Calibration Complete" message.

---

## Step 7: Start Using the System

### Enable Mouse Control

After calibration, mouse control should be automatically enabled. If not:

1. **Press `M`** to toggle mouse control on/off

### Move the Cursor

1. **Look at different areas of the screen**
2. **The cursor should follow your gaze**
3. **Move your eyes, not your head** for best results

### Click by Dwelling

1. **Look at the location** where you want to click
2. **Hold your gaze steady** for 1.5 seconds
3. **A click will be performed** automatically

### Use Virtual Keyboard (Optional)

1. **Press `K`** to show the virtual keyboard
2. **Look at keys** to select them
3. **Dwell on a key** to type it
4. **Use special keys:** SPACE, BACK, CLEAR, ENTER

### Essential Controls

While the application is running:

| Key | Action |
|-----|--------|
| `Q` or `ESC` | Quit application |
| `C` | Start calibration |
| `K` | Toggle virtual keyboard |
| `M` | Toggle mouse control |
| `H` | Hide/show UI |
| `R` | Reset calibration |
| `SPACE` | Manual click (in manual mode) |

---

## Quick Setup (Using Scripts)

For faster setup, use the provided automated scripts:

### On Linux/Mac:

```bash
# Make script executable
chmod +x setup.sh

# Run setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Run application
python src/main.py
```

Or use the run script:
```bash
./run.sh
```

### On Windows:

```cmd
# Run setup script
setup.bat

# Activate virtual environment
venv\Scripts\activate.bat

# Run application
python src\main.py
```

Or use the run script:
```cmd
run.bat
```

**✅ Verification:** Scripts will create the virtual environment, install dependencies, and verify the setup automatically.

---

## Docker Setup (Alternative)

If you prefer using Docker:

### Prerequisites:
- Docker installed on your system
- Docker Compose installed

### Build and Run:

```bash
# Build Docker image
docker-compose build

# Allow Docker to access display (Linux only)
xhost +local:docker

# Run container
docker-compose up
```

### Stop Docker Container:

```bash
docker-compose down
```

> **Note:** Docker setup handles all dependencies automatically but requires Docker knowledge.

---

## Troubleshooting

### Problem: Python not found

**Solution:**
- Download and install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Restart your terminal after installation

### Problem: pip install fails

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing dependencies one by one
pip install opencv-python
pip install mediapipe
pip install pyautogui
pip install numpy
pip install PyQt5
```

### Problem: Camera not accessible

**Windows:**
1. Go to Settings > Privacy > Camera
2. Enable camera access for desktop apps
3. Close other applications using the camera

**Linux:**
```bash
# Add user to video group
sudo usermod -a -G video $USER
# Logout and login again
```

**macOS:**
1. Go to System Preferences > Security & Privacy > Camera
2. Grant camera permission to Terminal or your Python IDE

### Problem: MediaPipe installation fails

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential
pip install mediapipe
```

**Mac:**
```bash
xcode-select --install
pip install mediapipe
```

**Windows:**
- Install Microsoft C++ Build Tools
- Restart and try again

### Problem: Poor tracking accuracy

**Solutions:**
1. **Improve lighting** - Use good, even lighting on your face
2. **Adjust camera position** - Place at eye level, 50-70cm away
3. **Run calibration again** - Press `C` and recalibrate
4. **Check face visibility** - Ensure your entire face is visible
5. **Clean camera lens** - Remove dust or smudges
6. **Adjust sensitivity** - Edit `config/default_config.yaml`

### Problem: Cursor moves too fast/slow

**Solution:**
Edit `config/default_config.yaml` and adjust the sensitivity value:
```yaml
mouse_control:
  sensitivity: 1.0  # Lower = slower, Higher = faster (range: 0.1 - 3.0)
  smoothing: 5      # Higher = smoother movement
  dwell_time: 1.5
  click_mode: dwell
```

### Problem: Clicks not registering

**Solution:**
1. Ensure mouse control is enabled (press `M`)
2. Hold your gaze steady for the full dwell time
3. Adjust dwell time in `config/default_config.yaml`:
```yaml
mouse_control:
  sensitivity: 1.0
  smoothing: 5
  dwell_time: 1.5  # Lower = faster clicks (range: 0.5 - 3.0)
  click_mode: dwell
```

### Problem: Application crashes on startup

**Solutions:**
1. **Check camera availability:**
   ```bash
   python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened()); cap.release()"
   ```
2. **Verify all dependencies:**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```
3. **Check logs:**
   - Look in the `logs` folder for error messages
4. **Try different camera index:**
   - Edit config to use camera 1 instead of 0

### Still Having Issues?

1. Check the [full documentation](README.md)
2. Review [USER_GUIDE.md](docs/USER_GUIDE.md) for detailed usage
3. Check [INSTALLATION.md](docs/INSTALLATION.md) for advanced setup
4. Open an issue on [GitHub](https://github.com/punit745/Eye-tracking-system-for-disable-people/issues)

---

## Next Steps

### 🎓 Learn More:

1. **Read the User Guide:**
   ```bash
   cat docs/USER_GUIDE.md
   ```

2. **Try Examples:**
   ```bash
   # Mouse control example
   python examples/mouse_control.py
   
   # Complete demo
   python examples/complete_demo.py
   ```

3. **Customize Configuration:**
   - Edit `config/default_config.yaml`
   - Adjust sensitivity, dwell times, and click modes
   - Experiment with different settings

### 🎯 Practice:

1. **Start with simple tasks:**
   - Move cursor to different screen areas
   - Click on large buttons
   - Practice dwelling

2. **Progress to complex tasks:**
   - Browse the web
   - Use the virtual keyboard
   - Try different applications

3. **Master the controls:**
   - Learn all keyboard shortcuts
   - Switch between click modes
   - Use calibration when needed

### 🔧 Advanced Usage:

- **Multiple click modes:** Try dwell, blink, or manual modes
- **Custom configurations:** Create your own config files
- **Integration:** Use with screen readers and other assistive tools

---

## 📚 Additional Resources

- **Full Documentation:** [README.md](README.md)
- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **User Guide:** [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **Installation Details:** [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Project Summary:** [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)

---

## ✅ Setup Checklist

Use this checklist to track your progress:

- [ ] Python 3.8+ installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Camera access verified
- [ ] Basic tracking example works
- [ ] Main application runs
- [ ] System calibrated (9 points)
- [ ] Mouse control working
- [ ] Comfortable with basic controls

---

## 🎉 Congratulations!

You've successfully set up the Eye Tracking System! 

Remember:
- **Practice makes perfect** - It takes time to get comfortable with eye control
- **Calibrate regularly** - Recalibrate if you change position or lighting
- **Adjust settings** - Customize sensitivity and dwell times to your preference
- **Be patient** - This is assistive technology designed to help, take your time

**Need Help?** Open an issue on [GitHub](https://github.com/punit745/Eye-tracking-system-for-disable-people/issues)

---

**Note:** This is assistive technology designed for people with mobility impairments. Always consult with healthcare professionals to ensure it meets your specific needs.
