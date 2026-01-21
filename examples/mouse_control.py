"""
Mouse Control Example
Example demonstrating mouse control with eye tracking.
"""

import cv2
import sys
import os
import pyautogui

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.eye_tracker import EyeTracker
from core.mouse_controller import MouseController, ClickMode


def main():
    """Run mouse control example."""
    print("Mouse Control Example")
    print("Controls:")
    print("  'q' - Quit")
    print("  'm' - Toggle mouse control")
    print("  SPACE - Manual click")
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    
    # Initialize components
    eye_tracker = EyeTracker()
    mouse_controller = MouseController(
        sensitivity=1.0,
        dwell_time=1.5,
        click_mode=ClickMode.DWELL
    )
    
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
                break
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame
            processed_frame, eye_data = eye_tracker.process_frame(frame)
            
            if processed_frame is not None and eye_data:
                # Get gaze information
                gaze_ratio = eye_data.get('gaze_ratio')
                
                if gaze_ratio:
                    # Convert to screen position
                    screen_pos = eye_tracker.gaze_to_screen_position(
                        gaze_ratio, screen_width, screen_height
                    )
                    
                    # Control mouse
                    if mouse_controller.is_enabled:
                        mouse_controller.move_cursor(screen_pos)
                        mouse_controller.check_dwell_click(screen_pos)
                        
                        # Show dwell progress
                        progress = mouse_controller.get_dwell_progress()
                        if progress > 0:
                            h, w = processed_frame.shape[:2]
                            text = f"Dwell: {int(progress * 100)}%"
                            cv2.putText(processed_frame, text, (10, 60),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display status
                status = "Mouse: ON" if mouse_controller.is_enabled else "Mouse: OFF"
                color = (0, 255, 0) if mouse_controller.is_enabled else (0, 0, 255)
                cv2.putText(processed_frame, status, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                # Show frame
                cv2.imshow("Mouse Control", processed_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                mouse_controller.toggle_control()
                print(f"Mouse control: {'enabled' if mouse_controller.is_enabled else 'disabled'}")
            elif key == ord(' '):
                mouse_controller.click()
    
    finally:
        camera.release()
        eye_tracker.release()
        cv2.destroyAllWindows()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
