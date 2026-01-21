"""
Configuration Module
Manages application settings and configurations.
"""

import yaml
import json
import os
from typing import Any, Dict


class Config:
    """Configuration manager for eye tracking system."""
    
    # Default configuration
    DEFAULT_CONFIG = {
        'camera': {
            'device_id': 0,
            'width': 640,
            'height': 480,
            'fps': 30
        },
        'eye_tracking': {
            'max_faces': 1,
            'min_detection_confidence': 0.5,
            'min_tracking_confidence': 0.5,
            'smoothing_window': 5
        },
        'mouse_control': {
            'sensitivity': 1.0,
            'smoothing': 5,
            'dwell_time': 1.5,
            'click_mode': 'dwell'  # 'dwell', 'blink', or 'manual'
        },
        'calibration': {
            'num_points': 9,
            'samples_per_point': 30,
            'dwell_time': 2.0
        },
        'keyboard': {
            'position': [50, 50],
            'key_size': [60, 60],
            'spacing': 10,
            'dwell_time': 1.5
        },
        'accessibility': {
            'blink_detection': True,
            'gesture_control': True,
            'voice_feedback': False
        },
        'ui': {
            'show_video_feed': True,
            'show_gaze_indicator': True,
            'show_fps': True,
            'fullscreen': False
        },
        'logging': {
            'enabled': True,
            'level': 'INFO',
            'log_file': 'eye_tracker.log'
        }
    }
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file (YAML or JSON)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
    
    def load_from_file(self, filepath: str):
        """Load configuration from file."""
        try:
            with open(filepath, 'r') as f:
                if filepath.endswith('.yaml') or filepath.endswith('.yml'):
                    user_config = yaml.safe_load(f)
                elif filepath.endswith('.json'):
                    user_config = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {filepath}")
                
                # Update config with user settings
                self._update_nested_dict(self.config, user_config)
                
        except Exception as e:
            print(f"Error loading config file: {e}")
    
    def _update_nested_dict(self, base: Dict, update: Dict):
        """Recursively update nested dictionary."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._update_nested_dict(base[key], value)
            else:
                base[key] = value
    
    def save_to_file(self, filepath: str):
        """Save configuration to file."""
        try:
            with open(filepath, 'w') as f:
                if filepath.endswith('.yaml') or filepath.endswith('.yml'):
                    yaml.dump(self.config, f, default_flow_style=False)
                elif filepath.endswith('.json'):
                    json.dump(self.config, f, indent=2)
                else:
                    raise ValueError(f"Unsupported config file format: {filepath}")
        except Exception as e:
            print(f"Error saving config file: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Path to config value (e.g., 'camera.width')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Path to config value (e.g., 'camera.width')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_section(self, section: str) -> Dict:
        """Get entire configuration section."""
        return self.config.get(section, {})
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access."""
        return self.config[key]
    
    def __setitem__(self, key: str, value: Any):
        """Allow dictionary-style setting."""
        self.config[key] = value
