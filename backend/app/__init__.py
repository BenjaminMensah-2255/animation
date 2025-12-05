from flask import Flask
from flask_cors import CORS
from app.models.database import init_db
import os

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # CORS configuration
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Ensure storage directory exists
    os.makedirs('storage/projects', exist_ok=True)
    os.makedirs('storage/videos', exist_ok=True)
    os.makedirs('storage/frames', exist_ok=True)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    from app.routes import story_bp, animation_bp, project_bp, audio_bp
    app.register_blueprint(story_bp)
    app.register_blueprint(animation_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(audio_bp)
    
    return app
