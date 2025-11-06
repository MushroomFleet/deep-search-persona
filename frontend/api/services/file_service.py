"""
File Service
Manages persona file uploads and storage
"""
import os
import uuid
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import Optional, Dict, List

class FileService:
    def __init__(self):
        self.upload_folder = Path(__file__).parent.parent / 'uploads'
        self.upload_folder.mkdir(exist_ok=True)
        self.personas = {}  # In-memory storage (use DB in production)
    
    def save_persona(self, file) -> Dict:
        """
        Save uploaded persona file
        
        Args:
            file: FileStorage object
        
        Returns:
            Dict: Persona metadata
        """
        # Generate unique ID
        persona_id = str(uuid.uuid4())
        
        # Secure filename
        original_filename = secure_filename(file.filename)
        filename = f"{persona_id}.md"
        filepath = self.upload_folder / filename
        
        # Save file
        file.save(str(filepath))
        
        # Read content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Store metadata
        persona = {
            'id': persona_id,
            'name': original_filename.replace('.md', '').replace('.markdown', '').replace('.txt', ''),
            'filename': original_filename,
            'filepath': str(filepath),
            'content_length': len(content),
            'uploaded_at': datetime.now().isoformat()
        }
        
        self.personas[persona_id] = persona
        
        return persona
    
    def list_personas(self) -> List[Dict]:
        """List all personas"""
        return list(self.personas.values())
    
    def get_persona(self, persona_id: str) -> Optional[Dict]:
        """Get persona by ID"""
        return self.personas.get(persona_id)
    
    def delete_persona(self, persona_id: str) -> bool:
        """Delete persona"""
        if persona_id not in self.personas:
            return False
        
        persona = self.personas[persona_id]
        filepath = Path(persona['filepath'])
        
        # Delete file
        if filepath.exists():
            filepath.unlink()
        
        # Remove from storage
        del self.personas[persona_id]
        
        return True
