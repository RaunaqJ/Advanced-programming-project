from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'films.json'

def load_media():
    """Load media data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_media(media_list):
    """Save media data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(media_list, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving media: {e}")
        return False

@app.route('/api/films', methods=['GET'])
@app.route('/api/media', methods=['GET'])
def get_all_media():
    """Endpoint 1: List of all available media items"""
    try:
        media_list = load_media()
        return jsonify({
            'success': True,
            'data': media_list,
            'count': len(media_list)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/media/category/<category>', methods=['GET'])
def get_media_by_category(category):
    """Endpoint 2: List of media items in a specific category"""
    try:
        media_list = load_media()
        filtered_media = [m for m in media_list if m.get('category', '').lower() == category.lower()]
        return jsonify({
            'success': True,
            'data': filtered_media,
            'count': len(filtered_media),
            'category': category
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/media/search', methods=['GET'])
def search_media():
    """Endpoint 3: Search for media items with a specific name (exact match)"""
    try:
        name = request.args.get('name', '')
        if not name:
            return jsonify({
                'success': False,
                'error': 'Name parameter is required'
            }), 400
        
        media_list = load_media()
        found_media = [m for m in media_list if m.get('name', '').lower() == name.lower()]
        
        return jsonify({
            'success': True,
            'data': found_media,
            'count': len(found_media)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/media/<int:media_id>', methods=['GET'])
def get_media_details(media_id):
    """Endpoint 4: Display the metadata of a specific media item"""
    try:
        media_list = load_media()
        media = next((m for m in media_list if m.get('id') == media_id), None)
        
        if media:
            return jsonify({
                'success': True,
                'data': media
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Media not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/films', methods=['POST'])
@app.route('/api/media', methods=['POST'])
def create_media():
    """Endpoint 5: Create a new media item"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        media_list = load_media()
        
        # Generate new ID (as integer)
        new_id = max([int(m.get('id', 0)) if isinstance(m.get('id'), (int, str)) else 0 for m in media_list], default=0) + 1
        
        new_media = {
            'id': new_id,
            'name': data['name'],
            'year': data.get('year') or data.get('publication_date', ''),
            'director': data.get('director') or data.get('author', ''),
            'category': data['category'],
            'runtime': data.get('runtime', ''),
            'description': data.get('description', ''),
            'created_at': datetime.now().isoformat()
        }
        
        media_list.append(new_media)
        
        if save_media(media_list):
            return jsonify({
                'success': True,
                'data': new_media,
                'message': 'Media created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save media'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/films/<film_id>', methods=['DELETE'])
@app.route('/api/media/<film_id>', methods=['DELETE'])
def delete_media(film_id):
    """Endpoint 6: Delete a specific media item"""
    try:
        media_list = load_media()
        # Convert to string since IDs in JSON are strings
        media = next((m for m in media_list if str(m.get('id')) == str(film_id)), None)
        
        if not media:
            return jsonify({
                'success': False,
                'error': 'Media not found'
            }), 404
        
        media_list = [m for m in media_list if str(m.get('id')) != str(film_id)]
        
        if save_media(media_list):
            return jsonify({
                'success': True,
                'message': 'Media deleted successfully',
                'deleted_media': media
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save changes'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Initialize with sample data if file doesn't exist
    if not os.path.exists(DATA_FILE):
        sample_data = [
            {
                'id': 1,
                'name': 'The Shawshank Redemption',
                'publication_date': '1994',
                'author': 'Frank Darabont',
                'category': 'Film'
            },
            {
                'id': 2,
                'name': 'The Godfather',
                'publication_date': '1972',
                'author': 'Francis Ford Coppola',
                'category': 'Film'
            },
            {
                'id': 3,
                'name': 'Pulp Fiction',
                'publication_date': '1994',
                'author': 'Quentin Tarantino',
                'category': 'Film'
            }
        ]
        save_media(sample_data)
    
    app.run(debug=False, port=5000)