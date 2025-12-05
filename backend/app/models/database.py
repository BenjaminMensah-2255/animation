import sqlite3
import os
import json
from datetime import datetime

DB_PATH = 'storage/projects/animation.db'

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with required tables"""
    os.makedirs('storage/projects', exist_ok=True)
    
    db = get_db()
    cursor = db.cursor()
    
    # Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            thumbnail TEXT,
            status TEXT DEFAULT 'draft'
        )
    ''')
    
    # Stories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')
    
    # Scenes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scenes (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            story_id TEXT,
            sequence INTEGER,
            title TEXT,
            background_type TEXT,
            characters TEXT,
            narration TEXT,
            duration REAL DEFAULT 3.0,
            transitions TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
    ''')
    
    # Add title column if it doesn't exist (migration for existing databases)
    cursor.execute("PRAGMA table_info(scenes)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'title' not in columns:
        cursor.execute('ALTER TABLE scenes ADD COLUMN title TEXT')
    
    # Characters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            character_type TEXT,
            appearance TEXT,
            position TEXT,
            expression TEXT DEFAULT 'neutral',
            created_at TEXT NOT NULL
        )
    ''')
    
    # Audio table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_tracks (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            scene_id TEXT,
            track_type TEXT,
            content TEXT NOT NULL,
            duration REAL,
            file_path TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (scene_id) REFERENCES scenes(id)
        )
    ''')
    
    # Animations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animations (
            id TEXT PRIMARY KEY,
            scene_id TEXT NOT NULL,
            character_id TEXT,
            animation_type TEXT,
            keyframes TEXT,
            duration REAL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (scene_id) REFERENCES scenes(id),
            FOREIGN KEY (character_id) REFERENCES characters(id)
        )
    ''')
    
    db.commit()
    db.close()

def query_db(query, args=(), one=False):
    """Query the database"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Execute a database command"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    db.commit()
    db.close()
