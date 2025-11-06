# Phase 3: Backend Integration Bridge

## Overview
This phase implements a lightweight Python API server to bridge the React frontend with `pipeline_advanced.py`, handling command execution, file uploads, and real-time output streaming.

## Prerequisites
- Phase 1 & 2 completed
- Python 3.8+ installed
- Flask or FastAPI knowledge

---

## 1. Backend Architecture

### 1.1 Technology Stack

**Flask** - Lightweight WSGI web framework
- Simple REST API
- Server-Sent Events (SSE) support
- Easy integration with existing Python code

### 1.2 Project Structure

```
frontend/api/
├── __init__.py
├── server.py              # Main Flask application
├── routes/
│   ├── __init__.py
│   ├── research.py        # Research endpoints
│   └── persona.py         # Persona upload endpoints
├── services/
│   ├── __init__.py
│   ├── pipeline_service.py  # Pipeline execution
│   └── file_service.py     # File management
├── utils/
│   ├── __init__.py
│   └── stream_parser.py   # Parse pipeline output
├── uploads/               # Temporary persona files
└── requirements.txt       # API dependencies
```

---

## 2. API Server Setup

### 2.1 Install Dependencies (`frontend/api/requirements.txt`)

```txt
Flask==3.0.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
```

### 2.2 Main Server (`frontend/api/server.py`)

```python
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
}    })

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
```

---

## 3. Research Endpoints

### 3.1 Research Routes (`frontend/api/routes/research.py`)

```python
"""
Research API Routes
Handles pipeline execution and real-time streaming
"""
from flask import Blueprint, request, jsonify, Response
from services.pipeline_service import PipelineService, PipelineExecutionError
import json

research_bp = Blueprint('research', __name__)
pipeline_service = PipelineService()

@research_bp.route('/execute', methods=['POST'])
def execute_research():
    """
    Execute research pipeline
    
    Body:
        query (str): Research query
        persona_id (str, optional): ID of persona file to use
    
    Returns:
        Stream: Server-Sent Events with real-time progress
    """
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'error': 'Missing required field: query'}), 400
    
    query = data['query']
    persona_id = data.get('persona_id')
    
    def generate():
        """Generator for Server-Sent Events"""
        try:
            # Start execution
            yield f"data: {json.dumps({'type': 'start', 'query': query})}\n\n"
            
            # Execute pipeline with streaming
            for event in pipeline_service.execute_with_stream(query, persona_id):
                yield f"data: {json.dumps(event)}\n\n"
            
            # Complete
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            
        except PipelineExecutionError as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': f'Unexpected error: {str(e)}'})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@research_bp.route('/jobs', methods=['GET'])
def list_jobs():
    """List all research jobs"""
    jobs = pipeline_service.get_all_jobs()
    return jsonify({'jobs': jobs})

@research_bp.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    """Get specific job details"""
    job = pipeline_service.get_job(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job)

@research_bp.route('/jobs/<job_id>/result', methods=['GET'])
def get_job_result(job_id):
    """Get job result"""
    result = pipeline_service.get_job_result(job_id)
    
    if not result:
        return jsonify({'error': 'Result not found'}), 404
    
    return jsonify(result)
```

---

## 4. Persona Endpoints

### 4.1 Persona Routes (`frontend/api/routes/persona.py`)

```python
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
```

---

## 5. Services

### 5.1 Pipeline Service (`frontend/api/services/pipeline_service.py`)

```python
"""
Pipeline Service
Executes pipeline_advanced.py and streams output
"""
import subprocess
import json
import re
import uuid
from pathlib import Path
from typing import Generator, Dict, Any, Optional
from datetime import datetime

class PipelineExecutionError(Exception):
    """Pipeline execution error"""
    pass

class PipelineService:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.pipeline_script = self.project_root / 'pipeline_advanced.py'
        self.jobs = {}  # In-memory job storage (use DB in production)
    
    def execute_with_stream(
        self, 
        query: str, 
        persona_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Execute pipeline and stream output
        
        Args:
            query: Research query
            persona_id: Optional persona file ID
        
        Yields:
            Dict: Event data
        """
        job_id = str(uuid.uuid4())
        
        # Build command
        cmd = ['python', str(self.pipeline_script), query]
        
        # Add persona if provided
        if persona_id:
            persona_path = self._get_persona_path(persona_id)
            if persona_path and persona_path.exists():
                cmd.extend(['--writer-prompt', str(persona_path)])
        
        # Store job info
        self.jobs[job_id] = {
            'id': job_id,
            'query': query,
            'persona_id': persona_id,
            'status': 'running',
            'created_at': datetime.now().isoformat(),
            'started_at': datetime.now().isoformat()
        }
        
        try:
            # Execute pipeline
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.project_root)
            )
            
            # Stream output
            for line in iter(process.stdout.readline, ''):
                if not line:
                    break
                
                # Parse pipeline output
                event = self._parse_output_line(line)
                if event:
                    yield event
            
            # Wait for completion
            process.wait()
            
            if process.returncode != 0:
                error = process.stderr.read()
                self.jobs[job_id]['status'] = 'failed'
                self.jobs[job_id]['error'] = error
                raise PipelineExecutionError(f'Pipeline failed: {error}')
            
            # Update job status
            self.jobs[job_id]['status'] = 'completed'
            self.jobs[job_id]['completed_at'] = datetime.now().isoformat()
            
        except Exception as e:
            self.jobs[job_id]['status'] = 'failed'
            self.jobs[job_id]['error'] = str(e)
            raise
    
    def _parse_output_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse pipeline output line into event"""
        line = line.strip()
        
        if not line:
            return None
        
        # Parse iteration updates
        if 'Iteration' in line and 'State =' in line:
            match = re.search(r'Iteration (\d+): State = (\w+)', line)
            if match:
                return {
                    'type': 'progress',
                    'iteration': int(match.group(1)),
                    'state': match.group(2).lower(),
                    'message': line
                }
        
        # Parse transitions
        if '→ Transitioning:' in line:
            return {
                'type': 'state',
                'message': line
            }
        
        # Parse metrics
        if 'Confidence:' in line:
            confidence_match = re.search(r'Confidence: ([\d.]+)', line)
            coverage_match = re.search(r'Coverage: ([\d.]+)', line)
            
            return {
                'type': 'metrics',
                'confidence': float(confidence_match.group(1)) if confidence_match else 0,
                'coverage': float(coverage_match.group(1)) if coverage_match else 0,
                'message': line
            }
        
        # Generic log
        return {
            'type': 'log',
            'message': line
        }
    
    def _get_persona_path(self, persona_id: str) -> Optional[Path]:
        """Get path to persona file"""
        upload_folder = Path(__file__).parent.parent / 'uploads'
        persona_file = upload_folder / f"{persona_id}.md"
        return persona_file if persona_file.exists() else None
    
    def get_all_jobs(self) -> list:
        """Get all jobs"""
        return list(self.jobs.values())
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get specific job"""
        return self.jobs.get(job_id)
   
    def get_job_result(self, job_id: str) -> Optional[Dict]:
        """Get job result from output files"""
        # Look for result file in examples/
        examples_dir = self.project_root / 'examples'
        
        # Find most recent result file
        result_files = sorted(examples_dir.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if result_files:
            with open(result_files[0], 'r') as f:
                return json.load(f)
        
        return None
```

### 5.2 File Service (`frontend/api/services/file_service.py`)

```python
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
```

---

## 6. Frontend Service Integration

### 6.1 API Service (`frontend/src/services/api.ts`)

```typescript
/**
 * API Service for Deep Search Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export interface ApiError {
  error: string
}

export class ApiService {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`)
    return response.json()
  }

  // Execute research with SSE
  executeResearch(query: string, personaId?: string): EventSource {
    const params = new URLSearchParams({
      query,
      ...(personaId && { persona_id: personaId })
    })

    // Note: EventSource only supports GET, so we use POST via fetch for initial request
    // then establish SSE connection
    const url = `${this.baseUrl}/api/research/execute`
    
    // Create EventSource for SSE
    const eventSource = new EventSource(url)
    
    // Send POST request to start execution
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        persona_id: personaId
      })
    })

    return eventSource
  }

  // Upload persona
  async uploadPersona(file: File): Promise<any> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${this.baseUrl}/api/persona/upload`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.error)
    }

    return response.json()
  }

  // List personas
  async listPersonas(): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/api/persona/list`)
    const data = await response.json()
    return data.personas
  }
}

export const apiService = new ApiService()
```

---

## 7. Running the Backend

### 7.1 Start API Server

```bash
# From frontend/api/ directory
python server.py
```

### 7.2 Environment Configuration

Create `frontend/api/.env`:

```env
API_PORT=5000
API_DEBUG=True
FLASK_ENV=development
```

---

## 8. Testing the Integration

### 8.1 Test Health Endpoint

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "Deep Search API"
}
```

### 8.2 Test Research Execution

```bash
curl -X POST http://localhost:5000/api/research/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "What is quantum computing?"}'
```

### 8.3 Test Persona Upload

```bash
curl -X POST http://localhost:5000/api/persona/upload \
  -F "file=@../../isaac.md"
```

---

## 9. Next Steps

**Phase 3 Complete!** You now have:
- ✅ Flask API server running
- ✅ Research execution endpoint with SSE streaming
- ✅ Persona upload and management
- ✅ Frontend service integration

**Proceed to Phase 4:** State Management & Logic

---

## Troubleshooting

### Issue: CORS errors
**Solution:** Ensure Flask-CORS is installed and configured properly

### Issue: Pipeline not found
**Solution:** Check that `sys.path` includes parent directory

### Issue: SSE connection drops
**Solution:** Use `threaded=True` in Flask app.run()

**Phase 3 Complete!** 🎉
