"""
Gesture Manager Module
Manages eye and hand gestures for enhanced control.
"""

import time
import numpy as np
from typing import Optional, Tuple, Dict, List
from enum import Enum


class EyeGesture(Enum):
    """Types of eye gestures."""
    SINGLE_BLINK = "single_blink"
    DOUBLE_BLINK = "double_blink"
    LOOK_LEFT = "look_left"
    LOOK_RIGHT = "look_right"
    LOOK_UP = "look_up"
    LOOK_DOWN = "look_down"
    LONG_BLINK = "long_blink"


class GestureManager:
    """Manages detection and handling of eye gestures."""
    
    def __init__(self,
                 blink_threshold: float = 0.25,
                 double_blink_interval: float = 0.5,
                 long_blink_duration: float = 0.8,
                 gaze_direction_threshold: float = 0.15):
        """
        Initialize Gesture Manager.
        
        Args:
            blink_threshold: EAR threshold for blink detection
            double_blink_interval: Max time between blinks for double blink (seconds)
            long_blink_duration: Minimum duration for long blink (seconds)
            gaze_direction_threshold: Threshold for directional gaze detection
        """
        self.blink_threshold = blink_threshold
        self.double_blink_interval = double_blink_interval
        self.long_blink_duration = long_blink_duration
        self.gaze_direction_threshold = gaze_direction_threshold
        
        # Blink detection state
        self.is_currently_blinking = False
        self.blink_start_time = None
        self.last_blink_end_time = None
        self.last_blink_duration = 0
        self.blink_count = 0
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.3  # Cooldown between gestures
        
        # Gaze direction history
        self.gaze_history = []
        self.gaze_history_size = 10
        
        # Gesture callbacks
        self.gesture_callbacks = {}
        
    def register_callback(self, gesture: EyeGesture, callback):
        """Register a callback for a specific gesture."""
        self.gesture_callbacks[gesture] = callback
    
    def detect_blink(self, ear: float, current_time: float) -> Optional[EyeGesture]:
        """
        Detect blink gestures (single, double, long).
        
        Args:
            ear: Eye Aspect Ratio
            current_time: Current timestamp
            
        Returns:
            Detected gesture type or None
        """
        is_eyes_closed = ear < self.blink_threshold
        detected_gesture = None
        
        if is_eyes_closed and not self.is_currently_blinking:
            # Blink started
            self.is_currently_blinking = True
            self.blink_start_time = current_time
            
        elif not is_eyes_closed and self.is_currently_blinking:
            # Blink ended
            self.is_currently_blinking = False
            blink_duration = current_time - self.blink_start_time
            self.last_blink_duration = blink_duration
            
            # Check for long blink
            if blink_duration >= self.long_blink_duration:
                detected_gesture = EyeGesture.LONG_BLINK
                self.blink_count = 0  # Reset count on long blink
                self.last_gesture_time = current_time
            else:
                # Normal blink - check for double blink
                if self.last_blink_end_time is not None:
                    time_since_last_blink = current_time - self.last_blink_end_time
                    
                    if time_since_last_blink <= self.double_blink_interval:
                        # Double blink detected
                        detected_gesture = EyeGesture.DOUBLE_BLINK
                        self.blink_count = 0
                        self.last_gesture_time = current_time
                    else:
                        # Single blink
                        if current_time - self.last_gesture_time > self.gesture_cooldown:
                            detected_gesture = EyeGesture.SINGLE_BLINK
                            self.last_gesture_time = current_time
                else:
                    # First blink
                    if current_time - self.last_gesture_time > self.gesture_cooldown:
                        detected_gesture = EyeGesture.SINGLE_BLINK
                        self.last_gesture_time = current_time
                
                self.last_blink_end_time = current_time
        
        # Trigger callback if gesture detected
        if detected_gesture and detected_gesture in self.gesture_callbacks:
            self.gesture_callbacks[detected_gesture]()
        
        return detected_gesture
    
    def detect_gaze_direction(self, gaze_ratio: Tuple[float, float], 
                             current_time: float) -> Optional[EyeGesture]:
        """
        Detect directional gaze gestures.
        
        Args:
            gaze_ratio: (horizontal, vertical) gaze ratios (0-1)
            current_time: Current timestamp
            
        Returns:
            Detected gesture type or None
        """
        if gaze_ratio is None:
            return None
        
        # Add to history
        self.gaze_history.append(gaze_ratio)
        if len(self.gaze_history) > self.gaze_history_size:
            self.gaze_history.pop(0)
        
        # Need enough history to detect
        if len(self.gaze_history) < self.gaze_history_size:
            return None
        
        # Calculate average gaze position
        avg_h = np.mean([g[0] for g in self.gaze_history])
        avg_v = np.mean([g[1] for g in self.gaze_history])
        
        detected_gesture = None
        
        # Check cooldown
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
        
        # Detect extreme gaze directions (sustained look)
        # Horizontal direction (left/right)
        if avg_h < (0.5 - self.gaze_direction_threshold):
            detected_gesture = EyeGesture.LOOK_LEFT
        elif avg_h > (0.5 + self.gaze_direction_threshold):
            detected_gesture = EyeGesture.LOOK_RIGHT
        
        # Vertical direction (up/down) - only if no horizontal gesture
        if detected_gesture is None:
            if avg_v < (0.5 - self.gaze_direction_threshold):
                detected_gesture = EyeGesture.LOOK_UP
            elif avg_v > (0.5 + self.gaze_direction_threshold):
                detected_gesture = EyeGesture.LOOK_DOWN
        
        # Trigger callback if gesture detected and update time
        if detected_gesture and detected_gesture in self.gesture_callbacks:
            self.gesture_callbacks[detected_gesture]()
            self.last_gesture_time = current_time
            return detected_gesture
        
        return None
    
    def get_current_blink_duration(self, current_time: float) -> float:
        """Get duration of current blink if blinking."""
        if self.is_currently_blinking and self.blink_start_time:
            return current_time - self.blink_start_time
        return 0.0
    
    def reset(self):
        """Reset gesture detection state."""
        self.is_currently_blinking = False
        self.blink_start_time = None
        self.last_blink_end_time = None
        self.last_blink_duration = 0
        self.blink_count = 0
        self.gaze_history.clear()
