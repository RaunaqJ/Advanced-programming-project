"""
Film Cinemax Backend API
Flask REST API for film collection management
"""

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

JSON_FILE = 'films.json'

def load_films():
    """Load films from JSON file"""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_films(films):
    """Save films to JSON file"""
    with open(JSON_FILE, 'w') as f:
        json.dump(films, f, indent=2)

def get_next_id():
    """Get next available ID"""
    films = load_films()
    if not films:
        return 1
    return max(int(f['id']) for f in films) + 1

@app.route('/api/films', methods=['GET'])
def get_films():
    """Get all films - API endpoint"""
    films = load_films()
    category = request.args.get('category')
    search = request.args.get('search')
    
    if category and category != 'All':
        films = [f for f in films if f['category'] == category]
    
    if search:
        search_lower = search.lower()
        films = [f for f in films if search_lower in f['name'].lower() or 
                search_lower in f['director'].lower()]
    
    return jsonify(films)

@app.route('/api/films', methods=['POST'])
def add_film():
    """Add a new film"""
    data = request.json
    films = load_films()
    
    new_film = {
        'id': str(get_next_id()),
        'name': data.get('name'),
        'director': data.get('director'),
        'year': int(data.get('year')),
        'category': data.get('category'),
        'created_at': datetime.now().isoformat()
    }
    
    films.append(new_film)
    save_films(films)
    
    return jsonify(new_film), 201

@app.route('/api/films/<film_id>', methods=['DELETE'])
def delete_film(film_id):
    """Delete a film"""
    films = load_films()
    films = [f for f in films if f['id'] != film_id]
    save_films(films)
    
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=False, port=8000, threaded=True)

