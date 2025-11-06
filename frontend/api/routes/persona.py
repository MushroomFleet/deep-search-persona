"""
Persona API Routes
Handles persona file uploads and management
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from services.file_service import FileService
import os

persona_bp = Blueprint('persona', __name__)
file_service = FileService()

def allowed_file(filename):
    """Check if file extension is allowed"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in current_app.config['UPLOAD_EXTENSIONS']

@persona_bp.route('/upload', methods=['POST'])
def upload_persona():
    """
    Upload persona file
    
    Form Data:
        file: Persona markdown file
    
    Returns:
        JSON: Persona metadata
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'error': f'Invalid file type. Allowed: {current_app.config["UPLOAD_EXTENSIONS"]}'
        }), 400
    
    try:
        # Save file and get metadata
        persona = file_service.save_persona(file)
        return jsonify(persona), 201
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@persona_bp.route('/list', methods=['GET'])
def list_personas():
    """List all uploaded personas"""
    personas = file_service.list_personas()
    return jsonify({'personas': personas})

@persona_bp.route('/<persona_id>', methods=['GET'])
def get_persona(persona_id):
    """Get persona by ID"""
    persona = file_service.get_persona(persona_id)
    
    if not persona:
        return jsonify({'error': 'Persona not found'}), 404
    
    return jsonify(persona)

@persona_bp.route('/<persona_id>', methods=['DELETE'])
def delete_persona(persona_id):
    """Delete persona"""
    success = file_service.delete_persona(persona_id)
    
    if not success:
        return jsonify({'error': 'Persona not found'}), 404
    
    return jsonify({'message': 'Persona deleted successfully'})
