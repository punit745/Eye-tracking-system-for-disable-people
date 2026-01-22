# Eye Tracking System for People with Disabilities

A comprehensive, deployment-ready eye tracking system that enables people with physical disabilities to control their computer or smartphone interface through eye movements. This system serves as a replacement for traditional input devices (mouse, keyboard, touchpad) and is particularly helpful for people with spinal cord injuries, ALS (Amyotrophic Lateral Sclerosis), or other mobility-related challenges.

## 📖 Getting Started

**New to this project?** Follow our comprehensive step-by-step guide:
- 📘 **[Complete Setup Guide](SETUP_GUIDE.md)** - Detailed instructions from installation to first use
- 🚀 **[Quick Start Guide](QUICK_START.md)** - Get running in 3 simple steps
- 📚 **[Installation Guide](docs/INSTALLATION.md)** - Advanced installation options

## 🎯 Features

### Core Functionality
- **Real-time Eye Tracking**: Uses MediaPipe Face Mesh for accurate eye detection and tracking
- **Mouse Control**: Control cursor movement through eye gaze
- **Advanced Eye Gestures**:
  - Single blink for single click
  - Double blink for double click/open
  - Long blink for right click
  - Look left/right for horizontal navigation
  - Look up/down for scrolling
- **Hand Gesture Recognition**: Control system with hand gestures
  - Fist for click
  - Open palm for right click
  - Peace sign for double click
  - Thumbs up/down for scrolling
  - Swipe gestures for navigation
- **Multiple Click Modes**:
  - Dwell clicking (look at a point for specified time)
  - Gesture-based clicking (blinks and hand gestures)
  - Manual keyboard trigger
- **Virtual Keyboard**: On-screen keyboard for eye-controlled typing
- **Calibration System**: 9-point calibration for accurate gaze mapping
- **Smoothing & Filtering**: Reduces jitter for stable cursor control

### Accessibility Features
- Adjustable sensitivity and dwell times
- Visual feedback indicators
- Customizable gesture sensitivity
- Multiple input methods (eye + hand)
- Keyboard shortcuts for control
- Performance monitoring
- Real-time gesture feedback

### Technical Features
- Built with OpenCV and MediaPipe
- Cross-platform support (Windows, Linux, macOS)
- Configurable via YAML files
- Comprehensive logging system
- Real-time performance metrics
- Advanced gesture recognition
- Multi-modal input (eye + hand)

## 📋 Requirements

- Python 3.7 or higher
- Webcam
- Operating System: Windows 10/11, Linux, or macOS

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/punit745/Eye-tracking-system-for-disable-people.git
cd Eye-tracking-system-for-disable-people
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Quick Start
Run the main application:
```bash
python src/main.py
```

### With Custom Configuration
```bash
python src/main.py --config config/default_config.yaml
```

### Run Examples

**Basic Eye Tracking:**
```bash
python examples/basic_tracking.py
```

**Mouse Control:**
```bash
python examples/mouse_control.py
```

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `Q` or `ESC` | Quit application |
| `C` | Start calibration |
| `K` | Toggle virtual keyboard |
| `M` | Toggle mouse control on/off |
| `G` | Toggle hand gesture recognition |
| `H` | Hide/show UI |
| `R` | Reset calibration |
| `SPACE` | Manual click (when in manual mode) |

## 🎮 Gesture Controls

### Eye Gestures
- **Single Blink**: Click
- **Double Blink**: Double click / Open
- **Long Blink** (0.8s+): Right click
- **Look Up**: Scroll up
- **Look Down**: Scroll down
- **Look Left/Right**: Navigate horizontally

### Hand Gestures
- **Fist**: Click
- **Open Palm**: Right click
- **Peace Sign** (✌️): Double click
- **Thumbs Up** (👍): Scroll up
- **Thumbs Down** (👎): Scroll down
- **Swipe Up/Down**: Page up/down
- **Swipe Left/Right**: Navigate back/forward

For detailed gesture guide, see [GESTURE_GUIDE.md](docs/GESTURE_GUIDE.md)

## 🎮 How to Use

### First Time Setup

1. **Start the Application**
   ```bash
   python src/main.py
   ```

2. **Calibration** (Important!)
   - Press `C` to start calibration
   - Look at each calibration point as it appears
   - Hold your gaze steady for 2 seconds on each point
   - The system will automatically move to the next point
   - Complete all 9 points for best accuracy

3. **Enable Mouse Control**
   - After calibration, mouse control is automatically enabled
   - Move your eyes to control the cursor
   - Use gestures or dwell to click

4. **Try Gestures**
   - **Eye Gestures**: Try single blink, double blink, and directional gaze
   - **Hand Gestures**: Press `G` to enable, try fist, open palm, peace sign
   - See [Gesture Guide](docs/GESTURE_GUIDE.md) for complete list

5. **Using the Virtual Keyboard**
   - Press `K` to show/hide the virtual keyboard
   - Look at keys to select them
   - Dwell on a key to type it
   - Use special keys: SPACE, BACK, CLEAR, ENTER

### Tips for Best Performance

1. **Lighting**: Use good, even lighting on your face and hands
2. **Camera Position**: Position camera at eye level, about 50-70cm away
3. **Posture**: Maintain consistent head position
4. **Calibration**: Recalibrate if accuracy decreases
5. **Practice**: Takes a few minutes to get comfortable with eye control
6. **Gestures**: Start with basic gestures (single blink, fist) before trying advanced ones
7. **Hand Position**: Keep hand visible and well-lit for hand gestures

## 🔧 Configuration

Edit `config/default_config.yaml` to customize:

```yaml
mouse_control:
  sensitivity: 1.0        # Cursor movement sensitivity (0.1 - 3.0)
  smoothing: 5           # Smoothing window size
  dwell_time: 1.5        # Time to dwell for click (seconds)
  click_mode: dwell      # Options: dwell, blink, manual

calibration:
  num_points: 9          # Number of calibration points (4, 5, or 9)
  samples_per_point: 30  # Samples collected per point
  dwell_time: 2.0       # Time to look at each calibration point

accessibility:
  blink_detection: true   # Enable eye gesture detection
  gesture_control: true   # Enable gesture system
  hand_gestures: true     # Enable hand gesture recognition

gesture_settings:
  blink_threshold: 0.25              # Sensitivity for blink detection
  double_blink_interval: 0.5         # Max time between double blinks
  long_blink_duration: 0.8           # Min duration for long blink
  gaze_direction_threshold: 0.15     # Sensitivity for directional gaze
  hand_detection_confidence: 0.7     # Hand detection confidence
  gesture_cooldown: 0.5              # Time between gesture activations
```

## 📁 Project Structure

```
Eye-tracking-system-for-disable-people/
├── src/
│   ├── core/
│   │   ├── eye_tracker.py              # Eye tracking engine
│   │   ├── mouse_controller.py         # Mouse control logic
│   │   ├── calibration.py              # Calibration system
│   │   ├── virtual_keyboard.py         # Virtual keyboard
│   │   ├── gesture_manager.py          # Eye gesture detection
│   │   └── hand_gesture_recognizer.py  # Hand gesture recognition
│   ├── utils/
│   │   ├── config.py                   # Configuration management
│   │   └── logger.py                   # Logging utilities
│   └── main.py                         # Main application
├── examples/
│   ├── basic_tracking.py               # Basic tracking example
│   └── mouse_control.py                # Mouse control example
├── docs/
│   └── GESTURE_GUIDE.md                # Complete gesture guide
├── config/
│   └── default_config.yaml             # Default configuration
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🛠️ Technical Details

### Eye Tracking Pipeline
1. **Face Detection**: MediaPipe Face Mesh detects facial landmarks
2. **Eye Region Extraction**: Identifies eye contours and iris positions
3. **Gaze Estimation**: Calculates gaze ratio from iris position relative to eye
4. **Gesture Detection**: Analyzes eye movements and blinks for gestures
5. **Smoothing**: Moving average filter reduces jitter
6. **Calibration**: Maps gaze coordinates to screen coordinates
7. **Action**: Controls mouse cursor or activates clicks

### Hand Tracking Pipeline
1. **Hand Detection**: MediaPipe Hands detects hand landmarks
2. **Gesture Recognition**: Analyzes finger positions and movements
3. **Gesture Classification**: Identifies specific gestures
4. **Action Mapping**: Triggers corresponding system actions

### Algorithms
- **Eye Aspect Ratio (EAR)**: For blink detection
- **Iris Position Tracking**: Using MediaPipe's refined landmarks
- **Inverse Distance Weighting**: For calibration mapping
- **Moving Average**: For gaze smoothing
- **Gesture State Machines**: For complex gesture detection
- **Hand Landmark Analysis**: For finger state recognition

## 🐛 Troubleshooting

### Camera Not Working
- Check if camera is connected and permissions are granted
- Try different camera indices in config (0, 1, 2, etc.)
- Close other applications using the camera

### Poor Tracking Accuracy
- Improve lighting conditions
- Adjust camera position
- Run calibration again
- Check if face is fully visible
- Clean camera lens

### Cursor Too Fast/Slow
- Adjust `sensitivity` in config (lower = slower, higher = faster)
- Increase `smoothing` value for more stable movement

### Clicks Not Working
- Ensure clicking is enabled
- Check `dwell_time` setting (lower = faster clicks)
- Try gesture-based clicking (blinks or hand gestures)
- Verify gesture detection is working (check UI feedback)

### Gestures Not Detected
- Ensure good lighting conditions
- Adjust gesture sensitivity in config
- Practice clear, deliberate gestures
- Check gesture cooldown settings
- See [Gesture Guide](docs/GESTURE_GUIDE.md) for detailed troubleshooting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **MediaPipe**: For the face mesh solution
- **OpenCV**: For computer vision capabilities
- **PyAutoGUI**: For system control

## 📧 Contact

For questions, suggestions, or support, please open an issue on GitHub.

## 🌟 Use Cases

This system is designed for:
- People with spinal cord injuries
- ALS (Amyotrophic Lateral Sclerosis) patients
- Individuals with cerebral palsy
- Anyone with limited hand mobility
- Accessibility research and development
- Assistive technology demonstrations

## 🎓 Future Enhancements

Potential improvements for future versions:
- [x] Advanced eye gesture recognition (wink, look directions)
- [x] Hand gesture integration
- [ ] Voice command integration
- [ ] Mobile app support (iOS/Android)
- [ ] Cloud-based calibration profiles
- [ ] Machine learning for improved accuracy
- [ ] Multi-monitor support
- [ ] Customizable gesture mapping
- [ ] Integration with screen readers
- [ ] Head tilt controls
- [ ] Facial expression recognition
- [ ] Gesture macros and sequences

---

**Note**: This is an assistive technology tool. While it can significantly improve accessibility, users should consult with healthcare professionals and occupational therapists to ensure it meets their specific needs.