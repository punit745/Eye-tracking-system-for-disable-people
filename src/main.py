"""
Main Application Module
Main application for eye tracking system with GUI.
"""

import cv2
import numpy as np
import time
from typing import Optional
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.eye_tracker import EyeTracker
from core.mouse_controller import MouseController, ClickMode
from core.calibration import Calibration
from core.virtual_keyboard import VirtualKeyboard
from core.hand_gesture_recognizer import HandGestureRecognizer, HandGesture
from core.gesture_manager import EyeGesture
from utils.config import Config
from utils.logger import setup_logger, PerformanceLogger


class EyeTrackingApp:
    """Main application for eye tracking system."""
    
    def __init__(self, config_file: str = None, gesture_mode: int = 3):
        """
        Initialize application.
        
        Args:
            config_file: Path to configuration file
            gesture_mode: Gesture control mode (1=Eye only, 2=Hand only, 3=Both)
        """
        # Load configuration
        self.config = Config(config_file)
        
        # Setup logger
        log_config = self.config.get_section('logging')
        self.logger = setup_logger(
            name="EyeTrackingApp",
            log_file=log_config.get('log_file'),
            level=log_config.get('level', 'INFO')
        )
        
        self.perf_logger = PerformanceLogger(self.logger)
        
        # Initialize camera
        self.camera = None
        self.init_camera()
        
        # Initialize components
        self.eye_tracker = EyeTracker(
            max_faces=self.config.get('eye_tracking.max_faces', 1),
            min_detection_confidence=self.config.get('eye_tracking.min_detection_confidence', 0.5),
            min_tracking_confidence=self.config.get('eye_tracking.min_tracking_confidence', 0.5)
        )
        
        click_mode_str = self.config.get('mouse_control.click_mode', 'dwell')
        click_mode = ClickMode.DWELL if click_mode_str == 'dwell' else ClickMode.BLINK
        
        self.mouse_controller = MouseController(
            sensitivity=self.config.get('mouse_control.sensitivity', 1.0),
            smoothing=self.config.get('mouse_control.smoothing', 5),
            dwell_time=self.config.get('mouse_control.dwell_time', 1.5),
            click_mode=click_mode
        )
        
        self.calibration = Calibration()
        self.virtual_keyboard = VirtualKeyboard(
            position=tuple(self.config.get('keyboard.position', [50, 50])),
            key_size=tuple(self.config.get('keyboard.key_size', [60, 60])),
            spacing=self.config.get('keyboard.spacing', 10),
            dwell_time=self.config.get('keyboard.dwell_time', 1.5)
        )
        
        # Store gesture mode (1=Eye only, 2=Hand only, 3=Both)
        self.gesture_mode = gesture_mode
        self.gesture_mode_names = {1: "Eye Only", 2: "Hand Only", 3: "Both"}
        
        # Initialize eye gesture handling based on mode
        self.eye_gesture_enabled = gesture_mode in [1, 3]  # Enable for Eye only or Both
        
        # Initialize hand gesture recognizer based on mode
        self.hand_gesture_enabled = gesture_mode in [2, 3]  # Enable for Hand only or Both
        self.hand_gesture_recognizer = None
        if self.hand_gesture_enabled:
            self.hand_gesture_recognizer = HandGestureRecognizer(
                max_hands=1,
                min_detection_confidence=self.config.get('gesture_settings.hand_detection_confidence', 0.75),
                min_tracking_confidence=self.config.get('gesture_settings.hand_tracking_confidence', 0.7)
            )
            # Set swipe threshold from config
            swipe_threshold = self.config.get('gesture_settings.swipe_threshold', 100)
            self.hand_gesture_recognizer.swipe_threshold = swipe_threshold
            self._setup_hand_gesture_callbacks()
        
        # Application state
        self.is_running = False
        self.is_calibrating = False
        self.show_ui = True
        self.fps = 0
        self.last_eye_gesture = None
        self.last_hand_gesture = None
        self.frame_count = 0  # For frame skipping optimization
        self.hand_gesture_skip_frames = 2  # Process hand gestures every Nth frame
        
        # Setup eye gesture callbacks only if eye gestures are enabled
        if self.eye_gesture_enabled:
            self._setup_eye_gesture_callbacks()
        
        self.logger.info(f"Eye Tracking Application initialized (Mode: {self.gesture_mode_names[gesture_mode]})")
    
    def init_camera(self):
        """Initialize camera."""
        camera_config = self.config.get_section('camera')
        device_id = camera_config.get('device_id', 0)
        use_threaded = camera_config.get('use_threaded', True)  # Enable by default
        
        width = camera_config.get('width', 640)
        height = camera_config.get('height', 480)
        fps = camera_config.get('fps', 30)
        
        if use_threaded:
            try:
                from utils.threaded_camera import ThreadedCamera
                self.camera = ThreadedCamera(device_id, width, height, fps)
                self.logger.info(f"Threaded camera initialized: {device_id}")
                return
            except Exception as e:
                self.logger.warning(f"Failed to use threaded camera: {e}, falling back to standard")
        
        # Fallback to standard camera
        self.camera = cv2.VideoCapture(device_id)
        
        if not self.camera.isOpened():
            self.logger.error(f"Failed to open camera {device_id}")
            raise RuntimeError(f"Cannot open camera {device_id}")
        
        # Set camera properties
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        
        self.logger.info(f"Camera initialized: {device_id}")
    
    def _setup_eye_gesture_callbacks(self):
        """Setup callbacks for eye gestures."""
        # Single blink -> single click
        self.eye_tracker.register_gesture_callback(
            EyeGesture.SINGLE_BLINK,
            lambda: self._on_eye_gesture(EyeGesture.SINGLE_BLINK)
        )
        
        # Double blink -> double click / open
        self.eye_tracker.register_gesture_callback(
            EyeGesture.DOUBLE_BLINK,
            lambda: self._on_eye_gesture(EyeGesture.DOUBLE_BLINK)
        )
        
        # Long blink -> right click
        self.eye_tracker.register_gesture_callback(
            EyeGesture.LONG_BLINK,
            lambda: self._on_eye_gesture(EyeGesture.LONG_BLINK)
        )
        
        # Directional gazes -> scroll
        self.eye_tracker.register_gesture_callback(
            EyeGesture.LOOK_UP,
            lambda: self._on_eye_gesture(EyeGesture.LOOK_UP)
        )
        
        self.eye_tracker.register_gesture_callback(
            EyeGesture.LOOK_DOWN,
            lambda: self._on_eye_gesture(EyeGesture.LOOK_DOWN)
        )
    
    def _setup_hand_gesture_callbacks(self):
        """Setup callbacks for hand gestures."""
        if not self.hand_gesture_recognizer:
            return
        
        # Define gesture action mapping
        gesture_actions = {
            HandGesture.FIST: lambda: self._on_hand_gesture(HandGesture.FIST),
            HandGesture.OPEN_PALM: lambda: self._on_hand_gesture(HandGesture.OPEN_PALM),
            HandGesture.THUMBS_UP: lambda: self._on_hand_gesture(HandGesture.THUMBS_UP),
            HandGesture.THUMBS_DOWN: lambda: self._on_hand_gesture(HandGesture.THUMBS_DOWN),
            HandGesture.PEACE: lambda: self._on_hand_gesture(HandGesture.PEACE),
            HandGesture.SWIPE_UP: lambda: self._on_hand_gesture(HandGesture.SWIPE_UP),
            HandGesture.SWIPE_DOWN: lambda: self._on_hand_gesture(HandGesture.SWIPE_DOWN),
        }
        
        # Register callbacks
        for gesture, callback in gesture_actions.items():
            self.hand_gesture_recognizer.register_callback(gesture, callback)
    
    def _on_eye_gesture(self, gesture: EyeGesture):
        """Handle eye gesture detection."""
        self.last_eye_gesture = gesture
        
        if gesture == EyeGesture.SINGLE_BLINK:
            # Single click
            if self.mouse_controller.is_enabled:
                self.mouse_controller.click()
                self.logger.info("Eye gesture: Single blink -> Click")
        
        elif gesture == EyeGesture.DOUBLE_BLINK:
            # Double click / Open
            if self.mouse_controller.is_enabled:
                self.mouse_controller.double_click()
                self.logger.info("Eye gesture: Double blink -> Double click")
        
        elif gesture == EyeGesture.LONG_BLINK:
            # Right click
            if self.mouse_controller.is_enabled:
                self.mouse_controller.right_click()
                self.logger.info("Eye gesture: Long blink -> Right click")
        
        elif gesture == EyeGesture.LOOK_UP:
            # Scroll up
            if self.mouse_controller.is_enabled:
                self.mouse_controller.scroll(3)
                self.logger.debug("Eye gesture: Look up -> Scroll up")
        
        elif gesture == EyeGesture.LOOK_DOWN:
            # Scroll down
            if self.mouse_controller.is_enabled:
                self.mouse_controller.scroll(-3)
                self.logger.debug("Eye gesture: Look down -> Scroll down")
    
    def _on_hand_gesture(self, gesture: HandGesture):
        """Handle hand gesture detection."""
        self.last_hand_gesture = gesture
        
        # Define gesture action mapping
        gesture_actions = {
            HandGesture.FIST: lambda: (self.mouse_controller.click(), "Fist -> Click"),
            HandGesture.OPEN_PALM: lambda: (self.mouse_controller.right_click(), "Open palm -> Right click"),
            HandGesture.THUMBS_UP: lambda: (self.mouse_controller.scroll(5), None),  # No log for frequent actions
            HandGesture.THUMBS_DOWN: lambda: (self.mouse_controller.scroll(-5), None),
            HandGesture.PEACE: lambda: (self.mouse_controller.double_click(), "Peace -> Double click"),
            HandGesture.SWIPE_UP: lambda: (self.mouse_controller.scroll(10), "Swipe up -> Page up"),
            HandGesture.SWIPE_DOWN: lambda: (self.mouse_controller.scroll(-10), "Swipe down -> Page down"),
        }
        
        # Execute action if mapped
        if gesture in gesture_actions:
            result = gesture_actions[gesture]()
            if result and result[1]:  # Log if message provided
                self.logger.info(f"Hand gesture: {result[1]}")
    
    def start_calibration(self):
        """Start calibration process."""
        self.is_calibrating = True
        self.calibration.start()
        self.mouse_controller.disable()
        self.logger.info("Calibration started")
    
    def handle_keyboard_input(self, key: int) -> bool:
        """
        Handle keyboard input.
        
        Args:
            key: Key code from cv2.waitKey()
            
        Returns:
            True if application should continue, False to quit
        """
        if key == ord('q') or key == 27:  # 'q' or ESC
            return False
        elif key == ord('c'):  # Start calibration
            self.start_calibration()
        elif key == ord('k'):  # Toggle keyboard
            self.virtual_keyboard.toggle()
            self.logger.info(f"Virtual keyboard: {'shown' if self.virtual_keyboard.is_visible else 'hidden'}")
        elif key == ord('m'):  # Toggle mouse control
            self.mouse_controller.toggle_control()
            self.logger.info(f"Mouse control: {'enabled' if self.mouse_controller.is_enabled else 'disabled'}")
        elif key == ord('h'):  # Toggle UI
            self.show_ui = not self.show_ui
        elif key == ord('g'):  # Toggle hand gestures
            if self.hand_gesture_recognizer:
                self.hand_gesture_recognizer.toggle()
                status = "enabled" if self.hand_gesture_recognizer.is_enabled else "disabled"
                self.logger.info(f"Hand gestures: {status}")
        elif key == ord('r'):  # Reset calibration
            self.calibration.reset()
            self.eye_tracker.reset_calibration()
            self.logger.info("Calibration reset")
        elif key == ord(' '):  # Manual click
            self.mouse_controller.click()
        
        return True
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a single frame."""
        self.perf_logger.start_timer("frame")
        self.frame_count += 1  # Increment frame counter
        
        # Track eyes
        processed_frame, eye_data = self.eye_tracker.process_frame(frame)
        
        if processed_frame is None:
            return frame
        
        # Get gaze information
        gaze_ratio = None
        if eye_data and eye_data.get('gaze_ratio'):
            gaze_ratio = self.eye_tracker.get_smoothed_gaze(eye_data['gaze_ratio'])
        
        # Detect eye gestures (only when not calibrating and eye gestures enabled)
        if not self.is_calibrating and eye_data and self.eye_gesture_enabled:
            eye_gesture = self.eye_tracker.detect_eye_gesture(eye_data)
            # Gesture callbacks handle the actions
        
        # Handle calibration
        if self.is_calibrating:
            if self.calibration.is_active:
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
                        
                        self.is_calibrating = False
                        self.mouse_controller.enable()
                        self.logger.info("Calibration completed")
                
                # Draw calibration UI
                current_point = self.calibration.get_current_point()
                if current_point:
                    # Create fullscreen calibration display
                    h, w = processed_frame.shape[:2]
                    screen_w = self.calibration.screen_width
                    screen_h = self.calibration.screen_height
                    
                    cal_frame = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
                    self.calibration.draw_calibration_point(cal_frame, current_point.screen_pos)
                    self.calibration.draw_progress(cal_frame)
                    
                    # Resize and overlay on video feed
                    cal_frame_resized = cv2.resize(cal_frame, (w, h))
                    processed_frame = cv2.addWeighted(processed_frame, 0.3, cal_frame_resized, 0.7, 0)
        else:
            # Normal operation - control mouse
            if gaze_ratio and self.mouse_controller.is_enabled:
                # Convert gaze to screen position
                screen_pos = self.eye_tracker.gaze_to_screen_position(
                    gaze_ratio,
                    self.calibration.screen_width,
                    self.calibration.screen_height
                )
                
                if screen_pos:
                    # Move cursor
                    self.mouse_controller.move_cursor(screen_pos)
                    
                    # Handle clicking based on mode
                    if self.mouse_controller.click_mode == ClickMode.DWELL:
                        self.mouse_controller.check_dwell_click(screen_pos)
                    # Note: Blink clicking now handled by gesture system
                    
                    # Draw gaze indicator on screen
                    if self.show_ui:
                        h, w = processed_frame.shape[:2]
                        # Scale screen position to frame
                        frame_x = int(screen_pos[0] * w / self.calibration.screen_width)
                        frame_y = int(screen_pos[1] * h / self.calibration.screen_height)
                        
                        # Draw crosshair
                        cv2.circle(processed_frame, (frame_x, frame_y), 10, (0, 255, 0), 2)
                        cv2.line(processed_frame, (frame_x - 15, frame_y), (frame_x + 15, frame_y), (0, 255, 0), 2)
                        cv2.line(processed_frame, (frame_x, frame_y - 15), (frame_x, frame_y + 15), (0, 255, 0), 2)
                        
                        # Draw dwell progress
                        if self.mouse_controller.click_mode == ClickMode.DWELL:
                            progress = self.mouse_controller.get_dwell_progress()
                            if progress > 0:
                                radius = int(20 + progress * 20)
                                cv2.circle(processed_frame, (frame_x, frame_y), radius, (0, 255, 0), 2)
            
            # Handle virtual keyboard
            if self.virtual_keyboard.is_visible and gaze_ratio:
                screen_pos = self.eye_tracker.gaze_to_screen_position(
                    gaze_ratio,
                    self.calibration.screen_width,
                    self.calibration.screen_height
                )
                self.virtual_keyboard.update(screen_pos, processed_frame)
        
        # Process hand gestures (skip frames for performance)
        if self.hand_gesture_recognizer and self.hand_gesture_recognizer.is_enabled:
            if self.frame_count % self.hand_gesture_skip_frames == 0:
                processed_frame, hand_gesture = self.hand_gesture_recognizer.process_frame(processed_frame)
                # Gesture callbacks handle the actions
        
        # Draw UI
        if self.show_ui:
            self.draw_ui(processed_frame)
        
        self.perf_logger.stop_timer("frame")
        
        return processed_frame
    
    def draw_ui(self, frame: np.ndarray):
        """Draw UI elements on frame."""
        h, w = frame.shape[:2]
        
        # Draw FPS
        self.fps = self.perf_logger.get_fps("frame")
        fps_text = f"FPS: {self.fps:.1f}"
        cv2.putText(frame, fps_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw status
        status_y = 60
        if self.mouse_controller.is_enabled:
            status = "Mouse: ON"
            color = (0, 255, 0)
        else:
            status = "Mouse: OFF"
            color = (0, 0, 255)
        cv2.putText(frame, status, (10, status_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Draw calibration status
        if self.eye_tracker.is_calibrated:
            cal_status = "Calibrated"
            cal_color = (0, 255, 0)
        else:
            cal_status = "Not Calibrated"
            cal_color = (0, 0, 255)
        cv2.putText(frame, cal_status, (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, cal_color, 2)
        
        # Draw gesture mode
        mode_text = f"Mode: {self.gesture_mode_names[self.gesture_mode]}"
        cv2.putText(frame, mode_text, (10, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)
        
        # Draw last gestures
        gesture_y = 150
        if self.last_eye_gesture:
            gesture_text = f"Eye: {self.last_eye_gesture.value}"
            cv2.putText(frame, gesture_text, (10, gesture_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        if self.last_hand_gesture:
            gesture_text = f"Hand: {self.last_hand_gesture.value}"
            cv2.putText(frame, gesture_text, (10, gesture_y + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Draw help text
        help_y = h - 120
        help_texts = [
            "Q/ESC: Quit",
            "C: Calibrate",
            "K: Keyboard",
            "M: Toggle Mouse",
            "G: Toggle Hand Gestures",
            "H: Hide UI"
        ]
        for i, text in enumerate(help_texts):
            cv2.putText(frame, text, (10, help_y + i * 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def run(self):
        """Run main application loop."""
        self.is_running = True
        self.logger.info("Starting eye tracking application")
        
        # Create window with always-on-top property
        window_name = "Eye Tracking System"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)  # Always on top
        cv2.resizeWindow(window_name, 320, 240)  # Smaller overlay window
        
        try:
            while self.is_running:
                # Read frame
                ret, frame = self.camera.read()
                if not ret:
                    self.logger.error("Failed to read frame from camera")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Display
                cv2.imshow("Eye Tracking System", processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key != 255:
                    if not self.handle_keyboard_input(key):
                        break
                
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}", exc_info=True)
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        self.logger.info("Cleaning up...")
        
        self.is_running = False
        
        if self.camera:
            self.camera.release()
        
        if self.eye_tracker:
            self.eye_tracker.release()
        
        if self.hand_gesture_recognizer:
            self.hand_gesture_recognizer.release()
        
        cv2.destroyAllWindows()
        
        self.logger.info("Application closed")


def show_gesture_menu():
    """Display gesture selection menu at startup."""
    print("\n" + "="*60)
    print("   EYE TRACKING SYSTEM FOR PEOPLE WITH DISABILITIES")
    print("="*60)
    print("\nSelect gesture control mode:\n")
    print("  [1] Eye Gestures Only")
    print("      - Single blink → Click")
    print("      - Double blink → Double click")
    print("      - Long blink → Right click\n")
    print("  [2] Hand Gestures Only")
    print("      - Fist → Click")
    print("      - Open palm → Right click")
    print("      - Swipe up/down → Scroll\n")
    print("  [3] Both Eye and Hand Gestures")
    print("      - Use all gesture controls\n")
    print("="*60)
    
    while True:
        try:
            choice = input("\nEnter your choice (1/2/3): ").strip()
            if choice in ['1', '2', '3']:
                return int(choice)
            print("Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Eye Tracking System for People with Disabilities")
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--mode', type=int, choices=[1, 2, 3], 
                       help='Gesture mode: 1=Eye only, 2=Hand only, 3=Both (skips menu)')
    args = parser.parse_args()
    
    # Show menu if mode not specified via command line
    if args.mode:
        gesture_mode = args.mode
    else:
        gesture_mode = show_gesture_menu()
    
    # Display selected mode
    mode_names = {1: "Eye Gestures Only", 2: "Hand Gestures Only", 3: "Both Eye and Hand Gestures"}
    print(f"\n✓ Selected: {mode_names[gesture_mode]}")
    print("Starting application...\n")
    
    try:
        app = EyeTrackingApp(config_file=args.config, gesture_mode=gesture_mode)
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

