from flask import Flask

story_bp = __import__('app.routes.story', fromlist=['story_bp']).story_bp
animation_bp = __import__('app.routes.animation', fromlist=['animation_bp']).animation_bp
project_bp = __import__('app.routes.project', fromlist=['project_bp']).project_bp
audio_bp = __import__('app.routes.audio', fromlist=['audio_bp']).audio_bp

__all__ = ['story_bp', 'animation_bp', 'project_bp', 'audio_bp']
