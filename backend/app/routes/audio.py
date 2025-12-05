from flask import Blueprint, request, jsonify, send_file
import uuid
from datetime import datetime
from app.models.database import execute_db
from app.services.audio_service import AudioService
import os

audio_bp = Blueprint('audio', __name__, url_prefix='/api/audio')

@audio_bp.route('/generate', methods=['POST'])
def generate_audio():
    """Generate audio from text using TTS"""
    data = request.json
    project_id = data.get('project_id')
    scene_id = data.get('scene_id')
    text = data.get('text', '')
    track_type = data.get('track_type', 'narration')  # 'narration' or 'dialogue'
    
    if not text or not project_id:
        return jsonify({'error': 'text and project_id required'}), 400
    
    # Generate audio
    result = AudioService.generate_narration(text)
    
    if not result['success']:
        return jsonify({'error': result.get('error', 'Failed to generate audio')}), 500
    
    # Save to database
    audio_id = str(uuid.uuid4())
    execute_db(
        '''INSERT INTO audio_tracks (id, project_id, scene_id, track_type, content, duration, file_path, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (audio_id, project_id, scene_id, track_type, text, result['duration'], 
         result['filepath'], datetime.now().isoformat())
    )
    
    return jsonify({
        'audio_id': audio_id,
        'filename': result['filename'],
        'duration': result['duration'],
        'text': text
    }), 201

@audio_bp.route('/estimate-duration', methods=['POST'])
def estimate_duration():
    """Estimate audio duration from text"""
    data = request.json
    text = data.get('text', '')
    
    duration = AudioService.estimate_duration(text)
    
    return jsonify({'text': text, 'estimated_duration': duration}), 200

@audio_bp.route('/mouth-animation/<duration>', methods=['GET'])
def get_mouth_animation(duration):
    """Get mouth animation keyframes for given audio duration"""
    try:
        dur = float(duration)
    except:
        return jsonify({'error': 'Invalid duration'}), 400
    
    keyframes = AudioService.generate_mouth_animation_frames(dur)
    
    return jsonify({'keyframes': keyframes}), 200

@audio_bp.route('/<filename>', methods=['GET'])
def serve_audio(filename):
    """Serve audio file"""
    try:
        # Security: ensure filename doesn't contain path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        # Use os.path.join for proper path handling on all platforms
        filepath = os.path.join(os.getcwd(), 'storage', 'audio', filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': f'Audio file not found: {filename}'}), 404
        
        return send_file(filepath, mimetype='audio/wav', as_attachment=False)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
