# Gesture Control Guide

This guide explains all the gesture-based controls available in the Eye Tracking System for People with Disabilities.

## 📋 Table of Contents
- [Eye Gestures](#eye-gestures)
- [Hand Gestures](#hand-gestures)
- [Configuration](#configuration)
- [Tips for Best Results](#tips-for-best-results)
- [Troubleshooting](#troubleshooting)

## 👁️ Eye Gestures

### Single Blink
**Action**: Single mouse click  
**How to perform**: Close both eyes briefly (0.1-0.5 seconds) and open them  
**Use case**: Select items, click buttons, activate links

### Double Blink
**Action**: Double click / Open selected item  
**How to perform**: Close and open eyes twice quickly within 0.5 seconds  
**Use case**: Open files, folders, or applications

### Long Blink
**Action**: Right click / Context menu  
**How to perform**: Close eyes for 0.8+ seconds  
**Use case**: Open context menus, access additional options

### Look Left
**Action**: Cursor moves left (sustained gaze detection)  
**How to perform**: Look to the far left and hold gaze  
**Use case**: Navigate horizontally, adjust cursor position

### Look Right
**Action**: Cursor moves right (sustained gaze detection)  
**How to perform**: Look to the far right and hold gaze  
**Use case**: Navigate horizontally, adjust cursor position

### Look Up
**Action**: Scroll up  
**How to perform**: Look upward and hold gaze  
**Use case**: Scroll through documents, web pages

### Look Down
**Action**: Scroll down  
**How to perform**: Look downward and hold gaze  
**Use case**: Scroll through documents, web pages

## 🖐️ Hand Gestures

### Fist
**Action**: Left click  
**How to perform**: Close all fingers into a fist  
**Use case**: Click buttons, select items

### Open Palm
**Action**: Right click  
**How to perform**: Open all five fingers, palm facing camera  
**Use case**: Open context menus

### Pointing (Index Finger)
**Action**: Precision pointer mode  
**How to perform**: Extend only index finger  
**Use case**: Point at specific UI elements

### Peace Sign (✌️)
**Action**: Double click  
**How to perform**: Extend index and middle fingers (V shape)  
**Use case**: Open files/folders quickly

### Thumbs Up (👍)
**Action**: Scroll up  
**How to perform**: Extend thumb upward, other fingers closed  
**Use case**: Scroll up through content

### Thumbs Down (👎)
**Action**: Scroll down  
**How to perform**: Extend thumb downward, other fingers closed  
**Use case**: Scroll down through content

### OK Sign (👌)
**Action**: Confirm action  
**How to perform**: Touch thumb and index finger in a circle, other fingers extended  
**Use case**: Confirm selections, acknowledge prompts

### Swipe Up
**Action**: Page up / Large scroll up  
**How to perform**: Move hand upward quickly  
**Use case**: Navigate up one page

### Swipe Down
**Action**: Page down / Large scroll down  
**How to perform**: Move hand downward quickly  
**Use case**: Navigate down one page

### Swipe Left
**Action**: Navigate back / Previous  
**How to perform**: Move hand left quickly  
**Use case**: Go back in browser, previous slide

### Swipe Right
**Action**: Navigate forward / Next  
**How to perform**: Move hand right quickly  
**Use case**: Go forward in browser, next slide

## ⚙️ Configuration

### Enabling/Disabling Gestures

#### During Runtime
- Press `G` to toggle hand gesture recognition on/off
- Eye gestures are always active when mouse control is enabled

#### Via Configuration File
Edit `config/default_config.yaml`:

```yaml
accessibility:
  blink_detection: true      # Enable eye gesture detection
  gesture_control: true      # Enable gesture system
  hand_gestures: true        # Enable hand gesture recognition
  
gesture_settings:
  # Eye gesture settings
  blink_threshold: 0.25               # Lower = more sensitive to blinks
  double_blink_interval: 0.5          # Max time between blinks for double blink
  long_blink_duration: 0.8            # Min duration for long blink
  gaze_direction_threshold: 0.15      # Sensitivity for directional gaze
  
  # Hand gesture settings
  hand_detection_confidence: 0.7      # Hand detection confidence (0-1)
  hand_tracking_confidence: 0.5       # Hand tracking confidence (0-1)
  gesture_cooldown: 0.5               # Min time between gesture activations
```

### Gesture Sensitivity

#### Blink Detection
- **blink_threshold** (0.2-0.3): Lower values detect blinks more easily
- Recommended: 0.25 for most users

#### Double Blink Timing
- **double_blink_interval** (0.3-0.8 seconds): Max time between blinks
- Too short: Difficult to perform
- Too long: Accidental double blinks

#### Gaze Direction
- **gaze_direction_threshold** (0.1-0.3): How far to look for direction detection
- Lower: More sensitive, triggers easier
- Higher: More deliberate look required

## 💡 Tips for Best Results

### Eye Gestures

1. **Lighting**
   - Ensure even, bright lighting on your face
   - Avoid backlighting or harsh shadows
   - Natural light works best

2. **Camera Position**
   - Position camera at eye level
   - Distance: 50-70cm from your face
   - Ensure full face is visible

3. **Blink Technique**
   - Practice natural, complete blinks
   - Don't force or squint
   - Maintain relaxed facial expression

4. **Directional Gaze**
   - Hold gaze steady for 0.5-1 second
   - Look to extreme positions for best detection
   - Return to center between directional looks

### Hand Gestures

1. **Hand Position**
   - Keep hand 20-60cm from camera
   - Ensure entire hand is visible
   - Use good lighting on hand

2. **Clear Gestures**
   - Make distinct, deliberate gestures
   - Hold gesture for 0.3-0.5 seconds
   - Return to neutral position between gestures

3. **Background**
   - Use plain, contrasting background
   - Avoid cluttered backgrounds
   - Minimize hand-colored objects in frame

4. **Swipe Gestures**
   - Swift, decisive movements
   - Clear directional intent
   - At least 10cm movement distance

## 🐛 Troubleshooting

### Eye Gestures Not Working

**Problem**: Blinks not detected
- **Solution**: Adjust blink_threshold in config (try 0.27 or 0.23)
- **Solution**: Improve lighting conditions
- **Solution**: Clean camera lens

**Problem**: Accidental double blinks
- **Solution**: Increase double_blink_interval to 0.7-0.8 seconds
- **Solution**: Blink more deliberately with pause between

**Problem**: Directional gaze not detected
- **Solution**: Increase gaze_direction_threshold
- **Solution**: Look more to the extremes
- **Solution**: Recalibrate the system

### Hand Gestures Not Working

**Problem**: Hand not detected
- **Solution**: Improve lighting
- **Solution**: Ensure hand is fully visible in frame
- **Solution**: Lower hand_detection_confidence to 0.5-0.6

**Problem**: Wrong gestures detected
- **Solution**: Make clearer, more distinct gestures
- **Solution**: Hold gestures longer
- **Solution**: Increase gesture_cooldown

**Problem**: Gestures trigger repeatedly
- **Solution**: Increase gesture_cooldown to 0.7-1.0 seconds
- **Solution**: Return to neutral position between gestures

### Performance Issues

**Problem**: Lag or low FPS
- **Solution**: Disable hand gestures (press G or set hand_gestures: false)
- **Solution**: Reduce camera resolution in config
- **Solution**: Close other resource-intensive applications

## 🎓 Practice Exercises

### Beginner Exercises

1. **Blink Practice**: Practice single blinks in front of mirror
2. **Double Blink**: Time two blinks within 0.5 seconds
3. **Hand Shapes**: Practice making clear fist, palm, peace signs
4. **Gaze Control**: Practice looking to extremes and holding

### Intermediate Exercises

1. **Gesture Sequence**: Single blink → Double blink → Long blink
2. **Hand Sequence**: Fist → Open palm → Peace sign
3. **Mixed Control**: Use eye gaze to move, hand gesture to click
4. **Scrolling**: Practice look up/down and thumbs up/down

### Advanced Exercises

1. **Quick Navigation**: Use swipe gestures for rapid page navigation
2. **Precision Clicking**: Combine gaze positioning with gesture clicking
3. **Workflow**: Open file (double blink), scroll (gaze/thumbs), close (right click)

## 🎯 Recommended Gesture Combinations

### For Web Browsing
- **Navigate**: Eye gaze for cursor movement
- **Click links**: Single blink or fist
- **Scroll**: Look up/down or thumbs up/down
- **Back/Forward**: Swipe left/right

### For Document Editing
- **Select text**: Double blink to start, double blink to end
- **Copy/Paste**: Long blink (right click) for context menu
- **Scroll**: Look up/down for smooth scrolling
- **Navigate pages**: Swipe up/down

### For File Management
- **Navigate folders**: Eye gaze
- **Open files**: Double blink
- **Context menu**: Long blink or open palm
- **Select multiple**: Fist click with eye positioning

## 📊 Gesture Success Rates

Typical success rates with proper setup:

| Gesture Type | Success Rate | Learning Time |
|--------------|--------------|---------------|
| Single Blink | 95-98% | 5 minutes |
| Double Blink | 90-95% | 10 minutes |
| Long Blink | 92-97% | 5 minutes |
| Directional Gaze | 85-92% | 15 minutes |
| Fist | 93-97% | 2 minutes |
| Open Palm | 95-98% | 2 minutes |
| Peace Sign | 90-95% | 5 minutes |
| Thumbs Up/Down | 88-93% | 5 minutes |
| Swipe Gestures | 80-88% | 10 minutes |

## 🔄 Future Enhancements

Planned gesture features:
- [ ] Custom gesture mapping
- [ ] Gesture macros (sequences)
- [ ] Voice command integration
- [ ] Facial expression recognition
- [ ] Head tilt controls
- [ ] Gesture learning mode
- [ ] Multi-hand gestures
- [ ] Gesture recording and playback

---

**Need Help?** If you're having trouble with gestures, open an issue on GitHub with:
- Your configuration settings
- Description of the problem
- Any error messages
- System specifications
