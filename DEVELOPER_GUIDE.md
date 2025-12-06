# Developer Setup & Maintenance Guide

## 🛠️ For Development Team

This guide covers everything needed to develop, test, and maintain the Cartoon Animation Studio.

---

## 📋 Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 8GB minimum (16GB recommended)
- **Disk Space**: 2GB free
- **Internet**: Required for Google Gemini API

### Required Software
```
Node.js 18+        (npm comes with it)
Python 3.10+       
Git
FFmpeg (for video export)
```

### Optional but Recommended
- VS Code with extensions:
  - ES7+ React/Redux/React-Native snippets
  - Pylance (Python language server)
  - Thunder Client or Postman (API testing)

---

## 🚀 Development Setup

### 1. Clone & Install

```bash
# Clone repository
git clone https://github.com/your-org/animation.git
cd animation

# Install Node dependencies
npm install

# Install Python dependencies
pip install -r backend/requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Environment Configuration

Create `.env.local` in project root:

```env
# Google Gemini API
GOOGLE_API_KEY=sk-xxx...

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:5000
DEBUG=true

# Backend
FLASK_ENV=development
LOG_LEVEL=DEBUG

# Optional
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 3. Verify Installation

```bash
# Check Node.js
node --version    # Should be 18+
npm --version

# Check Python
python --version  # Should be 3.10+

# Check Git
git --version

# Check FFmpeg
ffmpeg -version   # Required for video export
```

---

## 📂 Project Structure for Developers

```
animation/
├── src/                              # Frontend (Next.js)
│   ├── app/                         # App Router
│   │   ├── layout.tsx              # Root layout
│   │   ├── page.tsx                # Home page
│   │   ├── projects/               # Project management
│   │   ├── editor/[id]/            # Story editor
│   │   └── viewer/                 # Animation viewer
│   ├── components/                  # React components
│   │   ├── StoryCreator.tsx        # Story creation form
│   │   ├── CharacterSelector.tsx   # Character picker
│   │   ├── SceneEditor.tsx         # Scene editor
│   │   ├── AnimationViewer.tsx     # Animation player
│   │   └── AudioGenerator.tsx      # Audio controls
│   └── lib/
│       └── api.ts                   # API client
│
├── backend/                         # Backend (Flask/Python)
│   ├── app/
│   │   ├── __init__.py             # Flask app initialization
│   │   ├── routes/                 # API endpoints
│   │   │   ├── projects.py         # Project CRUD
│   │   │   ├── stories.py          # Story generation
│   │   │   ├── animation.py        # Animation rendering
│   │   │   └── audio.py            # Audio endpoints
│   │   ├── services/               # Business logic
│   │   │   ├── story_generator.py  # Gemini integration
│   │   │   ├── animation_engine.py # SVG rendering engine
│   │   │   ├── audio_service.py    # Text-to-speech
│   │   │   └── video_export.py     # FFmpeg wrapper
│   │   └── models/
│   │       └── database.py         # SQLite interface
│   ├── run.py                       # Flask entry point
│   └── requirements.txt
│
├── storage/                         # Runtime data (gitignored)
│   ├── audio/                       # .wav files
│   ├── videos/                      # .mp4 files
│   ├── frames/                      # .png frames
│   └── animation.db                 # SQLite database
│
└── docs/
    ├── GETTING_STARTED.md           # Setup guide
    ├── EXECUTIVE_SUMMARY.md         # Business overview
    ├── API_DOCUMENTATION.md         # API reference
    ├── ENHANCED_FEATURES.md         # Technical specs
    └── ...
```

---

## 🔧 Common Development Tasks

### Start Development Server

**Option 1: Both frontend and backend together**
```bash
npm run dev:all
```

**Option 2: Frontend only**
```bash
npm run dev
# Runs on http://localhost:3000
```

**Option 3: Backend only**
```bash
npm run backend
# Runs on http://localhost:5000
```

### Run Linter & Type Check

```bash
# TypeScript check
npx tsc --noEmit

# ESLint (if configured)
npx eslint src/

# Python linting
pip install pylint
pylint backend/app/
```

### Test Changes

**Frontend Testing**
```bash
npm run dev          # Start dev server
# Open http://localhost:3000
# Click through features
# Check console for errors
```

**Backend API Testing**
```bash
# Using curl
curl http://localhost:5000/api/projects

# Using Thunder Client or Postman
GET http://localhost:5000/api/projects
```

### Build for Production

```bash
# Frontend build
npm run build

# Backend production setup
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.run:app
```

---

## 🗄️ Database Management

### SQLite Database Schema

Located at: `storage/animation.db`

**Tables:**
- `projects` - Story projects
- `stories` - Generated stories
- `scenes` - Individual scenes in stories
- `characters` - Character definitions
- `audio_tracks` - Narration audio files
- `animations` - Animation metadata
- `relationships` - Project/story/scene relationships

### Database Operations

**Initialize Database**
```bash
python backend/app/models/database.py
```

**View Database**
```bash
# Using SQLite CLI
sqlite3 storage/animation.db

# Query example
.tables                    # List all tables
SELECT * FROM projects;   # View all projects
.schema projects          # View table structure
```

**Reset Database**
```bash
rm storage/animation.db
python backend/app/models/database.py
```

---

## 🔌 API Development

### Adding a New Endpoint

**Step 1: Create route handler**
```python
# backend/app/routes/new_feature.py
from flask import Blueprint, jsonify, request

new_feature_bp = Blueprint('new_feature', __name__, url_prefix='/api/new')

@new_feature_bp.route('/endpoint', methods=['GET'])
def new_endpoint():
    return jsonify({'message': 'Hello'}), 200
```

**Step 2: Register blueprint**
```python
# backend/run.py
from app.routes.new_feature import new_feature_bp
app.register_blueprint(new_feature_bp)
```

**Step 3: Test endpoint**
```bash
curl http://localhost:5000/api/new/endpoint
```

### Frontend API Integration

```typescript
// src/lib/api.ts
export const api = {
  async newFeature() {
    const response = await fetch(`${API_URL}/new/endpoint`);
    return response.json();
  }
};

// Usage in component
import { api } from '@/lib/api';

const data = await api.newFeature();
```

---

## 🎨 Frontend Development

### Component Structure

```typescript
// src/components/MyComponent.tsx
'use client';  // Mark as client component

import { useState } from 'react';

interface Props {
  title: string;
  onSubmit: (data: any) => void;
}

export default function MyComponent({ title, onSubmit }: Props) {
  const [state, setState] = useState('');

  return (
    <div className="p-4 bg-white rounded">
      <h2 className="text-2xl font-bold">{title}</h2>
      {/* Component content */}
    </div>
  );
}
```

### Styling with Tailwind CSS

```tsx
<div className="grid grid-cols-3 gap-4 p-6 bg-gradient-to-r from-blue-500 to-purple-600">
  <button className="px-4 py-2 bg-white text-blue-600 rounded hover:bg-gray-100 transition">
    Click me
  </button>
</div>
```

### Using Lucide Icons

```tsx
import { Play, Pause, Download } from 'lucide-react';

<button className="flex items-center gap-2">
  <Play size={20} />
  Play
</button>
```

---

## 🐍 Backend Development

### Adding a New Service

```python
# backend/app/services/my_service.py
class MyService:
    @staticmethod
    def process_data(data: dict) -> dict:
        """Process input data"""
        result = {'processed': data}
        return result
```

### Using Services in Routes

```python
from app.services.my_service import MyService

@my_bp.route('/process', methods=['POST'])
def process():
    data = request.json
    result = MyService.process_data(data)
    return jsonify(result), 200
```

---

## 🧪 Testing

### Frontend Testing (Optional Setup)

```bash
npm install --save-dev jest @testing-library/react

# Example test
// src/__tests__/MyComponent.test.tsx
import { render, screen } from '@testing-library/react';
import MyComponent from '@/components/MyComponent';

test('renders component', () => {
  render(<MyComponent title="Test" />);
  expect(screen.getByText('Test')).toBeInTheDocument();
});

# Run tests
npm test
```

### Backend Testing (Optional Setup)

```bash
pip install pytest

# Example test
# tests/test_api.py
import pytest
from app import create_app

def test_projects_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.get('/api/projects')
    assert response.status_code == 200

# Run tests
pytest tests/
```

---

## 📝 Code Standards

### TypeScript/JavaScript
- Use `const` by default
- Use arrow functions
- Follow ESLint rules
- Add type annotations

```typescript
// ✅ Good
const handleClick = (id: string): void => {
  console.log(id);
};

// ❌ Avoid
function handleClick(id) {
  console.log(id);
}
```

### Python
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused

```python
# ✅ Good
def calculate_total(prices: list[float]) -> float:
    """Calculate total price from list."""
    return sum(prices)

# ❌ Avoid
def calc(p):
    return sum(p)
```

---

## 🐛 Debugging

### Frontend Debugging

**Browser DevTools**
- F12 to open DevTools
- Console tab for errors
- Network tab for API calls
- Application tab for storage

**VS Code Debugging**
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/next",
      "args": ["dev"]
    }
  ]
}
```

### Backend Debugging

**Python Debugging with VS Code**
```bash
pip install debugpy
# Add breakpoints in code
# Press F5 to start debugging
```

**Flask Debug Mode**
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python -m flask run
```

---

## 📦 Dependencies Management

### Update Dependencies

```bash
# Frontend
npm update
npm audit fix

# Backend
pip list --outdated
pip install --upgrade package_name
```

### Add New Dependency

```bash
# Frontend
npm install package_name

# Backend
pip install package_name
pip freeze > backend/requirements.txt
```

---

## 🔄 Git Workflow

### Branch Strategy
```bash
# Create feature branch
git checkout -b feature/description

# Make changes
git add .
git commit -m "Description of changes"

# Push to remote
git push origin feature/description

# Create pull request on GitHub
# Wait for review and merge
```

### Commit Message Format
```
[type]: Brief description

Detailed explanation if needed

- Bullet point 1
- Bullet point 2
```

**Types:** feat, fix, docs, style, refactor, test, chore

---

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] All tests pass
- [ ] Code reviewed
- [ ] No console errors
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] API endpoints tested
- [ ] Performance optimized
- [ ] Security headers set
- [ ] SSL/HTTPS enabled
- [ ] Backup strategy in place

---

## 📞 Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :3000

# Kill process
kill -9 <PID>
```

### Module Not Found
```bash
# Frontend
npm install
rm -rf node_modules/.vite
npm run dev

# Backend
pip install -r backend/requirements.txt
```

### Database Locked
```bash
# Remove lock file
rm storage/animation.db-journal

# Restart backend
```

### API Connection Issues
```bash
# Check if backend is running
curl http://localhost:5000/api/projects

# Check CORS settings
# Check .env.local API_URL
# Check network tab in browser DevTools
```

---

## 📚 Useful Resources

- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev)
- [Flask Docs](https://flask.palletsprojects.com)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Google Gemini API](https://ai.google.dev)

---

## ✅ Ready to Develop!

You now have everything needed to develop and maintain this application. Happy coding! 🚀

**Questions?** Check the documentation files or reach out to the team.
