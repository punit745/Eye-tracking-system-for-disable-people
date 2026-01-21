"""
Virtual Keyboard Module
Provides on-screen keyboard for eye-controlled text input.
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List, Callable
import pyautogui


class Key:
    """Represents a virtual key."""
    
    def __init__(self, char: str, rect: Tuple[int, int, int, int], color: Tuple[int, int, int] = (100, 100, 100)):
        """
        Initialize a key.
        
        Args:
            char: Character or label for the key
            rect: (x, y, width, height) rectangle
            color: RGB color for the key
        """
        self.char = char
        self.x, self.y, self.width, self.height = rect
        self.color = color
        self.hover_color = (150, 150, 150)
        self.active_color = (0, 255, 0)
        self.is_hovered = False
        self.hover_time = 0
        
    def contains_point(self, point: Tuple[int, int]) -> bool:
        """Check if point is within key bounds."""
        x, y = point
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def draw(self, frame: np.ndarray, hover_progress: float = 0.0):
        """Draw the key on frame."""
        # Determine color based on state
        if hover_progress > 0:
            # Interpolate between normal and active color
            color = tuple(int(self.hover_color[i] + (self.active_color[i] - self.hover_color[i]) * hover_progress) 
                         for i in range(3))
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color
        
        # Draw key background
        cv2.rectangle(frame, (self.x, self.y), 
                     (self.x + self.width, self.y + self.height),
                     color, -1)
        
        # Draw border
        cv2.rectangle(frame, (self.x, self.y),
                     (self.x + self.width, self.y + self.height),
                     (200, 200, 200), 2)
        
        # Draw text
        text_size = cv2.getTextSize(self.char, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = self.x + (self.width - text_size[0]) // 2
        text_y = self.y + (self.height + text_size[1]) // 2
        cv2.putText(frame, self.char, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Draw hover progress bar
        if hover_progress > 0:
            bar_height = 5
            bar_width = int(self.width * hover_progress)
            cv2.rectangle(frame, (self.x, self.y + self.height - bar_height),
                         (self.x + bar_width, self.y + self.height),
                         (0, 255, 0), -1)


class VirtualKeyboard:
    """Virtual keyboard for eye-controlled typing."""
    
    def __init__(self, position: Tuple[int, int] = (50, 50), 
                 key_size: Tuple[int, int] = (60, 60),
                 spacing: int = 10,
                 dwell_time: float = 1.5):
        """
        Initialize virtual keyboard.
        
        Args:
            position: (x, y) position of keyboard on screen
            key_size: (width, height) of each key
            spacing: Spacing between keys
            dwell_time: Time to dwell for key selection
        """
        self.position = position
        self.key_width, self.key_height = key_size
        self.spacing = spacing
        self.dwell_time = dwell_time
        
        # Keyboard layout
        self.layout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '?'],
            ['SPACE', 'BACK', 'CLEAR', 'ENTER']
        ]
        
        # Create keys
        self.keys: List[Key] = []
        self._create_keys()
        
        # State
        self.is_visible = False
        self.current_hover_key: Optional[Key] = None
        self.hover_start_time = None
        
        # Output
        self.text_buffer = ""
        self.on_text_change: Optional[Callable[[str], None]] = None
        
    def _create_keys(self):
        """Create key objects based on layout."""
        self.keys = []
        y = self.position[1]
        
        for row in self.layout:
            x = self.position[0]
            
            for char in row:
                # Special key widths
                if char == 'SPACE':
                    width = self.key_width * 3
                elif char in ['BACK', 'CLEAR', 'ENTER']:
                    width = self.key_width * 2
                else:
                    width = self.key_width
                
                key = Key(char, (x, y, width, self.key_height))
                self.keys.append(key)
                x += width + self.spacing
            
            y += self.key_height + self.spacing
    
    def show(self):
        """Show the keyboard."""
        self.is_visible = True
    
    def hide(self):
        """Hide the keyboard."""
        self.is_visible = False
    
    def toggle(self):
        """Toggle keyboard visibility."""
        self.is_visible = not self.is_visible
    
    def update(self, gaze_position: Optional[Tuple[int, int]], frame: np.ndarray) -> Optional[str]:
        """
        Update keyboard state with gaze position.
        
        Args:
            gaze_position: Current gaze position
            frame: Frame to draw on
            
        Returns:
            Selected character if a key was activated, None otherwise
        """
        if not self.is_visible:
            return None
        
        # Draw keyboard
        self.draw(frame)
        
        if gaze_position is None:
            self.current_hover_key = None
            self.hover_start_time = None
            return None
        
        # Check which key is being looked at
        hovered_key = None
        for key in self.keys:
            if key.contains_point(gaze_position):
                hovered_key = key
                break
        
        # Handle hover state changes
        if hovered_key != self.current_hover_key:
            # Reset all keys
            for key in self.keys:
                key.is_hovered = False
            
            # Set new hover
            self.current_hover_key = hovered_key
            self.hover_start_time = None
            
            if hovered_key:
                hovered_key.is_hovered = True
                import time
                self.hover_start_time = time.time()
        
        # Check for key activation
        if self.current_hover_key and self.hover_start_time:
            import time
            hover_duration = time.time() - self.hover_start_time
            
            if hover_duration >= self.dwell_time:
                # Key activated
                result = self._activate_key(self.current_hover_key)
                self.current_hover_key = None
                self.hover_start_time = None
                return result
        
        return None
    
    def _activate_key(self, key: Key) -> Optional[str]:
        """
        Activate a key and return the action.
        
        Args:
            key: Key to activate
            
        Returns:
            Character or action string
        """
        char = key.char
        
        if char == 'SPACE':
            self.text_buffer += ' '
            return ' '
        elif char == 'BACK':
            if self.text_buffer:
                self.text_buffer = self.text_buffer[:-1]
            return 'BACK'
        elif char == 'CLEAR':
            self.text_buffer = ""
            return 'CLEAR'
        elif char == 'ENTER':
            # Type the buffer using pyautogui
            if self.text_buffer:
                pyautogui.write(self.text_buffer)
                self.text_buffer = ""
            return 'ENTER'
        else:
            self.text_buffer += char
            return char
    
    def get_hover_progress(self) -> float:
        """Get current hover progress (0.0 to 1.0)."""
        if not self.current_hover_key or not self.hover_start_time:
            return 0.0
        
        import time
        hover_duration = time.time() - self.hover_start_time
        progress = min(hover_duration / self.dwell_time, 1.0)
        return progress
    
    def draw(self, frame: np.ndarray):
        """Draw keyboard on frame."""
        if not self.is_visible:
            return
        
        # Draw semi-transparent background
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Calculate keyboard dimensions
        max_width = max(
            sum(self.key_width + self.spacing for _ in row) 
            for row in self.layout
        )
        total_height = len(self.layout) * (self.key_height + self.spacing)
        
        # Draw background rectangle
        bg_padding = 20
        cv2.rectangle(overlay,
                     (self.position[0] - bg_padding, self.position[1] - bg_padding),
                     (self.position[0] + max_width + bg_padding, 
                      self.position[1] + total_height + bg_padding),
                     (30, 30, 30), -1)
        
        # Blend with original frame
        alpha = 0.7
        frame[:] = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        # Draw keys
        hover_progress = self.get_hover_progress()
        for key in self.keys:
            if key == self.current_hover_key:
                key.draw(frame, hover_progress)
            else:
                key.draw(frame, 0.0)
        
        # Draw text buffer
        if self.text_buffer:
            buffer_y = self.position[1] - 50
            cv2.rectangle(frame, (self.position[0], buffer_y - 35),
                         (self.position[0] + max_width, buffer_y - 5),
                         (50, 50, 50), -1)
            cv2.putText(frame, self.text_buffer, (self.position[0] + 10, buffer_y - 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def get_text(self) -> str:
        """Get current text buffer."""
        return self.text_buffer
    
    def clear_text(self):
        """Clear text buffer."""
        self.text_buffer = ""
    
    def set_text(self, text: str):
        """Set text buffer."""
        self.text_buffer = text
