# Cartoon Animation Studio - Complete Setup Guide

## Overview

This is a full-stack animated story creation platform built with:
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Backend**: Python Flask, SQLite
- **Features**: Story generation, SVG character animation, TTS audio, frame rendering, video export

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- FFmpeg (for video export)
- Windows PowerShell or bash terminal

## Installation

### 1. Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# or: source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.models.database import init_db; init_db()"

# Start server
python run.py
```

Backend runs on: `http://localhost:5000`

### 2. Frontend Setup

```powershell
# From project root
npm install

# Create .env.local
echo NEXT_PUBLIC_API_URL=http://localhost:5000/api > .env.local

# Start dev server
npm run dev
```

Frontend runs on: `http://localhost:3000`

### 3. Run Both Together (Optional)

```powershell
npm run dev:all
```

## Project Structure

```
animation/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx                    # Home/landing
│   │   ├── projects/
│   │   │   ├── page.tsx               # Project list
│   │   │   └── new/page.tsx           # Create project
│   │   └── editor/[id]/page.tsx       # Scene editor
│   ├── components/
│   │   ├── StoryCreator.tsx           # Story generation
│   │   ├── SceneEditor.tsx            # Edit scenes
│   │   ├── CharacterSelector.tsx      # Add/position characters
│   │   ├── AudioGenerator.tsx         # TTS generation
│   │   └── AnimationViewer.tsx        # Preview/playback
│   └── lib/api.ts                     # API client
├── backend/
│   ├── app/
│   │   ├── __init__.py               # App factory
│   │   ├── models/database.py        # Database setup
│   │   ├── services/
│   │   │   ├── story_generator.py    # Story templates
│   │   │   ├── animation_engine.py   # SVG rendering
│   │   │   └── audio_service.py      # TTS + mouth animation
│   │   └── routes/
│   │       ├── project.py            # Project endpoints
│   │       ├── story.py              # Story endpoints
│   │       ├── animation.py          # Animation endpoints
│   │       └── audio.py              # Audio endpoints
│   ├── run.py                        # Flask entry point
│   └── requirements.txt              # Python dependencies
└── package.json
```

## API Documentation

### Projects Endpoints

**Create Project**
```
POST /api/projects/create
Body: { "name": "My Animation", "description": "..." }
Returns: { "project_id": "uuid", "name": "...", "created_at": "..." }
```

**List Projects**
```
GET /api/projects
Returns: [{ "id": "uuid", "name": "...", "status": "..." }, ...]
```

**Get Project**
```
GET /api/projects/<id>
Returns: { "id": "...", "scenes": [...], "stories": [...] }
```

**Update Project**
```
PUT /api/projects/<id>/update
Body: { "name": "...", "description": "..." }
```

**Delete Project**
```
DELETE /api/projects/<id>/delete
```

**Create Scene**
```
POST /api/projects/<id>/scenes/create
Body: {
  "sequence": 1,
  "background_type": "forest",
  "characters": [...],
  "narration": "Once upon a time...",
  "duration": 3.0
}
Returns: { "scene_id": "uuid" }
```

### Stories Endpoints

**Generate Story**
```
POST /api/stories/create
Body: { "project_id": "uuid", "prompt": "A brave rabbit..." }
Returns: { "story_id": "uuid", "scenes": [...] }
```

**Get Characters**
```
GET /api/stories/characters
Returns: {
  "hero": { "name": "Hero", "color": "#FF6B6B", "expressions": [...] },
  ...
}
```

**Get Backgrounds**
```
GET /api/stories/backgrounds
Returns: {
  "forest": { "color": "#90EE90", "elements": [...] },
  ...
}
```

### Animation Endpoints

**Preview Scene**
```
GET /api/animations/preview/<scene_id>
Returns: SVG XML string
```

**Update Scene**
```
POST /api/animations/scenes/<id>/update
Body: { "characters": [...], "narration": "...", "background_type": "..." }
```

**Render Animation**
```
POST /api/animations/render
Body: { "project_id": "uuid" }
Returns: { "total_frames": 1800, "frame_rate": 30 }
```

### Audio Endpoints

**Generate Audio**
```
POST /api/audio/generate
Body: {
  "project_id": "uuid",
  "text": "Hello world",
  "track_type": "narration",
  "scene_id": "uuid"
}
Returns: { "audio_id": "uuid", "duration": 1.5 }
```

**Estimate Duration**
```
POST /api/audio/estimate-duration
Body: { "text": "Hello world" }
Returns: { "estimated_duration": 1.2 }
```

**Get Mouth Animation**
```
GET /api/audio/mouth-animation/<duration>
Returns: { "keyframes": [...] }
```

## Database Schema

### Projects Table
```sql
CREATE TABLE projects (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  created_at TEXT,
  updated_at TEXT,
  thumbnail TEXT,
  status TEXT DEFAULT 'draft'
);
```

### Stories Table
```sql
CREATE TABLE stories (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  content TEXT NOT NULL,
  created_at TEXT,
  FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### Scenes Table
```sql
CREATE TABLE scenes (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  story_id TEXT,
  sequence INTEGER,
  background_type TEXT,
  characters TEXT,  -- JSON
  narration TEXT,
  duration REAL DEFAULT 3.0,
  transitions TEXT,  -- JSON
  created_at TEXT,
  FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### Audio Tracks Table
```sql
CREATE TABLE audio_tracks (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  scene_id TEXT,
  track_type TEXT,
  content TEXT,
  duration REAL,
  file_path TEXT,
  created_at TEXT
);
```

### Characters Table
```sql
CREATE TABLE characters (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  character_type TEXT,
  appearance TEXT,
  position TEXT,  -- JSON
  expression TEXT DEFAULT 'neutral',
  created_at TEXT
);
```

### Animations Table
```sql
CREATE TABLE animations (
  id TEXT PRIMARY KEY,
  scene_id TEXT NOT NULL,
  character_id TEXT,
  animation_type TEXT,
  keyframes TEXT,  -- JSON
  duration REAL,
  created_at TEXT
);
```

## Usage Walkthrough

### 1. Create a Project
1. Click "Create" on home page
2. Enter project name and description
3. Click "Create Project"
4. Redirected to editor

### 2. Generate Story
1. In editor, go to "Story" tab
2. Write a story prompt (e.g., "A little bear finds honey")
3. Click "Generate Story"
4. System creates 3 example scenes

### 3. Edit Scene
1. Go to "Scenes" tab
2. Click a scene to edit
3. Go to "Edit" tab
4. Modify narration, add characters, adjust duration
5. Characters can be positioned (X: 0-1), given expressions
6. Click "Save Changes"

### 4. Generate Audio
1. In scene editor, scroll to "Audio" section
2. Add narration text
3. Click "Generate Audio"
4. Audio is created via text-to-speech
5. Duration is estimated and displayed

### 5. Preview Animation
1. Click "Preview" button at top
2. View animation frames
3. Use Play/Pause and timeline scrubber
4. Click "Export MP4" to download

### 6. Save Project
1. Click "Save" button
2. Project data is persisted
3. Can be loaded anytime from Projects page

## Available Characters

```
hero:
  - Color: Red (#FF6B6B)
  - Expressions: happy, sad, surprised, neutral

friend:
  - Color: Teal (#4ECDC4)
  - Expressions: happy, sad, surprised, neutral

villain:
  - Color: Mint (#95E1D3)
  - Expressions: angry, sneaky, evil, neutral

wise_one:
  - Color: Pink (#F38181)
  - Expressions: wise, kind, neutral
```

## Available Backgrounds

```
- forest (trees, grass)
- castle (stone walls, flags)
- village (houses, paths)
- mountain (rocks, snow)
- ocean (water, waves)
- garden (flowers, paths)
```

## Animation Types

```
- entrance: Fade in + slide from left
- movement: Move character to new position
- celebration: Bounce + spin
- expression_change: Change face expression
```

## Deployment

### Frontend (Vercel)

1. Push to GitHub
2. Connect repository to Vercel
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` = backend URL
4. Deploy

### Backend (Railway/Heroku/etc)

1. Create app on hosting platform
2. Set environment:
   ```
   DATABASE_URL=sqlite:///animation.db
   FLASK_ENV=production
   ```
3. Install system dependencies:
   - FFmpeg
   - Python 3.8+
4. Deploy code
5. Run: `python run.py`

## Development Tips

### Frontend
- Components in `src/components/`
- API calls in `src/lib/api.ts`
- Pages in `src/app/`
- Use Tailwind for styling
- Lucide React for icons

### Backend
- Routes in `backend/app/routes/`
- Services in `backend/app/services/`
- Database in `backend/app/models/database.py`
- Debug: add `app.run(debug=True)` in run.py

### Debugging

**Frontend Console Errors**
- Check browser DevTools (F12)
- Check that API_URL is correct
- Ensure backend is running

**Backend Errors**
- Check Flask terminal output
- Verify database exists in `storage/projects/animation.db`
- Check audio files saved in `storage/audio/`

## Common Issues

**"API not reachable"**
- Ensure backend running on port 5000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in `app/__init__.py`

**"Database locked"**
- Close any open connections
- Delete `storage/projects/animation.db` and reinit

**"Audio generation fails"**
- Ensure pyttsx3 installed: `pip install pyttsx3`
- On Windows, may need SAPI5 voice models

**"Video export fails"**
- Ensure FFmpeg installed and in PATH
- Run: `ffmpeg -version` to verify

## Next Steps

### To Deploy Live
1. Set up GitHub repository
2. Deploy frontend to Vercel
3. Deploy backend to Railway or similar
4. Update API URLs in environment variables

### To Add Features
1. Add LLM integration for story generation
2. Implement lip-sync for dialogue
3. Add custom character creator
4. Create template marketplace

### To Improve Performance
1. Cache generated SVGs
2. Use CDN for static assets
3. Optimize frame rendering
4. Implement progressive video encoding

## Support & Issues

For problems or feature requests:
1. Check this guide
2. Review backend logs: `python run.py` output
3. Check frontend console: F12 in browser
4. Verify database: `storage/projects/animation.db` exists

## License

MIT License - Free to use and modify
