"""
Deep Search API Bridge
Connects React frontend to pipeline_advanced.py
"""
import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Add parent directory to path to import pipeline
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from routes import research_bp, persona_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max
app.config['UPLOAD_EXTENSIONS'] = ['.md', '.markdown', '.txt']

# Ensure upload directory exists
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# Register blueprints
app.register_blueprint(research_bp, url_prefix='/api/research')
app.register_blueprint(persona_bp, url_prefix='/api/persona')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'service': 'Deep Search API'
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Get API status and configuration"""
    return jsonify({
        'status': 'running',
        'upload_folder': str(app.config['UPLOAD_FOLDER']),
        'max_file_size': app.config['MAX_CONTENT_LENGTH'],
        'allowed_extensions': app.config['UPLOAD_EXTENSIONS']
    })

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('API_DEBUG', 'False').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"Deep Search API Server")
    print(f"{'='*60}")
    print(f"Server running on: http://localhost:{port}")
    print(f"Debug mode: {debug}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)
