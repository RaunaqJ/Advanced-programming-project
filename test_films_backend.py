#!/usr/bin/env python3
"""
Test Films Backend - Test 1
Tests Flask REST API endpoints for Film Cinemax
"""

import unittest
import json
from backend import app

class TestFilmsBackendAPI(unittest.TestCase):
    """Test Film Cinemax backend API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_get_all_films(self):
        """Test GET /api/films - Retrieve all films"""
        response = self.client.get('/api/films')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
    
    def test_get_films_by_category(self):
        """Test GET /api/media/category/Drama - Filter by category"""
        response = self.client.get('/api/media/category/Drama')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('data', data)
    
    def test_add_film(self):
        """Test POST /api/films - Add a new film"""
        new_film = {
            'name': 'Test Film',
            'director': 'Test Director',
            'year': 2025,
            'category': 'Drama'
        }
        response = self.client.post('/api/films', json=new_film)
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertTrue(data['success'])

if __name__ == '__main__':
    print("\n" + "="*60)
    print("TEST 1: BACKEND API TESTS")
    print("="*60 + "\n")
    unittest.main(verbosity=2)
