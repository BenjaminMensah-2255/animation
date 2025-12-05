import os
import subprocess
import json
from pathlib import Path

class VideoExportService:
    """Export rendered frames and audio to MP4 video"""
    
    FRAME_RATE = 30
    
    @staticmethod
    def save_frame_as_png(svg_content: str, filepath: str, width: int = 1280, height: int = 720) -> bool:
        """Convert SVG to PNG using ImageMagick or similar"""
        try:
            # Create temporary SVG file
            svg_path = filepath.replace('.png', '.svg')
            with open(svg_path, 'w') as f:
                f.write(svg_content)
            
            # Convert SVG to PNG
            # Note: This requires ImageMagick to be installed: convert command
            cmd = f'convert "{svg_path}" "{filepath}"'
            result = subprocess.run(cmd, shell=True, capture_output=True)
            
            # Clean up SVG
            os.remove(svg_path)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error saving frame: {e}")
            return False
    
    @staticmethod
    def create_video_from_frames(frame_dir: str, output_path: str, audio_path: str = None, 
                                frame_rate: int = 30, width: int = 1280, height: int = 720) -> dict:
        """Create MP4 video from PNG frames using FFmpeg"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Command to create video from frames
            frame_pattern = os.path.join(frame_dir, 'frame_%06d.png')
            cmd = [
                'ffmpeg',
                '-framerate', str(frame_rate),
                '-i', frame_pattern,
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-preset', 'slow',
                '-y',  # Overwrite output file
                output_path
            ]
            
            # Add audio if provided
            if audio_path and os.path.exists(audio_path):
                cmd.extend(['-i', audio_path, '-c:a', 'aac', '-shortest'])
            
            # Run FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                file_size = os.path.getsize(output_path)
                return {
                    'success': True,
                    'output_path': output_path,
                    'file_size': file_size,
                    'message': 'Video exported successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'message': 'FFmpeg conversion failed'
                }
        
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'FFmpeg not found. Please install FFmpeg and add it to PATH.',
                'message': 'FFmpeg not installed'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error creating video'
            }
    
    @staticmethod
    def merge_audio_video(video_path: str, audio_path: str, output_path: str) -> dict:
        """Merge audio track with existing video"""
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output_path': output_path,
                    'message': 'Audio merged successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def estimate_video_duration(frame_count: int, frame_rate: int = 30) -> float:
        """Estimate video duration from frame count"""
        return frame_count / frame_rate
