import json
import uuid
from datetime import datetime

class StoryGenerator:
    """Generate stories and scenes from user prompts or templates"""
    
    # Predefined characters for quick selection
    CHARACTERS = {
        'hero': {
            'name': 'Hero',
            'color': '#FF6B6B',
            'type': 'protagonist',
            'expressions': ['happy', 'sad', 'surprised', 'neutral']
        },
        'friend': {
            'name': 'Friend',
            'color': '#4ECDC4',
            'type': 'companion',
            'expressions': ['happy', 'sad', 'surprised', 'neutral']
        },
        'villain': {
            'name': 'Villain',
            'color': '#95E1D3',
            'type': 'antagonist',
            'expressions': ['angry', 'sneaky', 'evil', 'neutral']
        },
        'wise_one': {
            'name': 'Wise One',
            'color': '#F38181',
            'type': 'guide',
            'expressions': ['wise', 'kind', 'neutral']
        }
    }
    
    # Predefined backgrounds
    BACKGROUNDS = {
        'forest': {'color': '#90EE90', 'elements': ['trees', 'grass', 'sky']},
        'castle': {'color': '#D3D3D3', 'elements': ['walls', 'gates', 'flags']},
        'village': {'color': '#FFE4B5', 'elements': ['houses', 'paths', 'sky']},
        'mountain': {'color': '#A9A9A9', 'elements': ['rocks', 'snow', 'sky']},
        'ocean': {'color': '#87CEEB', 'elements': ['water', 'waves', 'sky']},
        'garden': {'color': '#98FB98', 'elements': ['flowers', 'paths', 'sky']}
    }
    
    @staticmethod
    def generate_from_prompt(prompt: str) -> dict:
        """Generate a story structure from a text prompt"""
        # For now, create a simple template-based story
        # In production, this would use an LLM like GPT
        
        story_id = str(uuid.uuid4())
        
        scenes = [
            {
                'id': str(uuid.uuid4()),
                'sequence': 1,
                'title': 'Introduction',
                'background': 'forest',
                'characters': [
                    {
                        'character_id': 'hero',
                        'position': {'x': 0.3, 'y': 0.7},
                        'expression': 'happy'
                    }
                ],
                'narration': f'Once upon a time... {prompt[:100]}...',
                'duration': 3.0,
                'animations': [
                    {
                        'type': 'entrance',
                        'character_id': 'hero',
                        'duration': 1.0
                    }
                ]
            },
            {
                'id': str(uuid.uuid4()),
                'sequence': 2,
                'title': 'Adventure',
                'background': 'mountain',
                'characters': [
                    {
                        'character_id': 'hero',
                        'position': {'x': 0.4, 'y': 0.7},
                        'expression': 'surprised'
                    },
                    {
                        'character_id': 'friend',
                        'position': {'x': 0.6, 'y': 0.7},
                        'expression': 'happy'
                    }
                ],
                'narration': 'The adventure begins...',
                'duration': 4.0,
                'animations': [
                    {
                        'type': 'movement',
                        'character_id': 'hero',
                        'duration': 2.0
                    }
                ]
            },
            {
                'id': str(uuid.uuid4()),
                'sequence': 3,
                'title': 'Resolution',
                'background': 'village',
                'characters': [
                    {
                        'character_id': 'hero',
                        'position': {'x': 0.5, 'y': 0.7},
                        'expression': 'happy'
                    }
                ],
                'narration': 'And they all lived happily ever after.',
                'duration': 3.0,
                'animations': [
                    {
                        'type': 'celebration',
                        'character_id': 'hero',
                        'duration': 2.0
                    }
                ]
            }
        ]
        
        return {
            'story_id': story_id,
            'title': 'Generated Adventure',
            'scenes': scenes
        }
    
    @staticmethod
    def get_available_characters() -> dict:
        """Return available predefined characters"""
        return StoryGenerator.CHARACTERS
    
    @staticmethod
    def get_available_backgrounds() -> dict:
        """Return available predefined backgrounds"""
        return StoryGenerator.BACKGROUNDS
