# 🎬 Cartoon Animation Studio

**AI-powered animated storytelling platform** that generates creative stories and brings them to life with character animations and synchronized narration.


[![Node.js](https://img.shields.io/badge/Node.js-18+-green)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-16+-black)](https://nextjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-red)](https://flask.palletsprojects.com/)

---

## ✨ Features

### 📖 AI Story Generation
- Generate unlimited creative stories using Google Gemini API
- Automatic scene composition and character dialogue
- Story templates and custom prompts

### 🎨 Character Animation
- SVG-based animated characters with multiple expressions
- Real-time mouth synchronization with narration
- Side-by-side character positioning
- Support for multiple characters per scene

### 🔊 Audio & Narration
- Text-to-speech narration using pyttsx3
- Audio automatically synchronized with animation frames
- Adjustable speech rate and voice

### 🎬 Video Export
- Export animations as MP4 videos
- High-quality rendering (1280×720 @ 30FPS)
- Batch export multiple scenes

### 📁 Project Management
- Create and organize multiple projects
- Save stories and scenes locally
- Export and import projects

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ with npm
- **Python** 3.10+
- **FFmpeg** (for video export)
- **Google API Key** (for story generation)

### Installation

```bash
# Clone repository
git clone https://github.com/BenjaminMensah-2255/animation.git
cd animation

# Install Node dependencies
npm install

# Install Python dependencies
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### Configuration

Create `.env.local` in project root:

```env
GOOGLE_API_KEY=your_api_key_here
NEXT_PUBLIC_API_URL=http://localhost:5000
FLASK_ENV=development
```

Get your Google API Key: [Google AI Studio](https://aistudio.google.com/app/apikey)

### Run Development Servers

```bash
# Terminal 1: Frontend (http://localhost:3000)
npm run dev

# Terminal 2: Backend (http://localhost:5000)
npm run backend
```

Or run both simultaneously:

```bash
npm run dev:all
```

---

## 📚 Documentation

- **[Getting Started Guide](./GETTING_STARTED.md)** - Setup & feature walkthrough
- **[Executive Summary](./EXECUTIVE_SUMMARY.md)** - Business overview & ROI
- **[Developer Guide](./DEVELOPER_GUIDE.md)** - Development & API reference
- **[Testing Guide](./TESTING.md)** - Testing procedures
- **[Enhancement README](./ENHANCEMENT_README.md)** - Advanced features

---

## 🏗️ Project Structure

```
animation/
├── src/                    # Frontend (Next.js + React)
│   ├── app/               # App Router pages
│   ├── components/        # React components
│   └── lib/               # Utilities and API client
│
├── backend/               # Backend (Flask + Python)
│   ├── app/
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   └── models/        # Database
│   └── requirements.txt
│
├── storage/               # Runtime data
│   ├── audio/             # Generated audio files
│   ├── videos/            # Exported videos
│   └── frames/            # Animation frames
│
└── docs/                  # Documentation
```

---

## 🔌 API Endpoints

### Projects
```
GET    /api/projects                 # List all projects
POST   /api/projects                 # Create project
GET    /api/projects/<id>            # Get project details
PUT    /api/projects/<id>            # Update project
DELETE /api/projects/<id>            # Delete project
```

### Stories
```
GET    /api/stories/<project_id>     # List stories
POST   /api/stories                  # Generate new story
GET    /api/stories/<id>             # Get story details
PUT    /api/stories/<id>             # Update story
```

### Animations
```
POST   /api/animations/preview/<scene_id>    # Preview scene
POST   /api/animations/render/<scene_id>     # Render animation
GET    /api/animations/audio/<scene_id>      # Get narration audio
POST   /api/animations/export/<scene_id>     # Export as video
```

For detailed API documentation, see [GETTING_STARTED.md](./GETTING_STARTED.md#-api-endpoints).

---

## 🛠️ Tech Stack

### Frontend
- **Next.js** 16.0 - React framework
- **React** 19 - UI library
- **TypeScript** 5 - Type safety
- **Tailwind CSS** 4 - Styling
- **Lucide React** - Icons

### Backend
- **Flask** 3.0 - Web framework
- **Python** 3.10+ - Language
- **pyttsx3** 2.90 - Text-to-speech
- **google-generativeai** - Gemini API
- **SQLite3** - Database


## 📊 Performance

- **Animation Rendering:** 30 FPS @ 1280×720
- **Story Generation:** ~10-15 seconds (average)
- **Audio Synthesis:** ~5-8 seconds per narration
- **Memory Usage:** ~200MB frontend, ~300MB backend
- **Database:** SQLite (scalable to PostgreSQL)



## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request



## 🐛 Troubleshooting

### Issue: "Port already in use"
```bash
# Kill existing processes
lsof -i :3000  # Find process
kill -9 <PID>  # Kill process
```

### Issue: "API connection refused"
- Ensure backend is running: `npm run backend`
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Verify CORS settings in `backend/run.py`

### Issue: "No audio generated"
- Verify `GOOGLE_API_KEY` is set
- Check backend logs for errors
- Ensure pyttsx3 is installed: `pip install pyttsx3`

See [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md#-troubleshooting) for more solutions.

---

## 📞 Support

- **Documentation:** Check [GETTING_STARTED.md](./GETTING_STARTED.md)
- **Issues:** Open a [GitHub Issue](https://github.com/BenjaminMensah-2255/animation/issues)
- **Discussions:** Start a [GitHub Discussion](https://github.com/BenjaminMensah-2255/animation/discussions)

---

## 🎯 Roadmap

- [ ] **v1.1** - Multiple language support
- [ ] **v1.2** - Custom character uploads
- [ ] **v1.3** - Advanced video effects
- [ ] **v1.4** - Collaboration features
- [ ] **v2.0** - Mobile app


**Benjamin Mensah**
- GitHub: [@BenjaminMensah-2255](https://github.com/BenjaminMensah-2255)
- Created: 2025

---

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev) for story generation
- [Next.js](https://nextjs.org) team for amazing framework
- [Flask](https://flask.palletsprojects.com) community
- [Tailwind CSS](https://tailwindcss.com) for styling

---

<div align="center">

**[⬆ Back to Top](#-cartoon-animation-studio)**

Made with ❤️ by Benjamin Mensah

</div>
