"""
Research API Routes
Handles pipeline execution and real-time streaming
"""
from flask import Blueprint, request, jsonify, Response
from services.pipeline_service import PipelineService, PipelineExecutionError
import json

research_bp = Blueprint('research', __name__)
pipeline_service = PipelineService()

@research_bp.route('/execute', methods=['POST', 'GET'])
def execute_research():
    """
    Execute research pipeline
    
    Query Params (GET):
        query (str): Research query
        persona_id (str, optional): ID of persona file to use
    
    Body (POST):
        query (str): Research query
        persona_id (str, optional): ID of persona file to use
    
    Returns:
        Stream: Server-Sent Events with real-time progress
    """
    # Support both GET (for EventSource) and POST
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing required field: query'}), 400
        query = data['query']
        persona_id = data.get('persona_id')
    else:  # GET
        query = request.args.get('query')
        persona_id = request.args.get('persona_id')
        
        if not query:
            return jsonify({'error': 'Missing required field: query'}), 400
    
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
