#!/usr/bin/env python3
"""Quick test to verify the setup"""

import sys
import time

# Test 1: Check Flask
print("Testing Flask backend...")
try:
    import requests
    time.sleep(1)
    response = requests.get('http://localhost:8000/api/films', timeout=3)
    print(f"✓ Flask is running: {len(response.json())} films loaded")
except Exception as e:
    print(f"✗ Flask error: {e}")
    sys.exit(1)

# Test 2: Check PyQt6
print("Testing PyQt6...")
try:
    from PyQt6.QtWidgets import QApplication
    print("✓ PyQt6 is installed")
except Exception as e:
    print(f"✗ PyQt6 error: {e}")
    sys.exit(1)

print("\n✓ All systems ready! You can now run:")
print("  python3 /Users/raunaqj/Desktop/cs\\ test1/app.py")
