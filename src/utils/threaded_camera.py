"""
Threaded Camera Module
Provides a threaded camera class for better frame capture performance.
"""

import cv2
import threading
import queue
from typing import Tuple, Optional
import time


class ThreadedCamera:
    """
    A threaded camera class that captures frames in a separate thread.
    This prevents frame capture from blocking the main processing loop.
    """
    
    def __init__(self, device_id: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        """
        Initialize the threaded camera.
        
        Args:
            device_id: Camera device ID (default 0)
            width: Frame width
            height: Frame height
            fps: Target frames per second
        """
        self.device_id = device_id
        self.cap = cv2.VideoCapture(device_id)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera {device_id}")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        
        # Frame buffer (only keep latest 2 frames)
        self.frame_queue = queue.Queue(maxsize=2)
        
        # Thread control
        self.running = False
        self.thread = None
        
        # Latest frame for non-blocking access
        self._latest_frame = None
        self._frame_lock = threading.Lock()
        
        # Start capture thread
        self.start()
    
    def start(self):
        """Start the capture thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
    
    def _capture_loop(self):
        """Continuously capture frames in background thread."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Update latest frame
                with self._frame_lock:
                    self._latest_frame = frame.copy()
                
                # Update queue (drop old frames if full)
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except queue.Empty:
                        pass
                try:
                    self.frame_queue.put_nowait(frame)
                except queue.Full:
                    pass
            else:
                # Small delay on failed read to prevent CPU spinning
                time.sleep(0.01)
    
    def read(self) -> Tuple[bool, Optional[cv2.typing.MatLike]]:
        """
        Read a frame (blocking if no frame available).
        
        Returns:
            Tuple of (success, frame)
        """
        try:
            frame = self.frame_queue.get(timeout=1.0)
            return True, frame
        except queue.Empty:
            return False, None
    
    def read_latest(self) -> Tuple[bool, Optional[cv2.typing.MatLike]]:
        """
        Read the latest frame (non-blocking).
        
        Returns:
            Tuple of (success, frame)
        """
        with self._frame_lock:
            if self._latest_frame is not None:
                return True, self._latest_frame.copy()
        return False, None
    
    def isOpened(self) -> bool:
        """Check if camera is opened."""
        return self.cap.isOpened() and self.running
    
    def set(self, prop_id: int, value: float) -> bool:
        """Set a camera property."""
        return self.cap.set(prop_id, value)
    
    def get(self, prop_id: int) -> float:
        """Get a camera property."""
        return self.cap.get(prop_id)
    
    def stop(self):
        """Stop the capture thread."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
    
    def release(self):
        """Release camera resources."""
        self.stop()
        if self.cap:
            self.cap.release()


# Optional: Keep original camera interface for compatibility
Camera = ThreadedCamera
