"""
Hand Gesture Recognition Module
Recognizes hand gestures using MediaPipe Hands for enhanced control.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional, List, Dict
from enum import Enum
import time


class HandGesture(Enum):
    """Types of hand gestures."""
    FIST = "fist"
    OPEN_PALM = "open_palm"
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    PEACE = "peace"
    POINTING = "pointing"
    OK_SIGN = "ok_sign"
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    SWIPE_UP = "swipe_up"
    SWIPE_DOWN = "swipe_down"


class HandGestureRecognizer:
    """Recognizes hand gestures for system control."""
    
    def __init__(self,
                 max_hands: int = 1,
                 min_detection_confidence: float = 0.7,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize Hand Gesture Recognizer.
        
        Args:
            max_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Gesture state
        self.last_gesture = None
        self.gesture_start_time = None
        self.gesture_cooldown = 0.5  # seconds between gestures
        self.last_gesture_time = 0
        
        # Hand position history for swipe detection
        self.hand_positions = []
        self.position_history_size = 10
        
        # Gesture callbacks
        self.gesture_callbacks = {}
        
        # Enable/disable flag
        self.is_enabled = True
        
        # Configurable swipe threshold
        self.swipe_threshold = 100  # pixels
    
    def register_callback(self, gesture: HandGesture, callback):
        """Register a callback for a specific gesture."""
        self.gesture_callbacks[gesture] = callback
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[HandGesture]]:
        """
        Process frame to detect hand gestures.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Tuple of (processed_frame, detected_gesture)
        """
        if not self.is_enabled or frame is None:
            return frame, None
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        detected_gesture = None
        current_time = time.time()
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Detect gesture from landmarks
                h, w = frame.shape[:2]
                detected_gesture = self._recognize_gesture(hand_landmarks, w, h, current_time)
                
                # Track hand position for swipe detection
                palm_center = self._get_palm_center(hand_landmarks, w, h)
                if palm_center:
                    self.hand_positions.append(palm_center)
                    if len(self.hand_positions) > self.position_history_size:
                        self.hand_positions.pop(0)
                    
                    # Check for swipe gestures
                    swipe_gesture = self._detect_swipe(current_time)
                    if swipe_gesture:
                        detected_gesture = swipe_gesture
        else:
            # Clear position history when no hand detected
            if len(self.hand_positions) > 0:
                self.hand_positions.clear()
        
        # Trigger callback if gesture detected
        if detected_gesture and detected_gesture in self.gesture_callbacks:
            if current_time - self.last_gesture_time > self.gesture_cooldown:
                self.gesture_callbacks[detected_gesture]()
                self.last_gesture_time = current_time
        
        return frame, detected_gesture
    
    def _get_palm_center(self, hand_landmarks, w: int, h: int) -> Optional[Tuple[int, int]]:
        """Get the center of palm."""
        if not hand_landmarks:
            return None
        
        # Use wrist and middle finger base as reference
        wrist = hand_landmarks.landmark[0]
        middle_base = hand_landmarks.landmark[9]
        
        center_x = int((wrist.x + middle_base.x) / 2 * w)
        center_y = int((wrist.y + middle_base.y) / 2 * h)
        
        return (center_x, center_y)
    
    def _recognize_gesture(self, hand_landmarks, w: int, h: int, 
                          current_time: float) -> Optional[HandGesture]:
        """
        Recognize static hand gesture from landmarks.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            w: Frame width
            h: Frame height
            current_time: Current timestamp
            
        Returns:
            Detected gesture or None
        """
        # Get finger states (extended or folded)
        fingers_extended = self._get_fingers_extended(hand_landmarks)
        
        # Count extended fingers
        extended_count = sum(fingers_extended)
        
        # Check cooldown
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
        
        # Recognize gestures based on finger states
        # Fist (no fingers extended)
        if extended_count == 0:
            return HandGesture.FIST
        
        # Open palm (all fingers extended)
        elif extended_count == 5:
            return HandGesture.OPEN_PALM
        
        # Thumbs up (only thumb extended)
        elif extended_count == 1 and fingers_extended[0]:
            # Check if thumb is pointing up
            thumb_tip = hand_landmarks.landmark[4]
            wrist = hand_landmarks.landmark[0]
            if thumb_tip.y < wrist.y:  # Thumb is above wrist
                return HandGesture.THUMBS_UP
            else:
                return HandGesture.THUMBS_DOWN
        
        # Pointing (only index finger extended)
        elif extended_count == 1 and fingers_extended[1]:
            return HandGesture.POINTING
        
        # Peace sign (index and middle fingers extended)
        elif extended_count == 2 and fingers_extended[1] and fingers_extended[2]:
            return HandGesture.PEACE
        
        # OK sign (thumb and index forming circle, others extended)
        elif extended_count >= 3:
            # Check if thumb and index are close (forming circle)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            
            distance = np.sqrt((thumb_tip.x - index_tip.x)**2 + 
                             (thumb_tip.y - index_tip.y)**2)
            
            if distance < 0.05:  # Threshold for OK sign
                return HandGesture.OK_SIGN
        
        return None
    
    def _get_fingers_extended(self, hand_landmarks) -> List[bool]:
        """
        Check which fingers are extended.
        
        Returns:
            List of 5 booleans [thumb, index, middle, ring, pinky]
        """
        # Finger tip and pip (proximal interphalangeal) landmark indices
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 6, 10, 14, 18]
        
        fingers_extended = []
        
        for i in range(5):
            tip = hand_landmarks.landmark[finger_tips[i]]
            pip = hand_landmarks.landmark[finger_pips[i]]
            
            # For thumb, check horizontal distance
            if i == 0:
                # Thumb extended if tip is further from palm center than pip
                wrist = hand_landmarks.landmark[0]
                tip_dist = abs(tip.x - wrist.x)
                pip_dist = abs(pip.x - wrist.x)
                fingers_extended.append(tip_dist > pip_dist)
            else:
                # Other fingers extended if tip is above pip
                fingers_extended.append(tip.y < pip.y)
        
        return fingers_extended
    
    def _detect_swipe(self, current_time: float) -> Optional[HandGesture]:
        """
        Detect swipe gestures from hand movement.
        
        Args:
            current_time: Current timestamp
            
        Returns:
            Detected swipe gesture or None
        """
        if len(self.hand_positions) < self.position_history_size:
            return None
        
        # Calculate movement vector
        start_pos = self.hand_positions[0]
        end_pos = self.hand_positions[-1]
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Calculate distance and direction
        distance = np.sqrt(dx**2 + dy**2)
        
        # Configurable threshold for swipe detection (pixels)
        # Note: This should be made configurable via config file in future
        swipe_threshold = getattr(self, 'swipe_threshold', 100)
        
        if distance < swipe_threshold:
            return None
        
        # Check trajectory smoothness to reduce false positives
        # Calculate consistency of movement direction
        consistent_movement = True
        if len(self.hand_positions) >= 3:
            # Check if intermediate points follow the same general direction
            mid_idx = len(self.hand_positions) // 2
            mid_pos = self.hand_positions[mid_idx]
            
            # Vector from start to mid
            mid_dx = mid_pos[0] - start_pos[0]
            mid_dy = mid_pos[1] - start_pos[1]
            
            # Check if mid point is roughly between start and end
            # If movement changed direction significantly, it's not a clean swipe
            dot_product = (mid_dx * dx + mid_dy * dy)
            if dot_product < 0:  # Movement changed direction
                consistent_movement = False
        
        if not consistent_movement:
            return None
        
        # Determine direction
        angle = np.arctan2(dy, dx) * 180 / np.pi
        
        # Horizontal swipes
        if -45 <= angle < 45:
            return HandGesture.SWIPE_RIGHT
        elif 135 <= angle or angle < -135:
            return HandGesture.SWIPE_LEFT
        # Vertical swipes
        elif 45 <= angle < 135:
            return HandGesture.SWIPE_DOWN
        elif -135 <= angle < -45:
            return HandGesture.SWIPE_UP
        
        return None
    
    def toggle(self):
        """Toggle hand gesture recognition on/off."""
        self.is_enabled = not self.is_enabled
    
    def enable(self):
        """Enable hand gesture recognition."""
        self.is_enabled = True
    
    def disable(self):
        """Disable hand gesture recognition."""
        self.is_enabled = False
    
    def release(self):
        """Release resources."""
        if hasattr(self, 'hands'):
            self.hands.close()
