import json
import math
from typing import Dict, List, Tuple

class MouthShapes:
    """Mouth shapes for speech animation (visemes)"""
    SHAPES = {
        'rest': 'M -10 -18 L 10 -18',  # Neutral closed mouth
        'open': 'M -10 -18 Q 0 -12 10 -18',  # Open mouth (A, O)
        'smile': 'M -12 -18 Q 0 -12 12 -18',  # Smile
        'narrow': 'M -8 -18 L 8 -18',  # Narrow (E, I)
        'wide': 'M -14 -18 Q 0 -14 14 -18',  # Wide
        'oh': 'M -6 -18 L -6 -12 Q -6 -8 0 -8 Q 6 -8 6 -12 L 6 -18',  # O shape
        'teeth': 'M -10 -18 Q 0 -15 10 -18 M -8 -18 L -8 -16 M 0 -18 L 0 -16 M 8 -18 L 8 -16',  # Showing teeth
    }
    
    @staticmethod
    def get_mouth_for_phoneme(phoneme: str) -> str:
        """Get mouth shape based on phoneme"""
        phoneme_map = {
            'p': 'oh', 'b': 'oh', 'm': 'oh',  # Bilabial
            'a': 'open', 'o': 'oh',  # Vowels
            'e': 'narrow', 'i': 'narrow',  # Front vowels
            'u': 'oh', 'oo': 'oh',  # Back vowels
            'f': 'narrow', 'v': 'narrow',  # Fricatives
            'th': 'teeth', 't': 'narrow', 'd': 'narrow', 'n': 'narrow',  # Dentals
            'rest': 'rest'
        }
        return MouthShapes.SHAPES.get(phoneme_map.get(phoneme, 'rest'), MouthShapes.SHAPES['rest'])

class AnimationEngine:
    """Generate SVG animations and frame sequences"""
    
    FRAME_RATE = 30  # FPS for animation
    
    @staticmethod
    def create_character_svg(character: dict, position: dict, expression: str = 'neutral', mouth_shape: str = 'rest', is_speaking: bool = False) -> str:
        """Create an SVG representation of a character with animated mouth"""
        x = position.get('x', 0.5) * 1280  # Assume 1280px width
        y = position.get('y', 0.7) * 720   # Assume 720px height
        
        color = character.get('color', '#FF6B6B')
        name = character.get('name', 'Character')
        
        # Get mouth path based on shape
        mouth_path = MouthShapes.SHAPES.get(mouth_shape, MouthShapes.SHAPES['rest'])
        
        # Enhanced character with better proportions and animated mouth
        svg = f'''
        <g id="character-{name}" transform="translate({x}, {y})">
            <!-- Shadow (subtle) -->
            <ellipse cx="0" cy="72" rx="32" ry="8" fill="rgba(0,0,0,0.15)"/>
            
            <!-- Head (larger, more rounded) -->
            <circle cx="0" cy="-32" r="32" fill="{color}" stroke="#333" stroke-width="2.5"/>
            
            <!-- Hair/Top (more stylized) -->
            <path d="M -32 -38 Q -40 -55 -20 -64 Q 0 -72 20 -64 Q 40 -55 32 -38 Q 35 -45 20 -50 Q 0 -55 -20 -50 Q -35 -45 -32 -38" fill="{color}" stroke="#333" stroke-width="2"/>
            
            <!-- Cheeks (subtle blush) -->
            <circle cx="-18" cy="-25" r="8" fill="{color}" opacity="0.6"/>
            <circle cx="18" cy="-25" r="8" fill="{color}" opacity="0.6"/>
            
            <!-- Eyes (larger, more expressive) -->
            <circle cx="-14" cy="-38" r="6" fill="white" stroke="#333" stroke-width="2"/>
            <circle cx="14" cy="-38" r="6" fill="white" stroke="#333" stroke-width="2"/>
            <circle cx="-12" cy="-37" r="3.5" fill="black"/>
            <circle cx="16" cy="-37" r="3.5" fill="black"/>
            
            <!-- Eyebrows (expressive) -->
            <path d="M -18 -48 Q -14 -51 -10 -48" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
            <path d="M 10 -48 Q 14 -51 18 -48" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
            
            <!-- Nose -->
            <line x1="0" y1="-32" x2="0" y2="-20" stroke="#333" stroke-width="1.5"/>
            <circle cx="-2" cy="-18" r="2" fill="#333"/>
            <circle cx="2" cy="-18" r="2" fill="#333"/>
        '''
        
        # Add expression-based features
        if expression == 'happy':
            svg += '''
            <!-- Happy eyes (closed happy) -->
            <path d="M -20 -36 Q -14 -31 -8 -36" stroke="#333" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <path d="M 8 -36 Q 14 -31 20 -36" stroke="#333" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            '''
        elif expression == 'sad':
            svg += '''
            <!-- Sad eyes -->
            <path d="M -20 -35 L -8 -40" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
            <path d="M 8 -35 L 20 -40" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
            <!-- Tears -->
            <circle cx="-14" cy="-28" r="2.5" fill="#87CEEB"/>
            <circle cx="14" cy="-28" r="2.5" fill="#87CEEB"/>
            '''
        elif expression == 'surprised':
            svg += '''
            <!-- Surprised eyes (wide open) -->
            <circle cx="-14" cy="-38" r="8" fill="white" stroke="#333" stroke-width="2"/>
            <circle cx="14" cy="-38" r="8" fill="white" stroke="#333" stroke-width="2"/>
            <circle cx="-12" cy="-37" r="4" fill="black"/>
            <circle cx="16" cy="-37" r="4" fill="black"/>
            '''
        elif expression == 'angry':
            svg += '''
            <!-- Angry eyebrows -->
            <path d="M -18 -48 Q -14 -54 -10 -48" stroke="#333" stroke-width="3" fill="none" stroke-linecap="round"/>
            <path d="M 10 -48 Q 14 -54 18 -48" stroke="#333" stroke-width="3" fill="none" stroke-linecap="round"/>
            '''
        
        # Add animated mouth
        svg += f'''
            <!-- Mouth (animated) -->
            <path d="{mouth_path}" stroke="#333" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <!-- Mouth fill for open states -->
            {"<ellipse cx=\"0\" cy=\"-15\" rx=\"8\" ry=\"5\" fill=\"#DD6B6B\" opacity=\"0.6\"/>" if mouth_shape in ['open', 'oh', 'wide'] else ""}
            
            <!-- Body (more defined) -->
            <rect x="-20" y="5" width="40" height="50" fill="{color}" stroke="#333" stroke-width="2.5" rx="10"/>
            
            <!-- Shirt/Details (pattern) -->
            <rect x="-18" y="8" width="36" height="14" fill="#333" opacity="0.2" rx="4"/>
            <circle cx="-8" cy="15" r="2" fill="#FFD700"/>
            <circle cx="8" cy="15" r="2" fill="#FFD700"/>
            
            <!-- Arms (rounded) -->
            <line x1="-20" y1="15" x2="-48" y2="22" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
            <line x1="20" y1="15" x2="48" y2="22" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
            
            <!-- Hands (with fingers suggested) -->
            <circle cx="-48" cy="22" r="7" fill="{color}" stroke="#333" stroke-width="2"/>
            <circle cx="48" cy="22" r="7" fill="{color}" stroke="#333" stroke-width="2"/>
            
            <!-- Legs -->
            <line x1="-10" y1="55" x2="-10" y2="72" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
            <line x1="10" y1="55" x2="10" y2="72" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
            
            <!-- Shoes (stylized) -->
            <ellipse cx="-10" cy="75" rx="10" ry="6" fill="#333" stroke="#222" stroke-width="1.5"/>
            <ellipse cx="10" cy="75" rx="10" ry="6" fill="#333" stroke="#222" stroke-width="1.5"/>
            <line x1="-14" y1="75" x2="-6" y2="75" stroke="#FFD700" stroke-width="1" opacity="0.6"/>
            <line x1="6" y1="75" x2="14" y2="75" stroke="#FFD700" stroke-width="1" opacity="0.6"/>
        </g>
        '''
        
        return svg
    
    @staticmethod
    def create_background_svg(background_type: str, width: int = 1280, height: int = 720) -> str:
        """Create an SVG background with improved visuals"""
        backgrounds = {
            'forest': f'''
            <defs>
                <linearGradient id="skyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#E0F6FF;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="{width}" height="{height}" fill="url(#skyGradient)"/>
            <!-- Sun -->
            <circle cx="1100" cy="80" r="40" fill="#FFD700" opacity="0.8"/>
            <!-- Trees -->
            <g id="tree1">
                <rect x="80" y="350" width="30" height="150" fill="#8B4513"/>
                <circle cx="95" cy="300" r="70" fill="#228B22"/>
                <circle cx="55" cy="320" r="55" fill="#228B22"/>
                <circle cx="135" cy="320" r="55" fill="#228B22"/>
            </g>
            <g id="tree2" transform="translate(250, 0)">
                <rect x="80" y="350" width="30" height="150" fill="#8B4513"/>
                <circle cx="95" cy="300" r="70" fill="#2d5016"/>
                <circle cx="55" cy="320" r="55" fill="#2d5016"/>
                <circle cx="135" cy="320" r="55" fill="#2d5016"/>
            </g>
            <g id="tree3" transform="translate(500, 20)">
                <rect x="80" y="350" width="30" height="150" fill="#8B4513"/>
                <circle cx="95" cy="300" r="70" fill="#228B22"/>
                <circle cx="55" cy="320" r="55" fill="#228B22"/>
                <circle cx="135" cy="320" r="55" fill="#228B22"/>
            </g>
            <g id="tree4" transform="translate(750, 0)">
                <rect x="80" y="350" width="30" height="150" fill="#8B4513"/>
                <circle cx="95" cy="300" r="70" fill="#2d5016"/>
                <circle cx="55" cy="320" r="55" fill="#2d5016"/>
                <circle cx="135" cy="320" r="55" fill="#2d5016"/>
            </g>
            <g id="tree5" transform="translate(1000, 30)">
                <rect x="80" y="350" width="30" height="150" fill="#8B4513"/>
                <circle cx="95" cy="300" r="70" fill="#228B22"/>
                <circle cx="55" cy="320" r="55" fill="#228B22"/>
                <circle cx="135" cy="320" r="55" fill="#228B22"/>
            </g>
            <!-- Ground -->
            <rect y="500" width="{width}" height="{height-500}" fill="#90EE90"/>
            <!-- Grass detail -->
            <ellipse cx="100" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="200" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="300" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="400" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="500" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="600" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="700" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="800" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="900" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="1000" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="1100" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            <ellipse cx="1200" cy="500" rx="8" ry="12" fill="#7CCD7C"/>
            ''',
            'castle': f'''
            <defs>
                <linearGradient id="castleSkyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#4A90E2;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#87CEEB;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="{width}" height="{height}" fill="url(#castleSkyGradient)"/>
            <!-- Clouds -->
            <ellipse cx="150" cy="100" rx="60" ry="30" fill="white" opacity="0.7"/>
            <ellipse cx="200" cy="110" rx="50" ry="25" fill="white" opacity="0.7"/>
            <ellipse cx="900" cy="150" rx="70" ry="35" fill="white" opacity="0.7"/>
            <ellipse cx="970" cy="165" rx="60" ry="30" fill="white" opacity="0.7"/>
            <!-- Castle walls -->
            <rect x="350" y="200" width="580" height="300" fill="#A9A9A9" stroke="black" stroke-width="3"/>
            <!-- Tower left -->
            <rect x="280" y="180" width="100" height="360" fill="#808080" stroke="black" stroke-width="2"/>
            <polygon points="280,180 330,80 380,180" fill="#696969"/>
            <!-- Tower right -->
            <rect x="900" y="180" width="100" height="360" fill="#808080" stroke="black" stroke-width="2"/>
            <polygon points="900,180 950,80 1000,180" fill="#696969"/>
            <!-- Gate -->
            <rect x="620" y="350" width="80" height="150" fill="#4A4A4A" stroke="black" stroke-width="2"/>
            <rect x="635" y="360" width="50" height="90" fill="#2F2F2F"/>
            <!-- Flag -->
            <line x1="660" y1="100" x2="660" y2="200" stroke="black" stroke-width="3"/>
            <polygon points="660,100 660,130 720,115" fill="#FF0000"/>
            <!-- Ground -->
            <rect y="560" width="{width}" height="{height-560}" fill="#8B7355"/>
            <!-- Stone path -->
            <rect x="600" y="500" width="80" height="60" fill="#696969"/>
            <line x1="640" y1="500" x2="640" y2="560" stroke="black" stroke-width="1" opacity="0.5"/>
            <line x1="600" y1="530" x2="680" y2="530" stroke="black" stroke-width="1" opacity="0.5"/>
            ''',
            'ocean': f'''
            <defs>
                <linearGradient id="oceanSky" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#E0F6FF;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="oceanWater" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#1E90FF;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#000080;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="{width}" height="{height}" fill="url(#oceanSky)"/>
            <!-- Sun -->
            <circle cx="200" cy="100" r="50" fill="#FFD700" opacity="0.9"/>
            <!-- Birds -->
            <text x="400" y="100" font-size="20">🐦</text>
            <text x="600" y="80" font-size="20">🐦</text>
            <text x="800" y="120" font-size="20">🐦</text>
            <!-- Water -->
            <rect y="350" width="{width}" height="{height-350}" fill="url(#oceanWater)"/>
            <!-- Waves -->
            <path d="M 0 350 Q 150 330 300 350 T 600 350 T 900 350 T 1200 350 T 1500 350" stroke="white" stroke-width="3" fill="none"/>
            <path d="M 0 400 Q 150 380 300 400 T 600 400 T 900 400 T 1200 400 T 1500 400" stroke="rgba(255,255,255,0.6)" stroke-width="2" fill="none"/>
            <path d="M 0 450 Q 150 430 300 450 T 600 450 T 900 450 T 1200 450 T 1500 450" stroke="rgba(255,255,255,0.3)" stroke-width="2" fill="none"/>
            ''',
            'mountain': f'''
            <defs>
                <linearGradient id="mountainSky" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#E0F6FF;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="{width}" height="{height}" fill="url(#mountainSky)"/>
            <!-- Sun -->
            <circle cx="1050" cy="80" r="40" fill="#FFD700" opacity="0.8"/>
            <!-- Mountains -->
            <polygon points="100,600 400,200 700,600" fill="#8B7355" stroke="black" stroke-width="2"/>
            <polygon points="500,650 800,250 1100,650" fill="#A0826D" stroke="black" stroke-width="2"/>
            <polygon points="1000,600 1280,300 1560,600" fill="#8B7355" stroke="black" stroke-width="2"/>
            <!-- Snow caps -->
            <polygon points="400,200 370,280 430,280" fill="white"/>
            <polygon points="800,250 760,340 840,340" fill="white"/>
            <polygon points="1280,300 1240,400 1320,400" fill="white"/>
            <!-- Ground -->
            <rect y="600" width="{width}" height="{height-600}" fill="#90EE90"/>
            ''',
            'garden': f'''
            <defs>
                <linearGradient id="gardenSky" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#E0F6FF;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="{width}" height="{height}" fill="url(#gardenSky)"/>
            <!-- Flowers -->
            <g id="flower1" transform="translate(200, 400)">
                <circle cx="0" cy="0" r="8" fill="#FF69B4"/>
                <circle cx="0" cy="-10" r="6" fill="#FFB6C1"/>
                <circle cx="10" cy="-5" r="6" fill="#FFB6C1"/>
                <circle cx="10" cy="5" r="6" fill="#FFB6C1"/>
                <circle cx="0" cy="10" r="6" fill="#FFB6C1"/>
                <circle cx="-10" cy="5" r="6" fill="#FFB6C1"/>
                <circle cx="-10" cy="-5" r="6" fill="#FFB6C1"/>
                <line x1="0" y1="0" x2="0" y2="30" stroke="#228B22" stroke-width="2"/>
            </g>
            <g id="flower2" transform="translate(500, 420)">
                <circle cx="0" cy="0" r="8" fill="#FFD700"/>
                <circle cx="0" cy="-10" r="6" fill="#FFFF00"/>
                <circle cx="10" cy="-5" r="6" fill="#FFFF00"/>
                <circle cx="10" cy="5" r="6" fill="#FFFF00"/>
                <circle cx="0" cy="10" r="6" fill="#FFFF00"/>
                <circle cx="-10" cy="5" r="6" fill="#FFFF00"/>
                <circle cx="-10" cy="-5" r="6" fill="#FFFF00"/>
                <line x1="0" y1="0" x2="0" y2="30" stroke="#228B22" stroke-width="2"/>
            </g>
            <g id="flower3" transform="translate(800, 410)">
                <circle cx="0" cy="0" r="8" fill="#FF1493"/>
                <circle cx="0" cy="-10" r="6" fill="#FF69B4"/>
                <circle cx="10" cy="-5" r="6" fill="#FF69B4"/>
                <circle cx="10" cy="5" r="6" fill="#FF69B4"/>
                <circle cx="0" cy="10" r="6" fill="#FF69B4"/>
                <circle cx="-10" cy="5" r="6" fill="#FF69B4"/>
                <circle cx="-10" cy="-5" r="6" fill="#FF69B4"/>
                <line x1="0" y1="0" x2="0" y2="30" stroke="#228B22" stroke-width="2"/>
            </g>
            <g id="flower4" transform="translate(1100, 400)">
                <circle cx="0" cy="0" r="8" fill="#9370DB"/>
                <circle cx="0" cy="-10" r="6" fill="#DDA0DD"/>
                <circle cx="10" cy="-5" r="6" fill="#DDA0DD"/>
                <circle cx="10" cy="5" r="6" fill="#DDA0DD"/>
                <circle cx="0" cy="10" r="6" fill="#DDA0DD"/>
                <circle cx="-10" cy="5" r="6" fill="#DDA0DD"/>
                <circle cx="-10" cy="-5" r="6" fill="#DDA0DD"/>
                <line x1="0" y1="0" x2="0" y2="30" stroke="#228B22" stroke-width="2"/>
            </g>
            <!-- Path -->
            <rect x="580" y="450" width="120" height="250" fill="#D2B48C" stroke="#8B7355" stroke-width="2"/>
            <!-- Ground -->
            <rect y="500" width="{width}" height="{height-500}" fill="#90EE90"/>
            '''
        }
        
        return f'{backgrounds.get(background_type, backgrounds["forest"])}'
    
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
        """Render a single frame of a scene as SVG with dialogue and animated mouths"""
        svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
        
        # Add background
        svg += AnimationEngine.create_background_svg(scene.get('background_type', 'forest'), width, height)
        
        # Get narration and determine speaking character
        narration = scene.get('narration', '')
        is_speaking_frame = frame_num > 0  # Character speaks for most of scene
        
        # Add characters with animations applied
        scene_characters = scene.get('characters', [])
        if isinstance(scene_characters, str):
            try:
                scene_characters = json.loads(scene_characters)
            except:
                scene_characters = []
        
        for idx, char_ref in enumerate(scene_characters):
            # Handle both character ID strings and full character data objects
            if isinstance(char_ref, str):
                char_id = char_ref
                character = characters.get(char_id, {})
                if 'name' not in character:
                    character['name'] = char_id
                if 'color' not in character:
                    character['color'] = '#FF6B6B'
                # Position characters side by side
                position = {'x': 0.3 + (idx * 0.2), 'y': 0.65}
                expression = 'neutral'
            else:
                char_id = char_ref.get('character_id', str(idx))
                character = characters.get(char_id, {})
                if 'name' not in character:
                    character['name'] = char_ref.get('name', char_id)
                if 'color' not in character:
                    character['color'] = char_ref.get('color', '#FF6B6B')
                position = char_ref.get('position', {'x': 0.3 + (idx * 0.2), 'y': 0.65})
                expression = char_ref.get('expression', 'neutral')
            
            # Determine mouth shape based on narration and frame
            mouth_shape = 'rest'
            if is_speaking_frame and narration:
                # Animate mouth based on narration text and frame
                phoneme_index = (frame_num // 3) % len(narration)
                mouth_shape = MouthShapes.get_mouth_for_phoneme(narration[phoneme_index].lower())
            
            svg += AnimationEngine.create_character_svg(character, position, expression, mouth_shape, is_speaking_frame)
            
            # Add speech bubble with narration (first character speaks)
            if idx == 0 and narration:
                svg += AnimationEngine.create_speech_bubble(narration, position, character.get('color', '#FF6B6B'))
        
        svg += '</svg>'
        return svg
    
    @staticmethod
    def create_speech_bubble(text: str, position: dict, character_color: str, max_width: int = 200) -> str:
        """Create a speech bubble with text"""
        # Calculate position
        bubble_x = position.get('x', 0.5) * 1280 - 100
        bubble_y = position.get('y', 0.7) * 720 - 180
        
        # Word wrapping
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 25:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limit to 3 lines
        lines = lines[:3]
        text_to_display = '\n'.join(lines)
        
        # Speech bubble dimensions
        bubble_width = 200
        bubble_height = 30 + (len(lines) * 18)
        
        svg = f'''
        <!-- Speech Bubble -->
        <g id="speech-bubble">
            <!-- Bubble background (rounded rectangle) -->
            <rect x="{bubble_x}" y="{bubble_y}" width="{bubble_width}" height="{bubble_height}" 
                  rx="12" ry="12" fill="white" stroke="#333" stroke-width="2" opacity="0.95"/>
            
            <!-- Pointer tail -->
            <polygon points="{bubble_x + 20},{bubble_y + bubble_height} {bubble_x + 40},{bubble_y + bubble_height + 15} {bubble_x + 50},{bubble_y + bubble_height}" 
                     fill="white" stroke="#333" stroke-width="2"/>
            
            <!-- Text (with line breaks) -->
        '''
        
        # Add text lines
        for i, line in enumerate(lines):
            text_y = bubble_y + 22 + (i * 18)
            # Escape XML special characters
            line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            svg += f'<text x="{bubble_x + 10}" y="{text_y}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#333">{line}</text>\n'
        
        svg += '''
        </g>
        '''
        return svg

