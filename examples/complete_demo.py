"""
Complete Demo - Eye Tracking System
Demonstrates all features of the eye tracking system.
"""

import cv2
import sys
import os
import time
import pyautogui

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.eye_tracker import EyeTracker
from core.mouse_controller import MouseController, ClickMode
from core.calibration import Calibration
from core.virtual_keyboard import VirtualKeyboard


class DemoMode:
    """Enumeration of demo modes."""
    TRACKING = "tracking"
    CALIBRATION = "calibration"
    MOUSE = "mouse"
    KEYBOARD = "keyboard"


class EyeTrackingDemo:
    """Complete demonstration of eye tracking system."""
    
    def __init__(self):
        """Initialize demo."""
        print("=" * 60)
        print("Eye Tracking System - Complete Demo")
        print("=" * 60)
        print("\nInitializing components...")
        
        # Get screen size
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"Screen: {self.screen_width}x{self.screen_height}")
        
        # Initialize components
        self.eye_tracker = EyeTracker()
        self.mouse_controller = MouseController(click_mode=ClickMode.DWELL)
        self.calibration = Calibration(self.screen_width, self.screen_height)
        self.virtual_keyboard = VirtualKeyboard()
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("Cannot open camera")
        
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # State
        self.current_mode = DemoMode.TRACKING
        self.is_running = True
        
        print("✓ Initialization complete\n")
        self.print_instructions()
    
    def print_instructions(self):
        """Print usage instructions."""
        print("\n" + "=" * 60)
        print("INSTRUCTIONS")
        print("=" * 60)
        print("\nModes:")
        print("  1 - Eye Tracking Demo")
        print("  2 - Calibration Demo")
        print("  3 - Mouse Control Demo")
        print("  4 - Virtual Keyboard Demo")
        print("\nControls:")
        print("  Q/ESC - Quit")
        print("  C - Start calibration")
        print("  M - Toggle mouse control")
        print("  K - Toggle virtual keyboard")
        print("  SPACE - Manual click")
        print("  H - Hide/show help text")
        print("\n" + "=" * 60)
    
    def process_tracking_mode(self, frame, eye_data):
        """Process tracking mode."""
        if eye_data and eye_data.get('gaze_ratio'):
            gaze = eye_data['gaze_ratio']
            
            # Draw gaze info
            h, w = frame.shape[:2]
            text_y = 30
            
            cv2.putText(frame, "MODE: Eye Tracking Demo", (10, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            text_y += 30
            cv2.putText(frame, f"Gaze X: {gaze[0]:.3f}", (10, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            text_y += 30
            cv2.putText(frame, f"Gaze Y: {gaze[1]:.3f}", (10, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Draw gaze direction indicator
            center_x, center_y = w // 2, h // 2
            gaze_x = int(center_x + (gaze[0] - 0.5) * 200)
            gaze_y = int(center_y + (gaze[1] - 0.5) * 200)
            
            cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)
            cv2.line(frame, (center_x, center_y), (gaze_x, gaze_y), (0, 255, 0), 2)
            cv2.circle(frame, (gaze_x, gaze_y), 10, (0, 255, 0), 2)
            
            # Detect blinks
            is_blinking = self.eye_tracker.detect_blink(eye_data)
            blink_text = "BLINKING" if is_blinking else "Eyes Open"
            blink_color = (0, 0, 255) if is_blinking else (0, 255, 0)
            cv2.putText(frame, blink_text, (10, h - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, blink_color, 2)
    
    def process_calibration_mode(self, frame, eye_data):
        """Process calibration mode."""
        if not self.calibration.is_active:
            self.calibration.start()
        
        gaze_ratio = None
        if eye_data and eye_data.get('gaze_ratio'):
            gaze_ratio = self.eye_tracker.get_smoothed_gaze(eye_data['gaze_ratio'])
        
        if gaze_ratio:
            is_complete = self.calibration.update(gaze_ratio)
            if is_complete:
                # Apply calibration
                cal_data = self.calibration.get_calibration_data()
                if cal_data:
                    for point in cal_data:
                        self.eye_tracker.add_calibration_point(
                            point['screen'], point['gaze']
                        )
                    self.eye_tracker.calibrate()
                
                print("✓ Calibration complete!")
                self.current_mode = DemoMode.MOUSE
        
        # Draw calibration UI
        current_point = self.calibration.get_current_point()
        if current_point:
            h, w = frame.shape[:2]
            cal_frame = cv2.resize(frame, (self.screen_width, self.screen_height))
            self.calibration.draw_calibration_point(cal_frame, current_point.screen_pos)
            self.calibration.draw_progress(cal_frame)
            frame[:] = cv2.resize(cal_frame, (w, h))
    
    def process_mouse_mode(self, frame, eye_data):
        """Process mouse control mode."""
        h, w = frame.shape[:2]
        
        cv2.putText(frame, "MODE: Mouse Control", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        status = "ENABLED" if self.mouse_controller.is_enabled else "DISABLED"
        color = (0, 255, 0) if self.mouse_controller.is_enabled else (0, 0, 255)
        cv2.putText(frame, f"Status: {status}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        if eye_data and eye_data.get('gaze_ratio'):
            gaze_ratio = self.eye_tracker.get_smoothed_gaze(eye_data['gaze_ratio'])
            
            if gaze_ratio:
                screen_pos = self.eye_tracker.gaze_to_screen_position(
                    gaze_ratio, self.screen_width, self.screen_height
                )
                
                if screen_pos and self.mouse_controller.is_enabled:
                    # Move cursor
                    self.mouse_controller.move_cursor(screen_pos)
                    
                    # Check for dwell click
                    self.mouse_controller.check_dwell_click(screen_pos)
                    
                    # Draw cursor position on frame
                    frame_x = int(screen_pos[0] * w / self.screen_width)
                    frame_y = int(screen_pos[1] * h / self.screen_height)
                    
                    cv2.circle(frame, (frame_x, frame_y), 15, (0, 255, 0), 2)
                    
                    # Draw dwell progress
                    progress = self.mouse_controller.get_dwell_progress()
                    if progress > 0:
                        radius = int(20 + progress * 30)
                        cv2.circle(frame, (frame_x, frame_y), radius, (0, 255, 0), 2)
                        
                        # Progress text
                        cv2.putText(frame, f"Dwell: {int(progress * 100)}%", (10, 90),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    def process_keyboard_mode(self, frame, eye_data):
        """Process virtual keyboard mode."""
        cv2.putText(frame, "MODE: Virtual Keyboard", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        if not self.virtual_keyboard.is_visible:
            self.virtual_keyboard.show()
        
        gaze_ratio = None
        if eye_data and eye_data.get('gaze_ratio'):
            gaze_ratio = self.eye_tracker.get_smoothed_gaze(eye_data['gaze_ratio'])
        
        if gaze_ratio:
            screen_pos = self.eye_tracker.gaze_to_screen_position(
                gaze_ratio, self.screen_width, self.screen_height
            )
            
            key_pressed = self.virtual_keyboard.update(screen_pos, frame)
            if key_pressed:
                print(f"Key pressed: {key_pressed}")
    
    def process_frame(self, frame):
        """Process a frame based on current mode."""
        # Track eyes
        processed_frame, eye_data = self.eye_tracker.process_frame(frame)
        
        if processed_frame is None:
            return frame
        
        # Process based on mode
        if self.current_mode == DemoMode.TRACKING:
            self.process_tracking_mode(processed_frame, eye_data)
        elif self.current_mode == DemoMode.CALIBRATION:
            self.process_calibration_mode(processed_frame, eye_data)
        elif self.current_mode == DemoMode.MOUSE:
            self.process_mouse_mode(processed_frame, eye_data)
        elif self.current_mode == DemoMode.KEYBOARD:
            self.process_keyboard_mode(processed_frame, eye_data)
        
        return processed_frame
    
    def handle_key(self, key):
        """Handle keyboard input."""
        if key == ord('q') or key == 27:  # Q or ESC
            return False
        elif key == ord('1'):
            self.current_mode = DemoMode.TRACKING
            print("\n→ Switched to Eye Tracking Demo")
        elif key == ord('2'):
            self.current_mode = DemoMode.CALIBRATION
            print("\n→ Starting Calibration Demo")
        elif key == ord('3'):
            self.current_mode = DemoMode.MOUSE
            print("\n→ Switched to Mouse Control Demo")
        elif key == ord('4'):
            self.current_mode = DemoMode.KEYBOARD
            print("\n→ Switched to Virtual Keyboard Demo")
        elif key == ord('c'):
            self.current_mode = DemoMode.CALIBRATION
            print("\n→ Starting Calibration")
        elif key == ord('m'):
            self.mouse_controller.toggle_control()
            status = "enabled" if self.mouse_controller.is_enabled else "disabled"
            print(f"\n→ Mouse control {status}")
        elif key == ord('k'):
            self.virtual_keyboard.toggle()
            status = "shown" if self.virtual_keyboard.is_visible else "hidden"
            print(f"\n→ Virtual keyboard {status}")
        elif key == ord(' '):
            self.mouse_controller.click()
            print("\n→ Manual click")
        elif key == ord('h'):
            self.print_instructions()
        
        return True
    
    def run(self):
        """Run the demo."""
        try:
            while self.is_running:
                # Read frame
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to read frame")
                    break
                
                # Flip for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process
                processed_frame = self.process_frame(frame)
                
                # Display
                cv2.imshow("Eye Tracking System - Complete Demo", processed_frame)
                
                # Handle input
                key = cv2.waitKey(1) & 0xFF
                if key != 255:
                    if not self.handle_key(key):
                        break
        
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user")
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("\nCleaning up...")
        
        if self.camera:
            self.camera.release()
        
        if self.eye_tracker:
            self.eye_tracker.release()
        
        cv2.destroyAllWindows()
        print("Demo closed")


def main():
    """Main entry point."""
    try:
        demo = EyeTrackingDemo()
        demo.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
