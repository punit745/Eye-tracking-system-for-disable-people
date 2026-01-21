"""
Calibration Module
Handles calibration process for eye tracking system.
"""

import cv2
import numpy as np
import time
from typing import Tuple, List, Optional, Callable
import pyautogui


class CalibrationPoint:
    """Represents a single calibration point."""
    
    def __init__(self, screen_pos: Tuple[int, int], index: int):
        self.screen_pos = screen_pos
        self.index = index
        self.gaze_samples = []
        self.is_complete = False
        
    def add_sample(self, gaze_ratio: Tuple[float, float]):
        """Add a gaze sample for this point."""
        self.gaze_samples.append(gaze_ratio)
        
    def get_average_gaze(self) -> Optional[Tuple[float, float]]:
        """Get average gaze ratio from all samples."""
        if not self.gaze_samples:
            return None
        
        avg_x = np.mean([s[0] for s in self.gaze_samples])
        avg_y = np.mean([s[1] for s in self.gaze_samples])
        return (avg_x, avg_y)
        
    def mark_complete(self):
        """Mark this point as complete."""
        self.is_complete = True


class Calibration:
    """Manages the calibration process."""
    
    def __init__(self, screen_width: int = None, screen_height: int = None):
        """
        Initialize calibration.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        if screen_width is None or screen_height is None:
            screen_width, screen_height = pyautogui.size()
            
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Calibration configuration
        self.num_points = 9  # 3x3 grid
        self.samples_per_point = 30  # Number of samples to collect per point
        self.dwell_time = 2.0  # Time to look at each point
        
        # State
        self.is_active = False
        self.current_point_index = 0
        self.points: List[CalibrationPoint] = []
        self.start_time = None
        
        # Results
        self.is_calibrated = False
        self.calibration_data = None
        
    def start(self):
        """Start calibration process."""
        self.is_active = True
        self.current_point_index = 0
        self.is_calibrated = False
        self.points = self._generate_calibration_points()
        self.start_time = time.time()
        
    def _generate_calibration_points(self) -> List[CalibrationPoint]:
        """Generate calibration points in a grid pattern."""
        points = []
        
        # Margins from screen edge (10% on each side)
        margin_x = int(self.screen_width * 0.1)
        margin_y = int(self.screen_height * 0.1)
        
        # Calculate grid positions
        if self.num_points == 9:
            # 3x3 grid
            positions = [
                (margin_x, margin_y),  # Top-left
                (self.screen_width // 2, margin_y),  # Top-center
                (self.screen_width - margin_x, margin_y),  # Top-right
                (margin_x, self.screen_height // 2),  # Middle-left
                (self.screen_width // 2, self.screen_height // 2),  # Center
                (self.screen_width - margin_x, self.screen_height // 2),  # Middle-right
                (margin_x, self.screen_height - margin_y),  # Bottom-left
                (self.screen_width // 2, self.screen_height - margin_y),  # Bottom-center
                (self.screen_width - margin_x, self.screen_height - margin_y),  # Bottom-right
            ]
        elif self.num_points == 5:
            # 5-point calibration
            positions = [
                (margin_x, margin_y),  # Top-left
                (self.screen_width - margin_x, margin_y),  # Top-right
                (self.screen_width // 2, self.screen_height // 2),  # Center
                (margin_x, self.screen_height - margin_y),  # Bottom-left
                (self.screen_width - margin_x, self.screen_height - margin_y),  # Bottom-right
            ]
        else:
            # Default to 4 corners
            positions = [
                (margin_x, margin_y),
                (self.screen_width - margin_x, margin_y),
                (margin_x, self.screen_height - margin_y),
                (self.screen_width - margin_x, self.screen_height - margin_y),
            ]
        
        for i, pos in enumerate(positions):
            points.append(CalibrationPoint(pos, i))
            
        return points
    
    def update(self, gaze_ratio: Optional[Tuple[float, float]]) -> bool:
        """
        Update calibration with current gaze data.
        
        Args:
            gaze_ratio: Current gaze ratio
            
        Returns:
            True if calibration is complete
        """
        if not self.is_active or gaze_ratio is None:
            return False
        
        current_point = self.points[self.current_point_index]
        
        # Collect samples
        if len(current_point.gaze_samples) < self.samples_per_point:
            current_point.add_sample(gaze_ratio)
            return False
        
        # Mark point as complete and move to next
        current_point.mark_complete()
        self.current_point_index += 1
        
        # Check if all points complete
        if self.current_point_index >= len(self.points):
            self._finish_calibration()
            return True
        
        return False
    
    def _finish_calibration(self):
        """Complete calibration and compute transformation."""
        self.is_active = False
        self.is_calibrated = True
        
        # Build calibration data
        self.calibration_data = []
        for point in self.points:
            avg_gaze = point.get_average_gaze()
            if avg_gaze:
                self.calibration_data.append({
                    'screen': point.screen_pos,
                    'gaze': avg_gaze
                })
    
    def get_current_point(self) -> Optional[CalibrationPoint]:
        """Get the current calibration point."""
        if not self.is_active or self.current_point_index >= len(self.points):
            return None
        return self.points[self.current_point_index]
    
    def get_progress(self) -> float:
        """Get calibration progress (0.0 to 1.0)."""
        if not self.is_active:
            return 1.0 if self.is_calibrated else 0.0
        
        current_point = self.get_current_point()
        if not current_point:
            return 1.0
        
        point_progress = len(current_point.gaze_samples) / self.samples_per_point
        overall_progress = (self.current_point_index + point_progress) / len(self.points)
        return overall_progress
    
    def draw_calibration_point(self, frame: np.ndarray, 
                               position: Tuple[int, int] = None,
                               color: Tuple[int, int, int] = (0, 255, 0),
                               size: int = 30) -> np.ndarray:
        """
        Draw calibration target on frame.
        
        Args:
            frame: Frame to draw on
            position: Position to draw (uses current point if None)
            color: RGB color
            size: Size of target
            
        Returns:
            Frame with calibration target drawn
        """
        if position is None:
            current_point = self.get_current_point()
            if not current_point:
                return frame
            position = current_point.screen_pos
        
        x, y = position
        
        # Draw outer circle
        cv2.circle(frame, (x, y), size, color, 2)
        # Draw inner circle
        cv2.circle(frame, (x, y), size // 3, color, -1)
        # Draw crosshair
        cv2.line(frame, (x - size, y), (x + size, y), color, 2)
        cv2.line(frame, (x, y - size), (x, y + size), color, 2)
        
        return frame
    
    def draw_progress(self, frame: np.ndarray) -> np.ndarray:
        """Draw calibration progress on frame."""
        if not self.is_active:
            return frame
        
        progress = self.get_progress()
        h, w = frame.shape[:2]
        
        # Progress bar
        bar_width = int(w * 0.6)
        bar_height = 30
        bar_x = (w - bar_width) // 2
        bar_y = h - 60
        
        # Background
        cv2.rectangle(frame, (bar_x, bar_y), 
                     (bar_x + bar_width, bar_y + bar_height),
                     (50, 50, 50), -1)
        
        # Progress
        progress_width = int(bar_width * progress)
        cv2.rectangle(frame, (bar_x, bar_y),
                     (bar_x + progress_width, bar_y + bar_height),
                     (0, 255, 0), -1)
        
        # Text
        text = f"Calibration: {int(progress * 100)}%"
        cv2.putText(frame, text, (bar_x, bar_y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Instructions
        instruction = "Look at the target and hold your gaze steady"
        text_size = cv2.getTextSize(instruction, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = (w - text_size[0]) // 2
        cv2.putText(frame, instruction, (text_x, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def reset(self):
        """Reset calibration."""
        self.is_active = False
        self.current_point_index = 0
        self.points = []
        self.is_calibrated = False
        self.calibration_data = None
    
    def get_calibration_data(self) -> Optional[List[dict]]:
        """Get calibration data."""
        return self.calibration_data if self.is_calibrated else None
    
    def load_calibration_data(self, data: List[dict]):
        """Load existing calibration data."""
        self.calibration_data = data
        self.is_calibrated = True
