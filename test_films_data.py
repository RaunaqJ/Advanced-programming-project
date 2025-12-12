#!/usr/bin/env python3
"""
Test Films Data - Test 2
Tests JSON file operations for Film Cinemax
"""

import unittest
import json
import os
import shutil
from backend import load_media, save_media

DATA_FILE = 'films.json'
BACKUP_FILE = 'films_backup.json'

class TestFilmsDataOperations(unittest.TestCase):
    """Test Film Cinemax data operations"""
    
    @classmethod
    def setUpClass(cls):
        """Backup original data before tests"""
        if os.path.exists(DATA_FILE):
            shutil.copy(DATA_FILE, BACKUP_FILE)
    
    @classmethod
    def tearDownClass(cls):
        """Restore original data after tests"""
        if os.path.exists(BACKUP_FILE):
            shutil.copy(BACKUP_FILE, DATA_FILE)
            os.remove(BACKUP_FILE)
    
    def test_load_films(self):
        """Test loading films from JSON file"""
        films = load_media()
        self.assertIsInstance(films, list)
        self.assertGreater(len(films), 0)
    
    def test_film_structure(self):
        """Test that films have correct structure"""
        films = load_media()
        required_fields = ['id', 'name', 'director', 'year', 'category']
        
        for film in films:
            for field in required_fields:
                self.assertIn(field, film)
    
    def test_save_films(self):
        """Test saving films to JSON file"""
        films = load_media()
        original_count = len(films)
        save_media(films)
        loaded_films = load_media()
        self.assertEqual(len(loaded_films), original_count)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("TEST 2: DATA OPERATIONS TESTS")
    print("="*60 + "\n")
    unittest.main(verbosity=2)
