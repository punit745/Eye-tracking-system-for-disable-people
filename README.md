# Eye Tracking System for People with Disabilities

A comprehensive, deployment-ready eye tracking system that enables people with physical disabilities to control their computer or smartphone interface through eye movements. This system serves as a replacement for traditional input devices (mouse, keyboard, touchpad) and is particularly helpful for people with spinal cord injuries, ALS (Amyotrophic Lateral Sclerosis), or other mobility-related challenges.

## 🎯 Features

### Core Functionality
- **Real-time Eye Tracking**: Uses MediaPipe Face Mesh for accurate eye detection and tracking
- **Mouse Control**: Control cursor movement through eye gaze
- **Multiple Click Modes**:
  - Dwell clicking (look at a point for specified time)
  - Blink detection for clicking
  - Manual keyboard trigger
- **Virtual Keyboard**: On-screen keyboard for eye-controlled typing
- **Calibration System**: 9-point calibration for accurate gaze mapping
- **Smoothing & Filtering**: Reduces jitter for stable cursor control

### Accessibility Features
- Adjustable sensitivity and dwell times
- Visual feedback indicators
- Customizable click modes
- Keyboard shortcuts for control
- Performance monitoring

### Technical Features
- Built with OpenCV and MediaPipe
- Cross-platform support (Windows, Linux, macOS)
- Configurable via YAML files
- Comprehensive logging system
- Real-time performance metrics

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
| `H` | Hide/show UI |
| `R` | Reset calibration |
| `SPACE` | Manual click (when in manual mode) |

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
   - Dwell on a location for 1.5 seconds to click

4. **Using the Virtual Keyboard**
   - Press `K` to show/hide the virtual keyboard
   - Look at keys to select them
   - Dwell on a key to type it
   - Use special keys: SPACE, BACK, CLEAR, ENTER

### Tips for Best Performance

1. **Lighting**: Use good, even lighting on your face
2. **Camera Position**: Position camera at eye level, about 50-70cm away
3. **Posture**: Maintain consistent head position
4. **Calibration**: Recalibrate if accuracy decreases
5. **Practice**: Takes a few minutes to get comfortable with eye control

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
```

## 📁 Project Structure

```
Eye-tracking-system-for-disable-people/
├── src/
│   ├── core/
│   │   ├── eye_tracker.py          # Eye tracking engine
│   │   ├── mouse_controller.py     # Mouse control logic
│   │   ├── calibration.py          # Calibration system
│   │   └── virtual_keyboard.py     # Virtual keyboard
│   ├── utils/
│   │   ├── config.py               # Configuration management
│   │   └── logger.py               # Logging utilities
│   └── main.py                     # Main application
├── examples/
│   ├── basic_tracking.py           # Basic tracking example
│   └── mouse_control.py            # Mouse control example
├── config/
│   └── default_config.yaml         # Default configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🛠️ Technical Details

### Eye Tracking Pipeline
1. **Face Detection**: MediaPipe Face Mesh detects facial landmarks
2. **Eye Region Extraction**: Identifies eye contours and iris positions
3. **Gaze Estimation**: Calculates gaze ratio from iris position relative to eye
4. **Smoothing**: Moving average filter reduces jitter
5. **Calibration**: Maps gaze coordinates to screen coordinates
6. **Action**: Controls mouse cursor or activates clicks

### Algorithms
- **Eye Aspect Ratio (EAR)**: For blink detection
- **Iris Position Tracking**: Using MediaPipe's refined landmarks
- **Inverse Distance Weighting**: For calibration mapping
- **Moving Average**: For gaze smoothing

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
- Try different click modes (dwell vs blink)

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
- [ ] Eye gesture recognition (wink, look up/down for actions)
- [ ] Voice command integration
- [ ] Mobile app support (iOS/Android)
- [ ] Cloud-based calibration profiles
- [ ] Machine learning for improved accuracy
- [ ] Multi-monitor support
- [ ] Customizable action triggers
- [ ] Integration with screen readers

---

**Note**: This is an assistive technology tool. While it can significantly improve accessibility, users should consult with healthcare professionals and occupational therapists to ensure it meets their specific needs.