"""
Basic Eye Tracking Example
Simple example demonstrating basic eye tracking functionality.
"""

import cv2
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.eye_tracker import EyeTracker


def main():
    """Run basic eye tracking example."""
    print("Basic Eye Tracking Example")
    print("Press 'q' to quit")
    
    # Initialize eye tracker
    eye_tracker = EyeTracker()
    
    # Initialize camera
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("Error: Cannot open camera")
        return 1
    
    try:
        while True:
            # Read frame
            ret, frame = camera.read()
            if not ret:
                print("Error: Cannot read frame")
                break
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame
            processed_frame, eye_data = eye_tracker.process_frame(frame)
            
            if processed_frame is not None:
                # Display gaze information
                if eye_data and eye_data.get('gaze_ratio'):
                    gaze = eye_data['gaze_ratio']
                    text = f"Gaze: ({gaze[0]:.2f}, {gaze[1]:.2f})"
                    cv2.putText(processed_frame, text, (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Show frame
                cv2.imshow("Basic Eye Tracking", processed_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    
    finally:
        camera.release()
        eye_tracker.release()
        cv2.destroyAllWindows()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
