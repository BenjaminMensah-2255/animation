import pyttsx3
import os
import uuid
from pathlib import Path
import wave

class AudioService:
    """Generate audio and handle TTS"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Slower speech for clarity
        self.engine.setProperty('volume', 0.9)
    
    @staticmethod
    def generate_audio(text: str, scene_id: str = None) -> str:
        """Generate audio from text and return filename"""
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        filename = f"narration_{scene_id if scene_id else uuid.uuid4()}.wav"
        
        # Use correct path relative to project root
        storage_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'storage', 'audio')
        filepath = os.path.join(storage_dir, filename)
        os.makedirs(storage_dir, exist_ok=True)
        
        try:
            engine.save_to_file(text, filepath)
            engine.runAndWait()
            return filename
        except Exception as e:
            print(f"Error generating audio: {e}")
            raise
    
    @staticmethod
    def get_audio_duration(filename: str) -> float:
        """Get duration of WAV audio file"""
        try:
            filepath = os.path.join(os.getcwd(), 'storage', 'audio', filename)
            with wave.open(filepath, 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / rate
                return duration
        except Exception as e:
            print(f"Error getting audio duration: {e}")
            # Fallback: estimate based on text length if available
            return 4.0
    
    @staticmethod
    def generate_narration(text: str, filename: str = None) -> dict:
        """Generate audio from text using text-to-speech"""
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        if filename is None:
            filename = f"narration_{uuid.uuid4()}.wav"
        
        # Use correct path relative to project root
        storage_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'storage', 'audio')
        filepath = os.path.join(storage_dir, filename)
        os.makedirs(storage_dir, exist_ok=True)
        
        try:
            engine.save_to_file(text, filepath)
            engine.runAndWait()
            
            # Estimate duration (rough calculation)
            word_count = len(text.split())
            duration = word_count / 2.5  # Approximate words per second
            
            return {
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'duration': duration,
                'text': text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def estimate_duration(text: str) -> float:
        """Estimate audio duration from text"""
        # Average speaking rate: 150 words per minute
        words = len(text.split())
        return (words / 150) * 60  # Convert to seconds
    
    @staticmethod
    def generate_mouth_animation_frames(duration: float, frame_rate: int = 30) -> list:
        """Generate mouth animation frames synchronized with audio"""
        frames = int(duration * frame_rate)
        mouth_shapes = ['closed', 'open_small', 'open_medium', 'open_large']
        
        keyframes = []
        for i in range(frames):
            # Vary mouth shape based on position in audio
            shape_index = (i // 5) % len(mouth_shapes)
            keyframes.append({
                'frame': i,
                'mouth_shape': mouth_shapes[shape_index],
                'intensity': 0.5 + (0.5 * (i % 10) / 10)
            })
        
        return keyframes
