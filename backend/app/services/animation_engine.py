import json
import math
from typing import Dict, List, Tuple

class AnimationEngine:
    """Generate SVG animations and frame sequences"""
    
    FRAME_RATE = 30  # FPS for animation
    
    @staticmethod
    def create_character_svg(character: dict, position: dict, expression: str = 'neutral') -> str:
        """Create an SVG representation of a character"""
        x = position.get('x', 0.5) * 1280  # Assume 1280px width
        y = position.get('y', 0.7) * 720   # Assume 720px height
        
        color = character.get('color', '#FF6B6B')
        name = character.get('name', 'Character')
        
        svg = f'''
        <g id="character-{name}" transform="translate({x}, {y})">
            <!-- Head -->
            <circle cx="0" cy="-30" r="25" fill="{color}" stroke="black" stroke-width="2"/>
            
            <!-- Eyes -->
            <circle cx="-10" cy="-35" r="4" fill="black"/>
            <circle cx="10" cy="-35" r="4" fill="black"/>
        '''
        
        # Add expression-based features
        if expression == 'happy':
            svg += '''
            <!-- Happy mouth -->
            <path d="M -8 -22 Q 0 -18 8 -22" stroke="black" stroke-width="2" fill="none"/>
            '''
        elif expression == 'sad':
            svg += '''
            <!-- Sad mouth -->
            <path d="M -8 -18 Q 0 -22 8 -18" stroke="black" stroke-width="2" fill="none"/>
            '''
        elif expression == 'surprised':
            svg += '''
            <!-- Surprised mouth -->
            <circle cx="0" cy="-20" r="3" fill="black"/>
            '''
        
        svg += '''
            <!-- Body -->
            <rect x="-15" y="0" width="30" height="40" fill="{}" stroke="black" stroke-width="2" rx="5"/>
            
            <!-- Arms -->
            <line x1="-15" y1="10" x2="-35" y2="15" stroke="{}" stroke-width="3" stroke-linecap="round"/>
            <line x1="15" y1="10" x2="35" y2="15" stroke="{}" stroke-width="3" stroke-linecap="round"/>
            
            <!-- Legs -->
            <line x1="-8" y1="40" x2="-8" y2="55" stroke="{}" stroke-width="3" stroke-linecap="round"/>
            <line x1="8" y1="40" x2="8" y2="55" stroke="{}" stroke-width="3" stroke-linecap="round"/>
        </g>
        '''.format(color, color, color, color, color)
        
        return svg
    
    @staticmethod
    def create_background_svg(background_type: str, width: int = 1280, height: int = 720) -> str:
        """Create an SVG background"""
        backgrounds = {
            'forest': f'''
            <rect width="{width}" height="{height}" fill="#87CEEB"/>
            <ellipse cx="100" cy="300" rx="50" ry="150" fill="#228B22"/>
            <ellipse cx="300" cy="250" rx="60" ry="160" fill="#228B22"/>
            <ellipse cx="500" cy="280" rx="55" ry="155" fill="#228B22"/>
            <ellipse cx="700" cy="260" rx="65" ry="165" fill="#228B22"/>
            <ellipse cx="900" cy="290" rx="50" ry="150" fill="#228B22"/>
            <ellipse cx="1100" cy="270" rx="60" ry="160" fill="#228B22"/>
            <rect y="500" width="{width}" height="{height-500}" fill="#90EE90"/>
            ''',
            'castle': f'''
            <rect width="{width}" height="{height}" fill="#87CEEB"/>
            <rect x="400" y="200" width="480" height="300" fill="#D3D3D3" stroke="black" stroke-width="2"/>
            <polygon points="400,200 440,100 480,200" fill="#8B0000"/>
            <polygon points="720,200 760,100 800,200" fill="#8B0000"/>
            <polygon points="1040,200 1080,100 1120,200" fill="#8B0000"/>
            <rect x="450" y="250" width="40" height="100" fill="#4A4A4A"/>
            <rect x="750" y="250" width="40" height="100" fill="#4A4A4A"/>
            <rect y="500" width="{width}" height="{height-500}" fill="#8B7355"/>
            ''',
            'ocean': f'''
            <rect width="{width}" height="{height}" fill="#87CEEB"/>
            <rect y="400" width="{width}" height="{height-400}" fill="#1E90FF"/>
            <path d="M 0 400 Q 150 380 300 400 T 600 400 T 900 400 T 1200 400 T 1500 400" stroke="white" stroke-width="2" fill="none"/>
            <path d="M 0 450 Q 150 430 300 450 T 600 450 T 900 450 T 1200 450 T 1500 450" stroke="white" stroke-width="1" fill="none" opacity="0.5"/>
            '''
        }
        
        return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">{backgrounds.get(background_type, backgrounds["forest"])}</svg>'
    
    @staticmethod
    def generate_keyframes(animation_type: str, duration: float, start_pos: dict, end_pos: dict = None) -> List[dict]:
        """Generate keyframes for an animation"""
        frames = int(duration * AnimationEngine.FRAME_RATE)
        keyframes = []
        
        if animation_type == 'entrance':
            # Fade in and slide from left
            for i in range(frames):
                progress = i / frames
                keyframes.append({
                    'frame': i,
                    'x': start_pos['x'] + (progress * 0.1),
                    'y': start_pos['y'],
                    'opacity': progress,
                    'rotation': 0
                })
        
        elif animation_type == 'movement':
            # Move from start to end position
            end = end_pos or {'x': start_pos['x'] + 0.2, 'y': start_pos['y']}
            for i in range(frames):
                progress = i / frames
                keyframes.append({
                    'frame': i,
                    'x': start_pos['x'] + (end['x'] - start_pos['x']) * progress,
                    'y': start_pos['y'] + (end['y'] - start_pos['y']) * progress,
                    'opacity': 1.0,
                    'rotation': 0
                })
        
        elif animation_type == 'celebration':
            # Bounce and spin
            for i in range(frames):
                progress = i / frames
                bounce = math.sin(progress * math.pi * 3) * 0.1
                keyframes.append({
                    'frame': i,
                    'x': start_pos['x'],
                    'y': start_pos['y'] - bounce,
                    'opacity': 1.0,
                    'rotation': (progress * 360) % 360
                })
        
        elif animation_type == 'expression_change':
            # Static position, just expression changes
            for i in range(frames):
                keyframes.append({
                    'frame': i,
                    'x': start_pos['x'],
                    'y': start_pos['y'],
                    'opacity': 1.0,
                    'rotation': 0
                })
        
        return keyframes
    
    @staticmethod
    def render_scene_frame(scene: dict, characters: dict, frame_num: int, width: int = 1280, height: int = 720) -> str:
        """Render a single frame of a scene as SVG"""
        svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
        
        # Add background
        svg += AnimationEngine.create_background_svg(scene.get('background_type', 'forest'), width, height)
        
        # Add characters with animations applied
        for char_data in scene.get('characters', []):
            char_id = char_data.get('character_id')
            character = characters.get(char_id, {})
            position = char_data.get('position', {'x': 0.5, 'y': 0.7})
            expression = char_data.get('expression', 'neutral')
            
            svg += AnimationEngine.create_character_svg(character, position, expression)
        
        svg += '</svg>'
        return svg
