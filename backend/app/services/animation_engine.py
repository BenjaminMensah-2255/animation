import json
import math
from typing import Dict, List, Tuple

class AnimationEngine:
    """Generate SVG animations and frame sequences"""
    
    FRAME_RATE = 30  # FPS for animation
    
    @staticmethod
    def create_character_svg(character: dict, position: dict, expression: str = 'neutral') -> str:
        """Create an SVG representation of a character with improved visuals"""
        x = position.get('x', 0.5) * 1280  # Assume 1280px width
        y = position.get('y', 0.7) * 720   # Assume 720px height
        
        color = character.get('color', '#FF6B6B')
        name = character.get('name', 'Character')
        
        # Enhanced character with better proportions
        svg = f'''
        <g id="character-{name}" transform="translate({x}, {y})">
            <!-- Shadow -->
            <ellipse cx="0" cy="70" rx="30" ry="8" fill="rgba(0,0,0,0.2)"/>
            
            <!-- Head -->
            <circle cx="0" cy="-30" r="28" fill="{color}" stroke="black" stroke-width="2.5"/>
            
            <!-- Hair/Top -->
            <path d="M -28 -35 Q -35 -50 -20 -58 Q 0 -65 20 -58 Q 35 -50 28 -35" fill="{color}" stroke="black" stroke-width="2"/>
            
            <!-- Eyes -->
            <circle cx="-12" cy="-35" r="5" fill="white" stroke="black" stroke-width="1.5"/>
            <circle cx="12" cy="-35" r="5" fill="white" stroke="black" stroke-width="1.5"/>
            <circle cx="-10" cy="-34" r="3" fill="black"/>
            <circle cx="14" cy="-34" r="3" fill="black"/>
        '''
        
        # Add expression-based features
        if expression == 'happy':
            svg += '''
            <!-- Happy eyes (closed happy) -->
            <path d="M -18 -32 Q -12 -28 -6 -32" stroke="black" stroke-width="2" fill="none"/>
            <path d="M 6 -32 Q 12 -28 18 -32" stroke="black" stroke-width="2" fill="none"/>
            <!-- Happy mouth (curved smile) -->
            <path d="M -12 -18 Q 0 -12 12 -18" stroke="black" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            '''
        elif expression == 'sad':
            svg += '''
            <!-- Sad eyes -->
            <path d="M -18 -30 L -6 -34" stroke="black" stroke-width="2" fill="none" stroke-linecap="round"/>
            <path d="M 6 -30 L 18 -34" stroke="black" stroke-width="2" fill="none" stroke-linecap="round"/>
            <!-- Sad mouth (downward curve) -->
            <path d="M -12 -14 Q 0 -20 12 -14" stroke="black" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <!-- Tears -->
            <circle cx="-12" cy="-25" r="2" fill="#87CEEB"/>
            <circle cx="12" cy="-25" r="2" fill="#87CEEB"/>
            '''
        elif expression == 'surprised':
            svg += '''
            <!-- Surprised eyes (wide open) -->
            <circle cx="-12" cy="-35" r="7" fill="white" stroke="black" stroke-width="2"/>
            <circle cx="12" cy="-35" r="7" fill="white" stroke="black" stroke-width="2"/>
            <circle cx="-12" cy="-34" r="4" fill="black"/>
            <circle cx="12" cy="-34" r="4" fill="black"/>
            <!-- Surprised mouth (O shape) -->
            <circle cx="0" cy="-18" r="6" fill="none" stroke="black" stroke-width="2.5"/>
            '''
        elif expression == 'angry':
            svg += '''
            <!-- Angry eyes -->
            <path d="M -18 -32 L -6 -38" stroke="black" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <path d="M 6 -38 L 18 -32" stroke="black" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <!-- Angry mouth (straight line) -->
            <line x1="-12" y1="-15" x2="12" y2="-15" stroke="black" stroke-width="2.5" stroke-linecap="round"/>
            <!-- Angry eyebrows/marks -->
            <line x1="-15" y1="-42" x2="-8" y2="-40" stroke="black" stroke-width="2"/>
            <line x1="15" y1="-42" x2="8" y2="-40" stroke="black" stroke-width="2"/>
            '''
        else:  # neutral
            svg += '''
            <!-- Neutral mouth -->
            <line x1="-10" y1="-18" x2="10" y2="-18" stroke="black" stroke-width="2" stroke-linecap="round"/>
            '''
        
        svg += f'''
            <!-- Body -->
            <rect x="-18" y="0" width="36" height="45" fill="{color}" stroke="black" stroke-width="2.5" rx="8"/>
            
            <!-- Shirt/Details -->
            <rect x="-16" y="2" width="32" height="12" fill="{color}" opacity="0.8" stroke="black" stroke-width="1.5"/>
            
            <!-- Arms -->
            <line x1="-18" y1="12" x2="-42" y2="18" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            <line x1="18" y1="12" x2="42" y2="18" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            
            <!-- Hands -->
            <circle cx="-42" cy="18" r="6" fill="{color}" stroke="black" stroke-width="2"/>
            <circle cx="42" cy="18" r="6" fill="{color}" stroke="black" stroke-width="2"/>
            
            <!-- Legs -->
            <line x1="-10" y1="45" x2="-10" y2="65" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            <line x1="10" y1="45" x2="10" y2="65" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
            
            <!-- Shoes -->
            <ellipse cx="-10" cy="68" rx="8" ry="5" fill="black" stroke="black" stroke-width="1.5"/>
            <ellipse cx="10" cy="68" rx="8" ry="5" fill="black" stroke="black" stroke-width="1.5"/>
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
