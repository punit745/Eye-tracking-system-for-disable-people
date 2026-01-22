"""
Eye Tracker Module
Core module for detecting and tracking eye movements using MediaPipe and OpenCV.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional, List
import time
from core.gesture_manager import GestureManager, EyeGesture


class EyeTracker:
    """Main class for eye tracking using MediaPipe Face Mesh."""
    
    def __init__(self, 
                 max_faces=1, 
                 refine_landmarks=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        """
        Initialize the Eye Tracker.
        
        Args:
            max_faces: Maximum number of faces to detect
            refine_landmarks: Whether to refine eye and iris landmarks
            min_detection_confidence: Minimum confidence for face detection
            min_tracking_confidence: Minimum confidence for face tracking
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_faces,
            refine_landmarks=refine_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Eye landmark indices for MediaPipe Face Mesh
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        
        # Iris landmark indices
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]
        
        # Calibration data
        self.calibration_points = []
        self.is_calibrated = False
        
        # Smoothing
        self.gaze_history = []
        self.smoothing_window = 5
        
        # Gesture manager for advanced gestures
        self.gesture_manager = GestureManager(
            blink_threshold=0.25,
            double_blink_interval=0.5,
            long_blink_duration=0.8,
            gaze_direction_threshold=0.15
        )
        
    def process_frame(self, frame: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[dict]]:
        """
        Process a single frame to detect eye positions.
        
        Args:
            frame: Input frame from webcam
            
        Returns:
            Tuple of (processed_frame, eye_data)
        """
        if frame is None:
            return None, None
            
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        eye_data = None
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            h, w = frame.shape[:2]
            
            # Get eye landmarks
            left_eye_points = self._get_landmarks(face_landmarks, self.LEFT_EYE, w, h)
            right_eye_points = self._get_landmarks(face_landmarks, self.RIGHT_EYE, w, h)
            
            # Get iris landmarks
            left_iris = self._get_landmarks(face_landmarks, self.LEFT_IRIS, w, h)
            right_iris = self._get_landmarks(face_landmarks, self.RIGHT_IRIS, w, h)
            
            # Calculate iris centers
            left_iris_center = np.mean(left_iris, axis=0).astype(int) if len(left_iris) > 0 else None
            right_iris_center = np.mean(right_iris, axis=0).astype(int) if len(right_iris) > 0 else None
            
            # Calculate gaze ratio (normalized position of iris within eye)
            left_gaze_ratio = self._calculate_gaze_ratio(left_eye_points, left_iris_center)
            right_gaze_ratio = self._calculate_gaze_ratio(right_eye_points, right_iris_center)
            
            # Average gaze ratio
            avg_gaze_ratio = None
            if left_gaze_ratio is not None and right_gaze_ratio is not None:
                avg_gaze_ratio = ((left_gaze_ratio[0] + right_gaze_ratio[0]) / 2,
                                 (left_gaze_ratio[1] + right_gaze_ratio[1]) / 2)
            
            # Calculate Eye Aspect Ratio for both eyes
            left_ear = self._calculate_ear(left_eye_points)
            right_ear = self._calculate_ear(right_eye_points)
            avg_ear = (left_ear + right_ear) / 2.0
            
            eye_data = {
                'left_eye': left_eye_points,
                'right_eye': right_eye_points,
                'left_iris': left_iris_center,
                'right_iris': right_iris_center,
                'left_gaze_ratio': left_gaze_ratio,
                'right_gaze_ratio': right_gaze_ratio,
                'gaze_ratio': avg_gaze_ratio,
                'face_landmarks': face_landmarks,
                'left_ear': left_ear,
                'right_ear': right_ear,
                'avg_ear': avg_ear
            }
            
            # Draw visualizations
            self._draw_eyes(frame, eye_data)
            
        return frame, eye_data
    
    def _get_landmarks(self, face_landmarks, indices: List[int], w: int, h: int) -> np.ndarray:
        """Extract landmark coordinates."""
        points = []
        for idx in indices:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            points.append([x, y])
        return np.array(points)
    
    def _calculate_gaze_ratio(self, eye_points: np.ndarray, iris_center: Optional[np.ndarray]) -> Optional[Tuple[float, float]]:
        """
        Calculate the gaze ratio (position of iris relative to eye).
        Returns (horizontal_ratio, vertical_ratio) where 0.5 is center.
        """
        if iris_center is None or len(eye_points) == 0:
            return None
            
        # Get eye bounding box
        eye_left = np.min(eye_points[:, 0])
        eye_right = np.max(eye_points[:, 0])
        eye_top = np.min(eye_points[:, 1])
        eye_bottom = np.max(eye_points[:, 1])
        
        eye_width = eye_right - eye_left
        eye_height = eye_bottom - eye_top
        
        if eye_width == 0 or eye_height == 0:
            return None
        
        # Calculate normalized position
        horizontal_ratio = (iris_center[0] - eye_left) / eye_width
        vertical_ratio = (iris_center[1] - eye_top) / eye_height
        
        # Clamp values
        horizontal_ratio = np.clip(horizontal_ratio, 0.0, 1.0)
        vertical_ratio = np.clip(vertical_ratio, 0.0, 1.0)
        
        return (horizontal_ratio, vertical_ratio)
    
    def _draw_eyes(self, frame: np.ndarray, eye_data: dict):
        """Draw eye tracking visualizations on frame."""
        # Draw eye contours
        if eye_data['left_eye'] is not None:
            cv2.polylines(frame, [eye_data['left_eye']], True, (0, 255, 0), 1)
        if eye_data['right_eye'] is not None:
            cv2.polylines(frame, [eye_data['right_eye']], True, (0, 255, 0), 1)
        
        # Draw iris centers
        if eye_data['left_iris'] is not None:
            cv2.circle(frame, tuple(eye_data['left_iris']), 2, (255, 0, 0), -1)
        if eye_data['right_iris'] is not None:
            cv2.circle(frame, tuple(eye_data['right_iris']), 2, (255, 0, 0), -1)
    
    def get_smoothed_gaze(self, gaze_ratio: Optional[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """Apply smoothing to gaze position."""
        if gaze_ratio is None:
            return None
        
        self.gaze_history.append(gaze_ratio)
        if len(self.gaze_history) > self.smoothing_window:
            self.gaze_history.pop(0)
        
        # Calculate moving average
        avg_x = np.mean([g[0] for g in self.gaze_history])
        avg_y = np.mean([g[1] for g in self.gaze_history])
        
        return (avg_x, avg_y)
    
    def add_calibration_point(self, screen_pos: Tuple[int, int], gaze_ratio: Tuple[float, float]):
        """Add a calibration point."""
        self.calibration_points.append({
            'screen': screen_pos,
            'gaze': gaze_ratio
        })
    
    def calibrate(self):
        """Complete calibration process."""
        if len(self.calibration_points) >= 4:  # Minimum 4 points for calibration
            self.is_calibrated = True
            return True
        return False
    
    def reset_calibration(self):
        """Reset calibration data."""
        self.calibration_points = []
        self.is_calibrated = False
    
    def gaze_to_screen_position(self, gaze_ratio: Tuple[float, float], 
                                screen_width: int, screen_height: int) -> Tuple[int, int]:
        """
        Convert gaze ratio to screen coordinates.
        
        Args:
            gaze_ratio: (horizontal, vertical) ratios from 0 to 1
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            
        Returns:
            (x, y) screen coordinates
        """
        if gaze_ratio is None:
            return None
        
        # Simple linear mapping (can be improved with calibration)
        x = int(gaze_ratio[0] * screen_width)
        y = int(gaze_ratio[1] * screen_height)
        
        # Apply calibration if available
        if self.is_calibrated and len(self.calibration_points) > 0:
            # Use weighted average based on distance to calibration points
            x, y = self._apply_calibration(gaze_ratio, screen_width, screen_height)
        
        return (x, y)
    
    def _apply_calibration(self, gaze_ratio: Tuple[float, float], 
                          screen_width: int, screen_height: int) -> Tuple[int, int]:
        """Apply calibration transformation."""
        # Simple weighted interpolation based on calibration points
        weights = []
        positions = []
        
        for point in self.calibration_points:
            # Calculate distance in gaze space
            dist = np.sqrt((gaze_ratio[0] - point['gaze'][0])**2 + 
                          (gaze_ratio[1] - point['gaze'][1])**2)
            
            if dist < 0.001:  # Very close, use this point directly
                return point['screen']
            
            weight = 1.0 / (dist + 0.1)  # Inverse distance weighting
            weights.append(weight)
            positions.append(point['screen'])
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight == 0:
            return (int(gaze_ratio[0] * screen_width), 
                   int(gaze_ratio[1] * screen_height))
        
        # Weighted average
        x = sum(w * p[0] for w, p in zip(weights, positions)) / total_weight
        y = sum(w * p[1] for w, p in zip(weights, positions)) / total_weight
        
        return (int(x), int(y))
    
    def detect_blink(self, eye_data: dict) -> bool:
        """
        Detect if user is blinking (simple version).
        Uses Eye Aspect Ratio (EAR) to detect blinks.
        """
        if not eye_data or 'avg_ear' not in eye_data:
            return False
        
        # Blink threshold (typically around 0.2-0.25)
        return eye_data['avg_ear'] < 0.25
    
    def detect_eye_gesture(self, eye_data: dict) -> Optional[EyeGesture]:
        """
        Detect advanced eye gestures (single blink, double blink, directional gaze).
        
        Args:
            eye_data: Dictionary containing eye tracking data
            
        Returns:
            Detected gesture or None
        """
        if not eye_data:
            return None
        
        current_time = time.time()
        detected_gesture = None
        
        # Detect blink-based gestures
        if 'avg_ear' in eye_data:
            blink_gesture = self.gesture_manager.detect_blink(
                eye_data['avg_ear'], 
                current_time
            )
            if blink_gesture:
                detected_gesture = blink_gesture
        
        # Detect gaze direction gestures
        if detected_gesture is None and 'gaze_ratio' in eye_data:
            gaze_ratio = eye_data['gaze_ratio']
            if gaze_ratio:
                direction_gesture = self.gesture_manager.detect_gaze_direction(
                    gaze_ratio,
                    current_time
                )
                if direction_gesture:
                    detected_gesture = direction_gesture
        
        return detected_gesture
    
    def _calculate_ear(self, eye_points: np.ndarray) -> float:
        """Calculate Eye Aspect Ratio (EAR)."""
        if len(eye_points) < 6:
            return 1.0
        
        # Vertical eye distances
        vertical_1 = np.linalg.norm(eye_points[1] - eye_points[5])
        vertical_2 = np.linalg.norm(eye_points[2] - eye_points[4])
        
        # Horizontal eye distance
        horizontal = np.linalg.norm(eye_points[0] - eye_points[3])
        
        if horizontal == 0:
            return 1.0
        
        # EAR formula
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        return ear
    
    def register_gesture_callback(self, gesture: EyeGesture, callback):
        """Register a callback for a specific eye gesture."""
        self.gesture_manager.register_callback(gesture, callback)
    
    def release(self):
        """Release resources."""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
