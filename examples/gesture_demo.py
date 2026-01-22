"""
Gesture Control Example
Demonstrates the advanced eye and hand gesture features.
"""

import cv2
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.eye_tracker import EyeTracker
from core.hand_gesture_recognizer import HandGestureRecognizer, HandGesture
from core.gesture_manager import EyeGesture
import time


def main():
    """Main function to demonstrate gesture control."""
    print("=" * 60)
    print("Gesture Control Example")
    print("=" * 60)
    print("\nThis example demonstrates eye and hand gestures.")
    print("\nEye Gestures:")
    print("  - Single Blink: Detected and logged")
    print("  - Double Blink: Detected and logged")
    print("  - Long Blink: Detected and logged")
    print("  - Look Left/Right/Up/Down: Detected and logged")
    print("\nHand Gestures:")
    print("  - Fist, Open Palm, Peace, Thumbs Up/Down")
    print("  - Swipe gestures in all directions")
    print("\nPress 'q' to quit, 'h' to toggle hand gestures")
    print("=" * 60)
    
    # Initialize camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Cannot open camera")
        return 1
    
    # Set camera properties
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Initialize trackers
    eye_tracker = EyeTracker(
        max_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    hand_recognizer = HandGestureRecognizer(
        max_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    # Gesture counters
    gesture_counts = {
        'eye_gestures': {},
        'hand_gestures': {}
    }
    
    # Register callbacks
    def on_eye_gesture(gesture: EyeGesture):
        gesture_name = gesture.value
        gesture_counts['eye_gestures'][gesture_name] = \
            gesture_counts['eye_gestures'].get(gesture_name, 0) + 1
        print(f"👁️  Eye Gesture: {gesture_name.upper().replace('_', ' ')} "
              f"(Total: {gesture_counts['eye_gestures'][gesture_name]})")
    
    def on_hand_gesture(gesture: HandGesture):
        gesture_name = gesture.value
        gesture_counts['hand_gestures'][gesture_name] = \
            gesture_counts['hand_gestures'].get(gesture_name, 0) + 1
        print(f"🖐️  Hand Gesture: {gesture_name.upper().replace('_', ' ')} "
              f"(Total: {gesture_counts['hand_gestures'][gesture_name]})")
    
    # Register all eye gestures
    for gesture in EyeGesture:
        eye_tracker.register_gesture_callback(
            gesture, 
            lambda g=gesture: on_eye_gesture(g)
        )
    
    # Register all hand gestures
    for gesture in HandGesture:
        hand_recognizer.register_callback(
            gesture,
            lambda g=gesture: on_hand_gesture(g)
        )
    
    # Main loop
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Error: Failed to read frame")
                break
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process eye tracking
            processed_frame, eye_data = eye_tracker.process_frame(frame)
            if processed_frame is None:
                processed_frame = frame
            
            # Detect eye gestures
            if eye_data:
                eye_gesture = eye_tracker.detect_eye_gesture(eye_data)
            
            # Process hand gestures
            if hand_recognizer.is_enabled:
                processed_frame, hand_gesture = hand_recognizer.process_frame(processed_frame)
            
            # Draw statistics
            h, w = processed_frame.shape[:2]
            
            # Draw eye gesture stats
            y_pos = 30
            cv2.putText(processed_frame, "Eye Gestures:", (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            y_pos += 25
            for gesture_name, count in gesture_counts['eye_gestures'].items():
                text = f"  {gesture_name}: {count}"
                cv2.putText(processed_frame, text, (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_pos += 20
            
            # Draw hand gesture stats
            y_pos += 10
            hand_status = "ON" if hand_recognizer.is_enabled else "OFF"
            cv2.putText(processed_frame, f"Hand Gestures: {hand_status}", (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            y_pos += 25
            for gesture_name, count in gesture_counts['hand_gestures'].items():
                text = f"  {gesture_name}: {count}"
                cv2.putText(processed_frame, text, (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_pos += 20
            
            # Draw controls
            help_y = h - 60
            cv2.putText(processed_frame, "Controls:", (10, help_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            cv2.putText(processed_frame, "Q: Quit  |  H: Toggle Hand Gestures", 
                       (10, help_y + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display
            cv2.imshow("Gesture Control Demo", processed_frame)
            
            # Handle keyboard
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            elif key == ord('h'):
                hand_recognizer.toggle()
                status = "enabled" if hand_recognizer.is_enabled else "disabled"
                print(f"\nHand gesture recognition {status}")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    finally:
        # Cleanup
        print("\nCleaning up...")
        camera.release()
        eye_tracker.release()
        hand_recognizer.release()
        cv2.destroyAllWindows()
        
        # Print summary
        print("\n" + "=" * 60)
        print("Gesture Summary")
        print("=" * 60)
        print("\nEye Gestures:")
        for gesture_name, count in gesture_counts['eye_gestures'].items():
            print(f"  {gesture_name.replace('_', ' ').title()}: {count}")
        print("\nHand Gestures:")
        for gesture_name, count in gesture_counts['hand_gestures'].items():
            print(f"  {gesture_name.replace('_', ' ').title()}: {count}")
        print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
