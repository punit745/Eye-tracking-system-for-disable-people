#!/usr/bin/env python3
"""
Validation script to test imports and basic functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    try:
        # Test core modules
        from core.eye_tracker import EyeTracker
        print("✓ EyeTracker imported successfully")
        
        from core.mouse_controller import MouseController, ClickMode
        print("✓ MouseController imported successfully")
        
        from core.calibration import Calibration
        print("✓ Calibration imported successfully")
        
        from core.virtual_keyboard import VirtualKeyboard
        print("✓ VirtualKeyboard imported successfully")
        
        # Test utility modules
        from utils.config import Config
        print("✓ Config imported successfully")
        
        from utils.logger import setup_logger
        print("✓ Logger imported successfully")
        
        print("\n✓ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

def test_dependencies():
    """Test that all dependencies are available."""
    print("\nTesting dependencies...")
    
    dependencies = [
        ('cv2', 'opencv-python'),
        ('mediapipe', 'mediapipe'),
        ('numpy', 'numpy'),
        ('pyautogui', 'pyautogui'),
        ('yaml', 'pyyaml'),
    ]
    
    all_ok = True
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {package_name} available")
        except ImportError:
            print(f"✗ {package_name} not found - install with: pip install {package_name}")
            all_ok = False
    
    return all_ok

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from utils.config import Config
        config = Config()
        
        # Test default values
        assert config.get('camera.width') == 640
        assert config.get('mouse_control.sensitivity') == 1.0
        
        print("✓ Configuration system working")
        return True
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Eye Tracking System - Validation")
    print("=" * 50)
    print()
    
    results = []
    
    # Run tests
    results.append(("Dependencies", test_dependencies()))
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    
    # Summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(passed for _, passed in results)
    
    print()
    if all_passed:
        print("✓ All validations passed!")
        print("\nYou can now run the application:")
        print("  python src/main.py")
        return 0
    else:
        print("✗ Some validations failed")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
