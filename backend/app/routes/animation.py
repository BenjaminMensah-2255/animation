from flask import Blueprint, request, jsonify, send_file
import uuid
from datetime import datetime
import json
import os
from app.models.database import query_db, execute_db
from app.services.animation_engine import AnimationEngine
from app.services.story_generator import StoryGenerator
from app.services.video_export import VideoExportService

animation_bp = Blueprint('animation', __name__, url_prefix='/api/animations')

@animation_bp.route('/preview/<scene_id>', methods=['GET'])
def preview_scene(scene_id):
    """Preview a scene as SVG"""
    result = query_db(
        'SELECT * FROM scenes WHERE id = ?',
        (scene_id,),
        one=True
    )
    
    if not result:
        return jsonify({'error': 'Scene not found'}), 404
    
    scene_id_db, project_id, story_id, sequence, title, background_type, characters, narration, duration, transitions, created_at = result
    
    # Parse characters data
    try:
        characters_data = json.loads(characters) if characters else []
    except:
        characters_data = []
    
    # Get character definitions
    char_defs = StoryGenerator.get_available_characters()
    char_map = {k: v for k, v in char_defs.items()}
    
    # Render frame
    scene = {
        'background_type': background_type or 'forest',
        'characters': characters_data
    }
    
    svg = AnimationEngine.render_scene_frame(scene, char_map, 0)
    
    return svg, 200, {'Content-Type': 'image/svg+xml'}

@animation_bp.route('/scenes/<scene_id>/update', methods=['POST'])
def update_scene(scene_id):
    """Update scene elements (characters, positions, expressions)"""
    data = request.json
    
    # Get current scene
    result = query_db(
        'SELECT * FROM scenes WHERE id = ?',
        (scene_id,),
        one=True
    )
    
    if not result:
        return jsonify({'error': 'Scene not found'}), 404
    
    characters = json.dumps(data.get('characters', []))
    background_type = data.get('background_type', result[4])
    narration = data.get('narration', result[7])
    
    execute_db(
        '''UPDATE scenes SET characters = ?, background_type = ?, narration = ?
           WHERE id = ?''',
        (characters, background_type, narration, scene_id)
    )
    
    return jsonify({'success': True, 'scene_id': scene_id}), 200

@animation_bp.route('/scenes/<scene_id>/delete', methods=['DELETE'])
def delete_scene(scene_id):
    """Delete a scene"""
    # Get scene first to verify it exists
    result = query_db(
        'SELECT * FROM scenes WHERE id = ?',
        (scene_id,),
        one=True
    )
    
    if not result:
        return jsonify({'error': 'Scene not found'}), 404
    
    # Delete audio tracks associated with this scene
    execute_db(
        'DELETE FROM audio_tracks WHERE scene_id = ?',
        (scene_id,)
    )
    
    # Delete the scene
    execute_db(
        'DELETE FROM scenes WHERE id = ?',
        (scene_id,)
    )
    
    return jsonify({'success': True, 'message': 'Scene deleted'}), 200

@animation_bp.route('/render', methods=['POST'])
def render_animation():
    """Render full animation as frames"""
    data = request.json
    project_id = data.get('project_id')
    
    if not project_id:
        return jsonify({'error': 'project_id required'}), 400
    
    # Get all scenes for project
    results = query_db(
        'SELECT * FROM scenes WHERE project_id = ? ORDER BY sequence',
        (project_id,)
    )
    
    if not results:
        return jsonify({'error': 'No scenes found'}), 404
    
    frames = []
    char_defs = StoryGenerator.get_available_characters()
    
    for scene_row in results:
        scene_id, _, _, sequence, background_type, characters, narration, duration, transitions, created_at = scene_row
        
        try:
            characters_data = json.loads(characters) if characters else []
        except:
            characters_data = []
        
        scene = {
            'background_type': background_type or 'forest',
            'characters': characters_data
        }
        
        # Generate frames for this scene
        num_frames = int(float(duration or 3.0) * AnimationEngine.FRAME_RATE)
        for frame_num in range(num_frames):
            svg = AnimationEngine.render_scene_frame(scene, char_defs, frame_num)
            frames.append({
                'scene_id': scene_id,
                'frame_num': frame_num,
                'svg': svg
            })
    
    return jsonify({
        'total_frames': len(frames),
        'frame_rate': AnimationEngine.FRAME_RATE,
        'preview': frames[0] if frames else None
    }), 200

@animation_bp.route('/export/<project_id>', methods=['POST'])
def export_video(project_id):
    """Export animation as MP4 video"""
    data = request.json or {}
    
    # Get project
    project_result = query_db(
        'SELECT * FROM projects WHERE id = ?',
        (project_id,),
        one=True
    )
    
    if not project_result:
        return jsonify({'error': 'Project not found'}), 404
    
    # Get all scenes
    scenes = query_db(
        'SELECT * FROM scenes WHERE project_id = ? ORDER BY sequence',
        (project_id,)
    )
    
    if not scenes:
        return jsonify({'error': 'No scenes found'}), 404
    
    try:
        frame_dir = f'storage/frames/{project_id}'
        os.makedirs(frame_dir, exist_ok=True)
        
        char_defs = StoryGenerator.get_available_characters()
        frame_count = 0
        
        # Render all frames
        for scene_row in scenes:
            scene_id, _, _, sequence, background_type, characters, narration, duration, transitions, created_at = scene_row
            
            try:
                characters_data = json.loads(characters) if characters else []
            except:
                characters_data = []
            
            scene = {
                'background_type': background_type or 'forest',
                'characters': characters_data
            }
            
            # Generate frames for this scene
            num_frames = int(float(duration or 3.0) * AnimationEngine.FRAME_RATE)
            for frame_num in range(num_frames):
                svg = AnimationEngine.render_scene_frame(scene, char_defs, frame_num)
                
                # Save as PNG (requires ImageMagick)
                png_path = os.path.join(frame_dir, f'frame_{frame_count:06d}.png')
                # VideoExportService.save_frame_as_png(svg, png_path)
                
                # For now, just count frames
                frame_count += 1
        
        # Get audio track if exists
        audio_result = query_db(
            'SELECT file_path FROM audio_tracks WHERE project_id = ? LIMIT 1',
            (project_id,),
            one=True
        )
        audio_path = audio_result[0] if audio_result else None
        
        # Create video
        output_path = f'storage/videos/{project_id}.mp4'
        os.makedirs('storage/videos', exist_ok=True)
        
        result = VideoExportService.create_video_from_frames(
            frame_dir, output_path, audio_path, 
            frame_rate=AnimationEngine.FRAME_RATE
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'video_path': output_path,
                'download_url': f'/videos/{project_id}.mp4',
                'file_size': result.get('file_size', 0),
                'message': 'Video exported successfully'
            }), 200
        else:
            return jsonify({
                'error': result.get('error', 'Export failed'),
                'message': result.get('message')
            }), 500
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error exporting video'
        }), 500
