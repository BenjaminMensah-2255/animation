from flask import Blueprint, request, jsonify
import uuid
import json
from datetime import datetime
from app.models.database import query_db, execute_db
from app.services.story_generator import StoryGenerator
from app.services.audio_service import AudioService

story_bp = Blueprint('story', __name__, url_prefix='/api/stories')

@story_bp.route('/create', methods=['POST'])
def create_story():
    """Create a new story from a prompt or template"""
    data = request.json
    project_id = data.get('project_id')
    prompt = data.get('prompt', '')
    use_template = data.get('use_template', False)
    
    if not project_id:
        return jsonify({'error': 'project_id required'}), 400
    
    # Generate story structure
    story_data = StoryGenerator.generate_from_prompt(prompt)
    
    story_id = story_data['story_id']
    title = story_data['title']
    
    # Insert into database
    execute_db(
        '''INSERT INTO stories (id, project_id, title, description, content, created_at)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (story_id, project_id, title, prompt, str(story_data), datetime.now().isoformat())
    )
    
    # Create scenes in database and auto-generate audio
    scenes_response = []
    for scene in story_data.get('scenes', []):
        scene_id = str(uuid.uuid4())
        characters_data = json.dumps(scene.get('characters', []))
        animations_data = json.dumps(scene.get('animations', []))
        narration = scene.get('narration', '')
        audio_filename = None
        
        execute_db(
            '''INSERT INTO scenes (id, project_id, story_id, sequence, title, background_type, characters, narration, duration, transitions, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (scene_id, project_id, story_id, scene.get('sequence', 1), scene.get('title', ''), 
             scene.get('background', 'forest'), characters_data, narration, scene.get('duration', 3),
             animations_data, datetime.now().isoformat())
        )
        
        # Auto-generate audio for the scene
        try:
            if narration and narration.strip():
                audio_filename = AudioService.generate_audio(narration, scene_id)
                audio_duration = AudioService.get_audio_duration(audio_filename)
                
                # Save audio track to database
                audio_id = str(uuid.uuid4())
                execute_db(
                    '''INSERT INTO audio_tracks (id, project_id, scene_id, track_type, content, duration, file_path, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (audio_id, project_id, scene_id, 'narration', narration, audio_duration, audio_filename, datetime.now().isoformat())
                )
        except Exception as e:
            print(f"Error generating audio for scene {scene_id}: {e}")
        
        scenes_response.append({
            'id': scene_id,
            'sequence': scene.get('sequence', 1),
            'title': scene.get('title', ''),
            'background': scene.get('background', 'forest'),
            'narration': narration,
            'audio_filename': audio_filename,
            'audio_ready': True
        })
    
    return jsonify({
        'story_id': story_id,
        'title': title,
        'scenes': scenes_response
    }), 201

@story_bp.route('/characters', methods=['GET'])
def get_characters():
    """Get available predefined characters"""
    return jsonify(StoryGenerator.get_available_characters()), 200

@story_bp.route('/backgrounds', methods=['GET'])
def get_backgrounds():
    """Get available predefined backgrounds"""
    return jsonify(StoryGenerator.get_available_backgrounds()), 200

@story_bp.route('/<story_id>', methods=['GET'])
def get_story(story_id):
    """Get a specific story"""
    result = query_db(
        'SELECT * FROM stories WHERE id = ?',
        (story_id,),
        one=True
    )
    
    if not result:
        return jsonify({'error': 'Story not found'}), 404
    
    return jsonify({
        'id': result[0],
        'project_id': result[1],
        'title': result[2],
        'description': result[3],
        'content': result[4]
    }), 200
