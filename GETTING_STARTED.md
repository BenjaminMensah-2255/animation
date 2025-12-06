# 🎬 Cartoon Animation Studio - Getting Started Guide

**An AI-powered web application for creating, editing, and exporting animated stories with talking characters, professional backgrounds, and synchronized narration.**

---

## ⚡ Quick Start (5 Minutes)

### Prerequisites
- **Node.js** 18+ ([download](https://nodejs.org/))
- **Python** 3.10+ ([download](https://www.python.org/))
- **Git** ([download](https://git-scm.com/))
- **Google API Key** (for AI story generation) - [Get one here](https://aistudio.google.com/app/apikey)

### Installation & Launch

```bash
# 1. Clone the repository
git clone <repo-url>
cd animation

# 2. Install dependencies
npm install
pip install -r backend/requirements.txt

# 3. Create .env.local file and add your Google API key
echo GOOGLE_API_KEY=your_key_here > .env.local
echo NEXT_PUBLIC_API_URL=http://localhost:5000 >> .env.local

# 4. Start the application
npm run dev:all
```

**Open your browser:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

---

## 📊 What This Application Does

### Core Workflow

```
Write Story Prompt
        ↓
AI Generates 3-Scene Story (Google Gemini)
        ↓
Select Characters, Backgrounds, Expressions
        ↓
View Animation with Talking Characters (SVG + Audio Sync)
        ↓
Edit Scenes or Export as MP4 Video
```

### Key Features

| Feature | Capability |
|---------|-----------|
| **AI Story Generation** | Writes complete 3-scene stories from a single prompt |
| **Characters** | 4 types × 6 colors × 5 expressions = 120 variations |
| **Animation** | 30 FPS SVG rendering with 7 mouth shapes for speech |
| **Audio** | Text-to-speech narration auto-generated from story |
| **Speech Bubbles** | Dynamic text rendering with word wrapping |
| **Video Export** | MP4 output with audio (1280×720 @ 30fps) |
| **Backgrounds** | 6 environments (Forest, Castle, Ocean, Mountain, Garden, Village) |
| **Editing** | Full scene customization, reordering, deletion |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│  FRONTEND: Next.js 16 + React 19 + TypeScript 5         │
│  Running on: http://localhost:3000                       │
│                                                          │
│  Pages: Home, Projects, Editor, Viewer                  │
│  Components: StoryCreator, CharacterSelector,           │
│             SceneEditor, AnimationViewer                │
└─────────────────────────────────────────────────────────┘
                          ↕ REST API
┌─────────────────────────────────────────────────────────┐
│  BACKEND: Flask 3.0 + Python 3.14                        │
│  Running on: http://localhost:5000                       │
│                                                          │
│  Routes: /projects, /stories, /animations,              │
│          /audio, /scenes                                │
│  Services: StoryGenerator (AI), AnimationEngine (SVG),  │
│           AudioService (TTS), VideoExport (FFmpeg)      │
└─────────────────────────────────────────────────────────┘
                          ↕ Database/Files
┌─────────────────────────────────────────────────────────┐
│  DATA: SQLite Database + File Storage                   │
│                                                          │
│  Database: projects, stories, scenes, characters,       │
│           audio_tracks, animations                      │
│  Storage: /storage/audio/, /storage/videos/,            │
│          /storage/frames/                               │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Installation Details

### Step 1: Install Node Dependencies

```bash
npm install
```

**Installed packages:**
- Next.js 16.0.7 - React framework
- React 19.2.0 - UI library
- TypeScript 5 - Type safety
- Tailwind CSS 4 - Styling
- Lucide React - Icons

### Step 2: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

**Key packages:**
- Flask 3.0.0 - Web API framework
- pyttsx3 2.90 - Text-to-speech
- google-generativeai - Google Gemini API
- Pillow - Image processing
- FFmpeg - Video encoding

### Step 3: Configure Environment

Create `.env.local` file in project root:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:5000

# Optional
DEBUG=true
LOG_LEVEL=INFO
```

**Getting a Google API Key:**
1. Visit https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key into `.env.local`

---

## 🚀 Running the Application

### Option 1: Run Everything Together (Recommended)

```bash
npm run dev:all
```

This starts both:
- Next.js development server (port 3000)
- Flask API server (port 5000)

### Option 2: Run Separately

**Terminal 1 - Frontend:**
```bash
npm run dev
# Opens http://localhost:3000
```

**Terminal 2 - Backend:**
```bash
npm run backend
# Opens http://localhost:5000
```

### Verify Setup

1. Open http://localhost:3000
2. Click "Create New Project"
3. Enter a story prompt (e.g., "A brave rabbit finds a magical forest")
4. Click "Generate Story"
5. Click "View Animation" to see your animated story

---

## 📁 Project Structure

```
animation/
│
├── frontend
│   ├── src/app/
│   │   ├── page.tsx              ← Home page
│   │   ├── projects/page.tsx     ← Project list
│   │   ├── editor/[id]/page.tsx  ← Story editor
│   │   └── viewer/page.tsx       ← Animation viewer
│   │
│   ├── src/components/
│   │   ├── StoryCreator.tsx
│   │   ├── CharacterSelector.tsx
│   │   ├── SceneEditor.tsx
│   │   ├── AnimationViewer.tsx
│   │   └── AudioGenerator.tsx
│   │
│   └── src/lib/
│       └── api.ts                ← API client
│
├── backend/
│   ├── app/routes/
│   │   ├── projects.py          ← Project endpoints
│   │   ├── stories.py           ← Story creation
│   │   ├── animation.py         ← Animation rendering
│   │   └── audio.py             ← Audio endpoints
│   │
│   ├── app/services/
│   │   ├── story_generator.py   ← AI integration (Gemini)
│   │   ├── animation_engine.py  ← SVG rendering
│   │   ├── audio_service.py     ← Text-to-speech (pyttsx3)
│   │   └── video_export.py      ← MP4 creation (FFmpeg)
│   │
│   ├── app/models/
│   │   └── database.py          ← SQLite queries
│   │
│   ├── run.py                    ← Flask entry point
│   └── requirements.txt
│
├── storage/                     (Created at runtime)
│   ├── audio/                   ← WAV narration files
│   ├── videos/                  ← Exported MP4s
│   ├── frames/                  ← Animation frame PNGs
│   └── projects/                ← Project saves
│
├── .env.local                   ← Environment config
├── package.json
├── tsconfig.json
├── next.config.ts
└── README.md
```

---

## 🔌 API Endpoints

### Base URL: `http://localhost:5000/api`

#### Projects
```
GET    /projects              - List all projects
POST   /projects/create       - Create new project
GET    /projects/{id}         - Get project details
DELETE /projects/{id}/delete  - Delete project
```

#### Stories
```
POST /stories/create         - Generate story from prompt
GET  /stories/characters    - List available characters
GET  /stories/backgrounds   - List available backgrounds
```

#### Animation & Audio
```
GET  /animations/preview/{scene_id}  - Get scene as SVG
GET  /animations/audio/{scene_id}    - Get narration audio
POST /animations/export/{project_id} - Export as MP4
```

#### Scenes
```
POST   /scenes/{scene_id}/update  - Update scene
DELETE /scenes/{scene_id}/delete  - Delete scene
```

---

## 🐛 Common Issues & Solutions

### ❌ "Cannot find module 'next'"
**Solution:**
```bash
npm install
```

### ❌ "Port 3000 is already in use"
**Solution (Windows):**
```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Solution (Mac/Linux):**
```bash
lsof -ti :3000 | xargs kill -9
```

### ❌ "GOOGLE_API_KEY not set"
**Solution:**
1. Create `.env.local` file
2. Add line: `GOOGLE_API_KEY=your_key_here`
3. Restart the server

### ❌ "Flask server won't start"
**Solution:**
```bash
cd backend
pip install -r requirements.txt
python -m flask run --port=5000
```

### ❌ "Audio files not generating"
**Solution:**
```bash
mkdir -p storage/audio
mkdir -p storage/videos
mkdir -p storage/frames
```

### ❌ "Video export not working"
**Requirements:**
- FFmpeg must be installed and in system PATH
- Windows: Download from https://ffmpeg.org/download.html
- Mac: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

---

## 🎨 Feature Walkthrough

### Creating a Story

1. **Click "Create New Project"**
   - Enter project name and description

2. **Click "Generate Story"**
   - Write a prompt (e.g., "A young wizard discovers ancient magic")
   - AI creates 3-scene story with narration

3. **View Generated Story**
   - See story title, description, 3 scenes
   - Each scene shows background, characters, narration

4. **View Animation**
   - Click "View Animation" on any scene
   - See characters with animated mouths
   - Click "Play" to hear narration and watch animation

### Editing a Scene

1. **Go to Editor**
   - Click scene to edit
   - Modify character positions, expressions
   - Change background type
   - Edit narration text

2. **Preview Changes**
   - Click "Preview" to see SVG
   - Changes appear immediately

3. **Save & Export**
   - Click "Save"
   - Click "Export MP4" to download video

---

## 📊 Technical Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend Framework** | Next.js | 16.0.7 |
| **UI Library** | React | 19.2.0 |
| **Styling** | Tailwind CSS | 4.0 |
| **Type Safety** | TypeScript | 5 |
| **Backend Framework** | Flask | 3.0.0 |
| **Language** | Python | 3.14+ |
| **Database** | SQLite | 3 |
| **Text-to-Speech** | pyttsx3 | 2.90 |
| **AI Integration** | Google Gemini | Latest |
| **Video Export** | FFmpeg | Latest |
| **Animation** | SVG | Native |
| **Icons** | Lucide React | Latest |

---

## 🚀 Next Steps

### For Users
- Read `USER_GUIDE.md` for detailed feature explanations
- Check `VISUAL_GUIDE_ENHANCED.md` for UI screenshots

### For Developers
- See `ENHANCED_CHARACTER_GENERATION.md` for animation system
- Check `AI_INTEGRATION_GUIDE.md` for Gemini API setup
- Review `QUICK_REFERENCE.md` for common tasks

### For Deployment
- See hosting section below

---

## 🌐 Deploying to Production

### Frontend Deployment (Vercel)
```bash
# 1. Push to GitHub
git push origin main

# 2. Go to vercel.com
# 3. Import repository
# 4. Set environment: NEXT_PUBLIC_API_URL=your-backend-url
# 5. Deploy
```

### Backend Deployment (Railway)
```bash
# 1. Create Railway account
# 2. Connect GitHub repo
# 3. Set environment variables:
#    - GOOGLE_API_KEY
#    - FLASK_ENV=production
# 4. Deploy
```

### Production Considerations
- [ ] Switch from SQLite to PostgreSQL
- [ ] Set up cloud storage (S3/Cloudinary) for files
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS for production domain
- [ ] Set up logging and monitoring
- [ ] Test video export (requires FFmpeg)

---

## 📞 Support

- **Questions?** Check the documentation files in the project root
- **Bug?** Check the logs in terminal output
- **Need help?** Review `TROUBLESHOOTING.md`

---

## 📄 License

Proprietary - All Rights Reserved

---

## 🎯 Version Info

**Current Version**: 1.0.0
**Last Updated**: December 6, 2025
**Status**: Production Ready ✅

---

**Ready to create amazing animated stories? Start with Step 1 above!** 🎬✨
