"""
Logger Module
Provides logging functionality for the eye tracking system.
"""

import logging
import colorlog
import os
from datetime import datetime


def setup_logger(name: str = "EyeTracker", 
                log_file: str = None,
                level: str = "INFO") -> logging.Logger:
    """
    Setup and configure logger.
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level
        
    Returns:
        Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


class PerformanceLogger:
    """Logger for performance metrics."""
    
    def __init__(self, logger: logging.Logger = None):
        """Initialize performance logger."""
        self.logger = logger or logging.getLogger("Performance")
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, name: str):
        """Start a performance timer."""
        self.start_times[name] = datetime.now()
    
    def stop_timer(self, name: str) -> float:
        """Stop a performance timer and return elapsed time."""
        if name not in self.start_times:
            self.logger.warning(f"Timer '{name}' was not started")
            return 0.0
        
        elapsed = (datetime.now() - self.start_times[name]).total_seconds()
        
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(elapsed)
        del self.start_times[name]
        
        return elapsed
    
    def get_average(self, name: str) -> float:
        """Get average time for a metric."""
        if name not in self.metrics or not self.metrics[name]:
            return 0.0
        
        return sum(self.metrics[name]) / len(self.metrics[name])
    
    def get_fps(self, name: str = "frame") -> float:
        """Calculate FPS from frame times."""
        avg_time = self.get_average(name)
        return 1.0 / avg_time if avg_time > 0 else 0.0
    
    def log_metrics(self):
        """Log all metrics."""
        for name, times in self.metrics.items():
            avg_time = sum(times) / len(times)
            fps = 1.0 / avg_time if avg_time > 0 else 0
            self.logger.info(f"{name}: avg={avg_time:.4f}s, fps={fps:.2f}")
    
    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.start_times.clear()
