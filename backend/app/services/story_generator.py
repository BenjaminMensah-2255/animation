import json
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

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
        """Generate a story structure from a text prompt using Google Gemini AI"""
        story_id = str(uuid.uuid4())
        
        try:
            # Get Google API key from environment
            api_key = os.getenv('GOOGLE_API_KEY')
            print(f"DEBUG: API Key set: {bool(api_key)}")
            print(f"DEBUG: API Key (first 20 chars): {api_key[:20] if api_key else 'None'}")
            
            if not api_key:
                raise ValueError('GOOGLE_API_KEY not set in environment')
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            print(f"DEBUG: Calling Gemini with prompt: {prompt[:50]}...")
            
            # Generate narration for 3 scenes using Gemini
            response = model.generate_content(f"""Create a children's story with 3 scenes based on this prompt: {prompt}

Return ONLY a JSON object (no other text) with this exact structure:
{{
  "title": "Story Title",
  "scenes": [
    {{
      "title": "Scene 1 Title",
      "background": "forest",
      "characters": ["hero", "friend"],
      "narration": "2-3 sentences of engaging narration for this scene"
    }},
    {{
      "title": "Scene 2 Title",
      "background": "mountain",
      "characters": ["hero", "friend", "villain"],
      "narration": "2-3 sentences showing development"
    }},
    {{
      "title": "Scene 3 Title",
      "background": "village",
      "characters": ["hero", "friend"],
      "narration": "2-3 sentences with happy ending"
    }}
  ]
}}

Make the story engaging for children. Each scene's narration should relate to and build upon the prompt: {prompt}
The narration should be different for each scene and directly connected to the story prompt.""")
            
            print(f"DEBUG: Gemini response received")
            story_content = response.text.strip()
            print(f"DEBUG: Response (first 100 chars): {story_content[:100]}")
            
            # Clean up markdown code blocks if present
            if story_content.startswith('```'):
                story_content = story_content.split('```')[1]
                if story_content.startswith('json'):
                    story_content = story_content[4:]
            if story_content.endswith('```'):
                story_content = story_content[:-3]
            
            story_json = json.loads(story_content.strip())
            print(f"DEBUG: JSON parsed successfully")
            
            scenes = []
            for idx, scene_data in enumerate(story_json.get('scenes', []), 1):
                characters_list = []
                char_names = scene_data.get('characters', [])
                
                # Position characters across the scene
                positions = [
                    {'x': 0.2, 'y': 0.7},
                    {'x': 0.5, 'y': 0.7},
                    {'x': 0.8, 'y': 0.7},
                    {'x': 0.35, 'y': 0.6}
                ]
                
                for pos_idx, char_name in enumerate(char_names):
                    if char_name in StoryGenerator.CHARACTERS:
                        characters_list.append({
                            'character_id': char_name,
                            'position': positions[min(pos_idx, len(positions) - 1)],
                            'expression': 'happy'
                        })
                
                scene = {
                    'id': str(uuid.uuid4()),
                    'sequence': idx,
                    'title': scene_data.get('title', f'Scene {idx}'),
                    'background': scene_data.get('background', 'forest'),
                    'characters': characters_list,
                    'narration': scene_data.get('narration', ''),
                    'duration': 4.0,
                    'animations': [
                        {
                            'type': 'entrance',
                            'character_id': characters_list[0]['character_id'] if characters_list else 'hero',
                            'duration': 1.0
                        }
                    ]
                }
                scenes.append(scene)
            
            print(f"DEBUG: Story generated successfully with Gemini")
            return {
                'story_id': story_id,
                'title': story_json.get('title', 'Generated Adventure'),
                'scenes': scenes
            }
            
        except Exception as e:
            print(f"ERROR generating story with Gemini: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            print(f"DEBUG: Using fallback story generation")
            return StoryGenerator._generate_fallback_story(prompt, story_id)
            
            response = client.chat.completions.create(
                model="gemma2-9b-it",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Create a children's story with 3 scenes based on this prompt: {prompt}
                        
Return ONLY a JSON object (no other text) with this exact structure:
{{
  "title": "Story Title",
  "scenes": [
    {{
      "title": "Scene 1 Title",
      "background": "forest|castle|village|mountain|ocean|garden",
      "characters": ["hero", "friend", "villain", "wise_one"],
      "narration": "2-3 sentences of narration for this scene"
    }},
    {{
      "title": "Scene 2 Title",
      "background": "mountain|ocean|village|forest|castle|garden",
      "characters": ["hero", "friend"],
      "narration": "2-3 sentences of narration for this scene"
    }},
    {{
      "title": "Scene 3 Title",
      "background": "village|castle|garden|forest|mountain|ocean",
      "characters": ["hero"],
      "narration": "2-3 sentences of narration for this scene"
    }}
  ]
}}

Make it engaging for children, with clear story progression and 2-3 sentences per scene narration."""
                    }
                ]
            )
            
            story_content = response.choices[0].message.content.strip()
            
            if story_content.startswith('```'):
                story_content = story_content.split('```')[1]
                if story_content.startswith('json'):
                    story_content = story_content[4:]
            if story_content.endswith('```'):
                story_content = story_content[:-3]
            
            story_json = json.loads(story_content.strip())
            
            scenes = []
            for idx, scene_data in enumerate(story_json.get('scenes', []), 1):
                characters_list = []
                char_names = scene_data.get('characters', [])
                
                positions = [
                    {'x': 0.2, 'y': 0.7},
                    {'x': 0.5, 'y': 0.7},
                    {'x': 0.8, 'y': 0.7},
                    {'x': 0.35, 'y': 0.6}
                ]
                
                for pos_idx, char_name in enumerate(char_names):
                    if char_name in StoryGenerator.CHARACTERS:
                        characters_list.append({
                            'character_id': char_name,
                            'position': positions[min(pos_idx, len(positions) - 1)],
                            'expression': 'happy'
                        })
                
                scene = {
                    'id': str(uuid.uuid4()),
                    'sequence': idx,
                    'title': scene_data.get('title', f'Scene {idx}'),
                    'background': scene_data.get('background', 'forest'),
                    'characters': characters_list,
                    'narration': scene_data.get('narration', ''),
                    'duration': 4.0,
                    'animations': [
                        {
                            'type': 'entrance',
                            'character_id': characters_list[0]['character_id'] if characters_list else 'hero',
                            'duration': 1.0
                        }
                    ]
                }
                scenes.append(scene)
            
            return {
                'story_id': story_id,
                'title': story_json.get('title', 'Generated Adventure'),
                'scenes': scenes
            }
            
        except Exception as e:
            print(f"Error generating story with Groq: {e}")
            return StoryGenerator._generate_fallback_story(prompt, story_id)
    
    @staticmethod
    def _generate_fallback_story(prompt: str, story_id: str) -> dict:
        """Enhanced template-based story generation with intelligent narration"""
        # Parse the prompt to make better narration
        scenes = []
        
        # Scene 1: Introduction
        scene1_title = "The Beginning"
        scene1_narration = f"Once upon a time, {prompt}. It was a beautiful day in the garden, and our adventure was about to begin."
        
        # Scene 2: Development  
        scene2_title = "The Adventure"
        scene2_narration = f"As the story unfolded, unexpected challenges appeared. But our brave character didn't give up, and continued through the adventure with determination and hope."
        
        # Scene 3: Conclusion
        scene3_title = "The Happy Ending"
        scene3_narration = "Through courage and friendship, the day was saved. And so, everyone celebrated the wonderful adventure they shared together."
        
        scenes = [
            {
                'id': str(uuid.uuid4()),
                'sequence': 1,
                'title': scene1_title,
                'background': 'garden',
                'characters': [
                    {
                        'character_id': 'hero',
                        'position': {'x': 0.3, 'y': 0.7},
                        'expression': 'happy'
                    }
                ],
                'narration': scene1_narration,
                'duration': 4.0,
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
                'title': scene2_title,
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
                'narration': scene2_narration,
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
                'title': scene3_title,
                'background': 'village',
                'characters': [
                    {
                        'character_id': 'hero',
                        'position': {'x': 0.5, 'y': 0.7},
                        'expression': 'happy'
                    },
                    {
                        'character_id': 'friend',
                        'position': {'x': 0.4, 'y': 0.7},
                        'expression': 'happy'
                    }
                ],
                'narration': scene3_narration,
                'duration': 4.0,
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
            'title': prompt[:50] + '...' if len(prompt) > 50 else prompt,
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
