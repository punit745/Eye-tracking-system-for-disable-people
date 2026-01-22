# Quick Reference Guide

Quick reference card for Eye Tracking System gestures and controls.

## 🎮 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Q` or `ESC` | Quit application |
| `C` | Start calibration |
| `K` | Toggle virtual keyboard |
| `M` | Toggle mouse control on/off |
| `G` | Toggle hand gesture recognition |
| `H` | Hide/show UI |
| `R` | Reset calibration |
| `SPACE` | Manual click |

---

## 👁️ Eye Gestures

| Gesture | Duration | Action |
|---------|----------|--------|
| **Single Blink** | 0.1-0.5s | Click |
| **Double Blink** | Two blinks within 0.5s | Double click / Open |
| **Long Blink** | 0.8s+ | Right click / Menu |
| **Look Up** | Hold gaze upward | Scroll up |
| **Look Down** | Hold gaze downward | Scroll down |
| **Look Left** | Hold gaze left | Move cursor left |
| **Look Right** | Hold gaze right | Move cursor right |

---

## 🖐️ Hand Gestures

| Gesture | Hand Shape | Action |
|---------|------------|--------|
| **Fist** | All fingers closed | Click |
| **Open Palm** | All fingers extended | Right click |
| **Peace Sign** ✌️ | Index + middle fingers | Double click |
| **Pointing** | Index finger only | Precision pointer |
| **Thumbs Up** 👍 | Thumb up | Scroll up |
| **Thumbs Down** 👎 | Thumb down | Scroll down |
| **OK Sign** 👌 | Thumb + index circle | Confirm |
| **Swipe Up** | Quick upward motion | Page up |
| **Swipe Down** | Quick downward motion | Page down |
| **Swipe Left** | Quick left motion | Navigate back |
| **Swipe Right** | Quick right motion | Navigate forward |

---

## ⚙️ Quick Settings

### Adjust Blink Sensitivity
```yaml
gesture_settings:
  blink_threshold: 0.25  # Lower = more sensitive (0.2-0.3)
```

### Adjust Gesture Timing
```yaml
gesture_settings:
  double_blink_interval: 0.5    # Time for double blink (0.3-0.8s)
  long_blink_duration: 0.8       # Long blink duration (0.6-1.2s)
  gesture_cooldown: 0.5          # Time between gestures (0.3-1.0s)
```

### Adjust Cursor Speed
```yaml
mouse_control:
  sensitivity: 1.0    # 0.5 = slower, 2.0 = faster
  smoothing: 5        # Higher = smoother (3-10)
```

---

## 🎯 Tips for Best Results

### ✅ DO
- Use good, even lighting
- Position camera at eye level (50-70cm away)
- Keep head stable
- Make clear, deliberate gestures
- Practice basic gestures first
- Take breaks to avoid eye strain

### ❌ DON'T
- Use in poor lighting
- Move head excessively
- Make rushed gestures
- Skip calibration
- Use when tired
- Forget to blink naturally

---

## 🔧 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Blinks not detected | Adjust `blink_threshold` to 0.27 |
| Accidental double blinks | Increase `double_blink_interval` to 0.7 |
| Hand not detected | Improve lighting, ensure hand visible |
| Cursor too fast | Lower `sensitivity` to 0.7 |
| Cursor too slow | Increase `sensitivity` to 1.5 |
| Gestures trigger repeatedly | Increase `gesture_cooldown` to 0.8 |
| Poor accuracy | Run calibration (press `C`) |
| Low FPS | Disable hand gestures (press `G`) |

---

## 📱 Common Workflows

### Web Browsing
1. **Look** at link → **Single blink** to click
2. **Look down** to scroll
3. **Swipe left** to go back

### Document Reading
1. **Look up/down** for smooth scrolling
2. **Thumbs up/down** for page jumps
3. **Double blink** to select text

### File Navigation
1. **Look** at folder → **Double blink** to open
2. **Long blink** for context menu
3. **Fist gesture** to click items

---

## 🎓 Learning Path

### Week 1: Basics
- Master single blink clicking
- Practice cursor control
- Learn calibration process

### Week 2: Intermediate
- Add double blink for opening files
- Use directional gaze for scrolling
- Try basic hand gestures (fist, palm)

### Week 3: Advanced
- Long blink for right-click
- Peace sign for double click
- Swipe gestures for navigation

### Week 4: Expert
- Combine eye + hand gestures
- Create custom workflows
- Optimize personal settings

---

## 📞 Quick Help

- **Detailed Gesture Guide**: See `docs/GESTURE_GUIDE.md`
- **Configuration Help**: See `config/default_config.yaml`
- **Issues**: Open ticket on GitHub
- **Community**: Join discussions on project page

---

**Print this page and keep it handy while learning the system!**
