#!/usr/bin/env python3
"""
Test Films Frontend - Test 3
Tests PyQt6 GUI and backend connection for Film Cinemax
"""

import unittest
import sys
import requests
from PyQt6.QtWidgets import QApplication

class TestFilmsFrontendIntegration(unittest.TestCase):
    """Test Film Cinemax frontend integration"""
    
    @classmethod
    def setUpClass(cls):
        """Create QApplication instance"""
        if not QApplication.instance():
            cls.qapp = QApplication(sys.argv)
        else:
            cls.qapp = QApplication.instance()
    
    def test_pyqt6_installed(self):
        """Test that PyQt6 is properly installed"""
        try:
            from PyQt6.QtWidgets import QMainWindow, QTableWidget, QDialog
            from PyQt6.QtCore import Qt
        except ImportError as e:
            self.fail(f"PyQt6 not installed: {e}")
    
    def test_app_file_exists(self):
        """Test that app.py file exists"""
        import os
        app_exists = os.path.exists('app.py')
        self.assertTrue(app_exists, "app.py file not found")
    
    def test_backend_connection(self):
        """Test that Flask backend is running on port 5000"""
        try:
            response = requests.get('http://localhost:5000/api/films', timeout=3)
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.ConnectionError:
            self.fail("Cannot connect to backend on localhost:5000")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("TEST 3: FRONTEND INTEGRATION TESTS")
    print("="*60 + "\n")
    unittest.main(verbosity=2)
