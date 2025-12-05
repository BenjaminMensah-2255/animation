from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime
import json
from app.models.database import query_db, execute_db
from app.services.story_generator import StoryGenerator

project_bp = Blueprint('project', __name__, url_prefix='/api/projects')

@project_bp.route('/create', methods=['POST'])
def create_project():
    """Create a new animation project"""
    data = request.json
    project_id = str(uuid.uuid4())
    name = data.get('name', 'Untitled Project')
    description = data.get('description', '')
    
    now = datetime.now().isoformat()
    
    execute_db(
        '''INSERT INTO projects (id, name, description, created_at, updated_at, status)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (project_id, name, description, now, now, 'draft')
    )
    
    return jsonify({
        'project_id': project_id,
        'name': name,
        'description': description,
        'created_at': now
    }), 201

@project_bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get project details"""
    result = query_db(
        'SELECT * FROM projects WHERE id = ?',
        (project_id,),
        one=True
    )
    
    if not result:
        return jsonify({'error': 'Project not found'}), 404
    
    proj_id, name, description, created_at, updated_at, thumbnail, status = result
    
    # Get associated stories
    stories = query_db(
        'SELECT id, title FROM stories WHERE project_id = ?',
        (project_id,)
    )
    
    # Get associated scenes
    scenes = query_db(
        'SELECT id, sequence, background_type, title, narration FROM scenes WHERE project_id = ? ORDER BY sequence',
        (project_id,)
    )
    
    return jsonify({
        'id': proj_id,
        'name': name,
        'description': description,
        'created_at': created_at,
        'updated_at': updated_at,
        'status': status,
        'stories': [{'id': s[0], 'title': s[1]} for s in stories],
        'scenes': [{'id': s[0], 'sequence': s[1], 'background': s[2], 'title': s[3], 'narration': s[4]} for s in scenes]
    }), 200

@project_bp.route('', methods=['GET'])
def list_projects():
    """List all projects"""
    results = query_db(
        'SELECT id, name, description, created_at, updated_at, status FROM projects ORDER BY updated_at DESC'
    )
    
    projects = []
    for row in results:
        projects.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'created_at': row[3],
            'updated_at': row[4],
            'status': row[5]
        })
    
    return jsonify(projects), 200

@project_bp.route('/<project_id>/update', methods=['PUT'])
def update_project(project_id):
    """Update project details"""
    data = request.json
    
    execute_db(
        '''UPDATE projects SET name = ?, description = ?, updated_at = ?
           WHERE id = ?''',
        (data.get('name'), data.get('description'), datetime.now().isoformat(), project_id)
    )
    
    return jsonify({'success': True, 'project_id': project_id}), 200

@project_bp.route('/<project_id>/delete', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project and all associated data"""
    execute_db('DELETE FROM animations WHERE scene_id IN (SELECT id FROM scenes WHERE project_id = ?)', (project_id,))
    execute_db('DELETE FROM audio_tracks WHERE project_id = ?', (project_id,))
    execute_db('DELETE FROM scenes WHERE project_id = ?', (project_id,))
    execute_db('DELETE FROM stories WHERE project_id = ?', (project_id,))
    execute_db('DELETE FROM projects WHERE id = ?', (project_id,))
    
    return jsonify({'success': True}), 200

@project_bp.route('/<project_id>/scenes/create', methods=['POST'])
def create_scene(project_id):
    """Create a scene in a project"""
    data = request.json
    scene_id = str(uuid.uuid4())
    
    scene = {
        'background_type': data.get('background_type', 'forest'),
        'characters': data.get('characters', []),
        'narration': data.get('narration', ''),
        'duration': data.get('duration', 3.0),
        'transitions': json.dumps(data.get('transitions', {})),
        'title': data.get('title', '')
    }
    
    execute_db(
        '''INSERT INTO scenes (id, project_id, sequence, title, background_type, characters, narration, duration, transitions, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (scene_id, project_id, data.get('sequence', 1), scene['title'], scene['background_type'], 
         json.dumps(scene['characters']), scene['narration'], scene['duration'],
         scene['transitions'], datetime.now().isoformat())
    )
    
    return jsonify({
        'scene_id': scene_id,
        'project_id': project_id,
        'sequence': data.get('sequence', 1)
    }), 201
