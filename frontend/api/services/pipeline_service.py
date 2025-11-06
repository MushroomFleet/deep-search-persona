"""
Pipeline Service
Executes pipeline_advanced.py and streams output
"""
import subprocess
import json
import re
import uuid
import os
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
        
        # Build command with unbuffered output for real-time streaming
        cmd = ['python', '-u', str(self.pipeline_script), query]
        
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
            # Set UTF-8 encoding for child process (fixes Windows Unicode issues)
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'  # Force child Python to use UTF-8
            
            # Execute pipeline with UTF-8 encoding
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',  # Replace problematic characters instead of crashing
                env=env,  # Pass modified environment to child process
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
            
            # Load and send result
            result = self._load_latest_result()
            if result:
                yield {
                    'type': 'result',
                    'data': result
                }
            
        except Exception as e:
            self.jobs[job_id]['status'] = 'failed'
            self.jobs[job_id]['error'] = str(e)
            raise
    
    def _parse_output_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse pipeline output line into event"""
        line = line.strip()
        
        if not line:
            return None
        
        # Parse iteration updates (handle --- delimiters)
        if 'Iteration' in line and 'State =' in line:
            # Match pattern like: --- Iteration 10: State = SYNTHESIZING ---
            match = re.search(r'Iteration (\d+):\s*State\s*=\s*(\w+)', line)
            if match:
                return {
                    'type': 'progress',
                    'iteration': int(match.group(1)),
                    'state': match.group(2).lower(),
                    'message': line
                }
        
        # Parse transitions
        if '→ Transitioning:' in line or 'Transitioning:' in line:
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
   
    def _load_latest_result(self) -> Optional[Dict]:
        """Load the most recent research result"""
        # Check both examples/ (JSON) and research_outputs/ (Markdown)
        examples_dir = self.project_root / 'examples'
        outputs_dir = self.project_root / 'research_outputs'
        
        # Find most recent JSON file
        json_files = sorted(examples_dir.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Find most recent markdown file
        md_files = sorted(outputs_dir.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)
        
        result_data = None
        report_text = None
        
        # Load JSON data
        if json_files:
            with open(json_files[0], 'r', encoding='utf-8') as f:
                result_data = json.load(f)
        
        # Load markdown report
        if md_files:
            with open(md_files[0], 'r', encoding='utf-8') as f:
                report_text = f.read()
        
        # Combine both sources
        if result_data:
            # Add markdown report if available
            if report_text:
                result_data['final_report'] = report_text
            return result_data
        
        return None
    
    def get_job_result(self, job_id: str) -> Optional[Dict]:
        """Get job result from output files"""
        return self._load_latest_result()
