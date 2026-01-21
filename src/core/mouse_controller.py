"""
Mouse Controller Module
Controls mouse cursor based on eye tracking data.
"""

import pyautogui
import time
import numpy as np
from typing import Tuple, Optional
from enum import Enum


class ClickMode(Enum):
    """Different methods for triggering clicks."""
    DWELL = "dwell"  # Click by dwelling/looking at a point
    BLINK = "blink"  # Click by blinking
    GESTURE = "gesture"  # Click by specific eye gesture
    MANUAL = "manual"  # Manual keyboard trigger


class MouseController:
    """Controls mouse cursor and clicks based on eye tracking."""
    
    def __init__(self, 
                 sensitivity: float = 1.0,
                 smoothing: int = 5,
                 dwell_time: float = 1.5,
                 click_mode: ClickMode = ClickMode.DWELL):
        """
        Initialize Mouse Controller.
        
        Args:
            sensitivity: Movement sensitivity multiplier
            smoothing: Number of frames to smooth movement
            dwell_time: Time in seconds to dwell for click
            click_mode: Method for triggering clicks
        """
        # Disable PyAutoGUI failsafe (move mouse to corner to abort)
        pyautogui.FAILSAFE = True
        
        self.sensitivity = sensitivity
        self.smoothing = smoothing
        self.dwell_time = dwell_time
        self.click_mode = click_mode
        
        # Movement smoothing
        self.position_history = []
        
        # Dwell click tracking
        self.dwell_start_time = None
        self.dwell_position = None
        self.dwell_threshold = 50  # pixels
        
        # Blink detection
        self.blink_start_time = None
        self.last_blink_time = 0
        self.blink_cooldown = 0.5  # seconds between blinks
        
        # Get screen size
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Control flags
        self.is_enabled = True
        self.is_clicking_enabled = True
        
    def move_cursor(self, gaze_position: Tuple[int, int], smooth: bool = True):
        """
        Move mouse cursor to gaze position.
        
        Args:
            gaze_position: (x, y) screen coordinates
            smooth: Whether to apply smoothing
        """
        if not self.is_enabled or gaze_position is None:
            return
        
        x, y = gaze_position
        
        # Apply smoothing
        if smooth:
            self.position_history.append((x, y))
            if len(self.position_history) > self.smoothing:
                self.position_history.pop(0)
            
            # Calculate average position
            avg_x = int(np.mean([pos[0] for pos in self.position_history]))
            avg_y = int(np.mean([pos[1] for pos in self.position_history]))
            x, y = avg_x, avg_y
        
        # Apply sensitivity
        current_x, current_y = pyautogui.position()
        delta_x = int((x - current_x) * self.sensitivity)
        delta_y = int((y - current_y) * self.sensitivity)
        
        # Move cursor
        try:
            pyautogui.move(delta_x, delta_y, duration=0.01)
        except:
            pass  # Ignore any movement errors
    
    def check_dwell_click(self, current_position: Tuple[int, int]) -> bool:
        """
        Check if dwell click should be triggered.
        
        Args:
            current_position: Current gaze position
            
        Returns:
            True if click was triggered
        """
        if not self.is_clicking_enabled or current_position is None:
            return False
        
        # Start dwell if this is first frame or position changed significantly
        if self.dwell_position is None:
            self.dwell_position = current_position
            self.dwell_start_time = time.time()
            return False
        
        # Check if position is stable
        distance = np.sqrt(
            (current_position[0] - self.dwell_position[0])**2 + 
            (current_position[1] - self.dwell_position[1])**2
        )
        
        if distance > self.dwell_threshold:
            # Position moved, reset dwell
            self.dwell_position = current_position
            self.dwell_start_time = time.time()
            return False
        
        # Check if dwell time exceeded
        elapsed_time = time.time() - self.dwell_start_time
        if elapsed_time >= self.dwell_time:
            # Trigger click
            self.click()
            # Reset dwell
            self.dwell_position = None
            self.dwell_start_time = None
            return True
        
        return False
    
    def get_dwell_progress(self) -> float:
        """Get current dwell progress (0.0 to 1.0)."""
        if self.dwell_start_time is None:
            return 0.0
        
        elapsed_time = time.time() - self.dwell_start_time
        progress = min(elapsed_time / self.dwell_time, 1.0)
        return progress
    
    def check_blink_click(self, is_blinking: bool) -> bool:
        """
        Check if blink click should be triggered.
        
        Args:
            is_blinking: Whether user is currently blinking
            
        Returns:
            True if click was triggered
        """
        if not self.is_clicking_enabled:
            return False
        
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_blink_time < self.blink_cooldown:
            return False
        
        if is_blinking:
            if self.blink_start_time is None:
                self.blink_start_time = current_time
        else:
            if self.blink_start_time is not None:
                # Blink ended
                blink_duration = current_time - self.blink_start_time
                
                # Valid blink duration (0.1 to 0.5 seconds)
                if 0.1 <= blink_duration <= 0.5:
                    self.click()
                    self.last_blink_time = current_time
                    self.blink_start_time = None
                    return True
                
                self.blink_start_time = None
        
        return False
    
    def click(self, button: str = 'left'):
        """
        Perform mouse click.
        
        Args:
            button: 'left', 'right', or 'middle'
        """
        if not self.is_clicking_enabled:
            return
        
        try:
            pyautogui.click(button=button)
        except:
            pass
    
    def double_click(self):
        """Perform double click."""
        if not self.is_clicking_enabled:
            return
        
        try:
            pyautogui.doubleClick()
        except:
            pass
    
    def right_click(self):
        """Perform right click."""
        self.click(button='right')
    
    def drag_to(self, x: int, y: int, duration: float = 0.5):
        """
        Drag mouse to position.
        
        Args:
            x: Target x coordinate
            y: Target y coordinate
            duration: Time for drag operation
        """
        if not self.is_enabled:
            return
        
        try:
            pyautogui.drag(x, y, duration=duration, button='left')
        except:
            pass
    
    def scroll(self, amount: int):
        """
        Scroll mouse wheel.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
        """
        if not self.is_enabled:
            return
        
        try:
            pyautogui.scroll(amount)
        except:
            pass
    
    def set_sensitivity(self, sensitivity: float):
        """Set movement sensitivity."""
        self.sensitivity = max(0.1, min(sensitivity, 3.0))
    
    def set_dwell_time(self, dwell_time: float):
        """Set dwell time for click."""
        self.dwell_time = max(0.5, min(dwell_time, 5.0))
    
    def toggle_control(self):
        """Toggle cursor control on/off."""
        self.is_enabled = not self.is_enabled
        if not self.is_enabled:
            self.position_history.clear()
    
    def toggle_clicking(self):
        """Toggle clicking on/off."""
        self.is_clicking_enabled = not self.is_clicking_enabled
    
    def enable(self):
        """Enable mouse control."""
        self.is_enabled = True
    
    def disable(self):
        """Disable mouse control."""
        self.is_enabled = False
        self.position_history.clear()
    
    def reset(self):
        """Reset controller state."""
        self.position_history.clear()
        self.dwell_start_time = None
        self.dwell_position = None
        self.blink_start_time = None
