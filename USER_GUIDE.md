# 🎬 Cartoon Animation Studio - User Guide

## Overview

The Cartoon Animation Studio is an automated pipeline that lets you create animated stories with minimal effort. You write a prompt → the system generates a complete story with characters, scenes, animations, and audio → you can edit any part → export as video.

---

## 🏗️ How the System Works

### Architecture

```
USER (Browser at localhost:3000)
        ↓
   [Frontend - React]
   - Story Creator
   - Scene Editor
   - Animation Viewer
   - Audio Generator
        ↓
   [API Layer - HTTP]
        ↓
   [Backend - Flask at localhost:5000]
   - Story Generator Service
   - Animation Engine
   - Audio Service (TTS)
   - Video Export Service
        ↓
   [Database - SQLite]
   - Projects
   - Stories
   - Scenes
   - Characters
   - Audio Tracks
   - Animations
        ↓
   [Storage]
   - Audio Files (WAV)
   - Video Files (MP4)
   - Frame Images (PNG)
```

### Data Flow

1. **User enters story prompt** → Frontend sends to backend
2. **Backend generates story** → Creates 3 scenes with characters, backgrounds, narration
3. **Scenes saved to database** → Each scene has characters, positions, expressions
4. **User edits scenes** → Changes narration, character positions, expressions
5. **Audio generated** → TTS converts narration to speech
6. **Animations previewed** → SVG renders showing characters and backgrounds
7. **Project saved** → All data persists in SQLite database

---

## 🎯 Step-by-Step Testing Guide

### **Test 1: Create Your First Project**

**Goal**: Learn how projects are created

**Steps**:
1. Open browser at `http://localhost:3000`
2. Click **"Create Your First Animation"** or navigate to `/projects/new`
3. Enter:
   - **Project Name**: "My First Story"
   - **Description**: "A magical adventure"
4. Click **"Create Project"**
5. You're now in the **Editor Page**

**What Happens Behind the Scenes**:
```
Frontend: POST /api/projects/create
  ↓
Backend: Creates new project row in database
  ↓
Database: INSERT into projects (id, name, description, created_at, ...)
  ↓
Response: { project_id: "abc123", name: "My First Story" }
```

**Verify Success**: 
- You see project name at top of editor
- Three tabs appear: Story, Scenes, Edit

---

### **Test 2: Generate a Story**

**Goal**: Understand story generation from prompts

**Steps**:
1. In the **Story** tab, you see a text area labeled "Story Prompt"
2. Enter a prompt:
   ```
   A brave little rabbit discovers a magical forest and makes friends with a wise owl.
   ```
3. Click **"Generate Story"** button
4. Wait 2-3 seconds for generation

**What Happens Behind the Scenes**:
```
Frontend: POST /api/stories/create
  Body: { project_id: "abc123", prompt: "A brave little rabbit..." }
  ↓
Backend StoryGenerator Service:
  1. Create story structure
  2. Generate 3 scenes:
     - Scene 1: "Introduction" (narration about setup)
     - Scene 2: "Adventure" (narration about adventure)
     - Scene 3: "Resolution" (narration about conclusion)
  3. Assign random characters (Hero, Friend, Villain, Wise One)
  4. Assign random backgrounds (Forest, Mountain, Ocean, etc.)
  5. Create animations for each scene
  ↓
Backend: INSERT story and 3 scenes into database
  ↓
Response: {
    story_id: "xyz789",
    title: "Generated Adventure",
    scenes: [
      { id: "scene1", sequence: 1, title: "Introduction", ... },
      { id: "scene2", sequence: 2, title: "Adventure", ... },
      { id: "scene3", sequence: 3, title: "Resolution", ... }
    ]
  }
```

**Verify Success**:
- Story title appears: "Generated Adventure"
- Three scenes listed below
- Message shows "Scene 1: Introduction", "Scene 2: Adventure", "Scene 3: Resolution"

---

### **Test 3: View Generated Scenes**

**Goal**: See the automatically generated animation previews

**Steps**:
1. Click the **"Scenes"** tab
2. You see 3 scene boxes listed
3. Each shows:
   - Scene number (1, 2, 3)
   - Background type (e.g., "forest", "mountain")
4. Click on any scene

**What Happens Behind the Scenes**:
```
Frontend: Switches to "Edit" tab and loads selected scene
  ↓
Backend: GET /api/animations/preview/{scene_id}
  ↓
AnimationEngine Service:
  1. Fetch scene data from database
  2. Parse character positions and expressions
  3. Generate SVG markup with:
     - Background (colored rectangle with landscape elements)
     - Characters (stick figures with colors)
     - Face expressions (eyes, mouth based on emotion)
  4. Return SVG as string
  ↓
Response: SVG XML like:
  <svg>
    <rect fill="#87CEEB" .../> <!-- Sky background -->
    <ellipse .../> <!-- Trees -->
    <g transform="..."> <!-- Character -->
      <circle .../> <!-- Head -->
      <circle .../> <!-- Eyes -->
      <path .../> <!-- Mouth -->
    </g>
  </svg>
```

**Verify Success**:
- You're now in **"Edit"** tab
- Left side shows **animated preview** (characters and background)
- Right side shows scene details (narration, duration)

---

### **Test 4: Edit Scene Narration**

**Goal**: Customize the story dialogue

**Steps**:
1. In Edit tab, find the **"Scene Narration"** text area
2. Current narration shows: something like "The adventure begins..."
3. Edit it to something new:
   ```
   The brave rabbit hopped through the forest, looking for adventure.
   ```
4. Change **"Duration"** to 5 seconds (was 3)
5. Click **"Save Changes"** button

**What Happens Behind the Scenes**:
```
Frontend: POST /api/animations/scenes/{scene_id}/update
  Body: {
    narration: "The brave rabbit hopped...",
    duration: 5,
    characters: [...],
    background_type: "forest"
  }
  ↓
Backend:
  1. Validate scene exists
  2. UPDATE scenes table with new narration/duration
  ↓
Response: { success: true, scene_id: "abc123" }
  ↓
Frontend: Shows "Scene saved!" alert
```

**Verify Success**:
- Alert shows "Scene saved!"
- Animation preview updates (may take 1-2 seconds)

---

### **Test 5: Generate Audio**

**Goal**: Create text-to-speech narration

**Steps**:
1. Scroll down to **"Audio"** section
2. See the narration text in a blue box
3. Click **"Generate Audio"** button
4. Wait 3-5 seconds (system is converting text to speech)

**What Happens Behind the Scenes**:
```
Frontend:
  1. POST /api/audio/estimate-duration
     Body: { text: "The brave rabbit..." }
     ↓
     Response: { estimated_duration: 4.2 }
  ↓
  2. POST /api/audio/generate
     Body: {
       project_id: "abc123",
       scene_id: "scene1",
       text: "The brave rabbit...",
       track_type: "narration"
     }
     ↓
     Backend AudioService:
       - Initialize pyttsx3 engine
       - Set speech rate to 150 WPM
       - Save to file: storage/audio/narration_{uuid}.wav
       - Return filename
     ↓
     Response: {
       audio_id: "audio123",
       filename: "narration_abc-def-ghi.wav",
       duration: 4.2
     }
  ↓
  3. Frontend stores URL: 
     "http://localhost:5000/api/audio/narration_abc-def-ghi.wav"
```

**Verify Success**:
- Green box appears below "Generate Audio" button
- Shows "✓ Audio generated"
- Displays duration (e.g., "Duration: 4.2s")
- **"Play Audio"** button and **download icon** appear

---

### **Test 6: Play Audio**

**Goal**: Listen to the generated narration

**Steps**:
1. In the green audio box, click **"Play Audio"** button
2. You hear the narration being read aloud
3. Button changes to **"Pause"**
4. Audio plays through system speakers

**What Happens Behind the Scenes**:
```
Frontend:
  1. Button click triggers handlePlayPause()
  2. Creates new Audio element: new Audio(url)
  3. Calls audio.play()
  4. Updates UI to show "Pause" button
  ↓
Browser:
  1. HTTP GET /api/audio/narration_abc-def-ghi.wav
  ↓
Backend: 
  1. Validates filename (security check)
  2. Checks file exists in storage/audio/
  3. Calls send_file() to stream WAV file
  ↓
Browser: 
  1. Receives binary audio data
  2. Plays through speakers
```

**Verify Success**:
- You hear the narration voice
- Button shows "Pause"
- Audio plays for the duration (e.g., 4.2 seconds)

---

### **Test 7: Download Audio**

**Goal**: Save audio file locally

**Steps**:
1. In the green audio box, click the **download icon** (⬇️) button
2. File downloads to your Downloads folder
3. File is named: `audio-{scene_id}.wav`

**What Happens Behind the Scenes**:
```
Frontend:
  1. Click download button
  2. Create <a> element with:
     - href: audio URL
     - download: "audio-scene123.wav"
  3. Programmatically click link
  ↓
Browser:
  1. Triggers file download
  2. Saves to Downloads folder
```

**Verify Success**:
- File appears in Downloads folder
- Can play in any audio player (VLC, Windows Media Player, etc.)

---

### **Test 8: Edit Character Positions**

**Goal**: Customize where characters appear

**Steps**:
1. In the **"Edit"** tab, scroll to **"Characters"** section
2. See character list (e.g., "Hero" at position [0.3, 0.7])
3. Each character has:
   - Character name
   - Position sliders (X: 0-1, Y: 0-1)
   - Expression dropdown
4. Adjust sliders:
   - Move **X slider left** → character moves left
   - Move **Y slider down** → character moves down
5. Change **expression** to "surprised" or "sad"
6. Click **"Save Changes"**

**What Happens Behind the Scenes**:
```
Frontend:
  1. User changes position/expression
  2. State updates in React
  3. POST /api/animations/scenes/{scene_id}/update
     Body: {
       characters: [
         { character_id: "hero", position: { x: 0.2, y: 0.6 }, expression: "surprised" }
       ]
     }
  ↓
Backend:
  1. Convert characters to JSON
  2. UPDATE scenes table
  ↓
Frontend:
  1. GET /api/animations/preview/{scene_id}
  2. AnimationEngine renders new SVG with updated positions
  3. Preview updates in real-time
```

**Verify Success**:
- Preview updates showing character in new position
- Character expression changes (eyes/mouth change)

---

### **Test 9: Delete a Scene**

**Goal**: Remove unwanted scenes

**Steps**:
1. Click **red trash icon** (🗑️) next to "Save Changes" button
2. Confirmation dialog appears: "Are you sure you want to delete this scene?"
3. Click OK
4. Wait 1-2 seconds

**What Happens Behind the Scenes**:
```
Frontend:
  1. User clicks delete button
  2. Confirm dialog shown
  3. If confirmed: DELETE /api/animations/scenes/{scene_id}/delete
  ↓
Backend:
  1. Validate scene exists
  2. DELETE audio_tracks WHERE scene_id = ?
  3. DELETE scenes WHERE id = ?
  ↓
Frontend:
  1. Reload project
  2. Switch to "Scenes" tab
  3. Scene is gone from list
```

**Verify Success**:
- Alert shows "Scene deleted!"
- Automatically returns to Scenes tab
- Deleted scene no longer in list
- Project now has 2 scenes instead of 3

---

### **Test 10: Full Project Workflow**

**Goal**: Complete end-to-end workflow

**Steps**:

**1. Create Project** (Test 1)
- Project name: "My Adventure"

**2. Generate Story** (Test 2)
- Prompt: "A young explorer finds treasure in a hidden temple"
- Creates 3 scenes automatically

**3. Edit Scene 1** (Test 3-4)
- Click on Scene 1
- Edit narration to be more specific
- Save changes

**4. Generate Audio for Scene 1** (Test 5-6)
- Generate audio
- Play and listen

**5. Edit Scene 2** (Test 3-4)
- Click on Scene 2
- Change character positions
- Change expressions
- Save

**6. Generate Audio for Scene 2** (Test 5-6)
- Generate audio
- Download audio file

**7. Delete Scene 3** (Test 9)
- Click Scene 3
- Delete it
- Now project has 2 scenes

**8. Save Project** (Automatic)
- All data stored in SQLite database

**Result**: You have a complete project with custom narration, positioned characters, and generated audio!

---

## 📊 Database Inspection

### View What's Stored

The SQLite database is at: `backend/storage/projects/animation.db`

You can inspect it with tools like:
- **DBeaver** (visual tool)
- **SQLite3 CLI** (command line)
- **DB Browser for SQLite**

**Tables and their contents**:

```sql
-- Projects table: Stores your projects
SELECT * FROM projects;
-- Output: id, name, description, created_at, updated_at, status

-- Stories table: Generated stories
SELECT * FROM stories;
-- Output: id, project_id, title, description, content, created_at

-- Scenes table: Individual scenes (3 per story)
SELECT * FROM scenes;
-- Output: id, project_id, story_id, sequence, background_type, 
--         characters (JSON), narration, duration, transitions, created_at

-- Audio tracks table: Generated audio files
SELECT * FROM audio_tracks;
-- Output: id, project_id, scene_id, track_type, content, 
--         duration, file_path, created_at

-- Characters table: Character definitions
SELECT * FROM characters;
-- Output: id, name, character_type, appearance, position, expression, created_at
```

---

## 🔍 Debugging & Monitoring

### Check Backend Logs

Watch the Flask backend terminal to see API calls:

```
127.0.0.1 - - [05/Dec/2025 12:35:01] "POST /api/stories/create HTTP/1.1" 201 -
127.0.0.1 - - [05/Dec/2025 12:35:02] "POST /api/audio/generate HTTP/1.1" 201 -
127.0.0.1 - - [05/Dec/2025 12:35:07] "GET /api/audio/narration_xyz.wav HTTP/1.1" 200 -
```

### Check Frontend Logs

Open browser DevTools (F12 → Console) to see:
- API request responses
- JavaScript errors
- Component state changes

### Check Storage

Files are saved to:
- **Audio files**: `backend/storage/audio/narration_*.wav`
- **Video files**: `backend/storage/videos/*.mp4`
- **Frame images**: `backend/storage/frames/{project_id}/frame_*.png`

---

## 🎨 Understanding the Animation Preview

The animation preview is an **SVG graphic** that shows:

**Background** (colored rectangle):
- Forest: Light green with trees (ellipses)
- Castle: Gray with walls
- Mountain: Dark gray with peaks
- Ocean: Light blue with waves
- Garden: Light green with flowers
- Village: Tan with houses

**Characters** (simple shapes):
- Head: Circle
- Body: Rectangle
- Arms: Lines
- Legs: Lines
- Eyes: Small circles
- Mouth: Path (based on expression)

**Expressions**:
- Happy: Curved smile mouth
- Sad: Downward mouth
- Surprised: "O" mouth
- Angry: Angry eyebrows and mouth

**Positioning**:
- X, Y coordinates from 0 to 1 (normalized)
- 0,0 = top-left
- 1,1 = bottom-right
- Example: (0.5, 0.5) = center of screen

---

## 🚀 Quick Test Checklist

```
[ ] Create project
[ ] Generate story with prompt
[ ] View 3 scenes created
[ ] Edit scene 1 narration
[ ] Save scene changes
[ ] Generate audio
[ ] Play audio
[ ] Download audio file
[ ] Edit character positions
[ ] Change character expressions
[ ] Generate audio for scene 2
[ ] Delete scene 3
[ ] Project saved to database
```

---

## 💡 Tips & Tricks

1. **Faster iterations**: Keep browser tab open, just switch between Story/Scenes/Edit tabs
2. **Better audio**: Keep narration under 20 words per scene for clarity
3. **Visual appeal**: Position characters at different X positions (0.3, 0.7) to create space
4. **Storage**: Audio files automatically cleaned up when scenes deleted
5. **Database**: Data persists even if you close browser/restart servers

---

## 🎬 Next Steps (Not Yet Implemented)

These features could enhance the system:

- [ ] Frame rendering to PNG (requires ImageMagick)
- [ ] Video export (FFmpeg infrastructure ready)
- [ ] Real-time animation playback (AnimationViewer)
- [ ] Advanced LLM story generation (Claude/GPT integration)
- [ ] User authentication (multi-user support)
- [ ] Export to different formats (GIF, WebM, etc.)

---

## ❓ Common Issues & Solutions

**Issue**: "Failed to fetch" when generating audio
- **Solution**: Ensure backend is running on port 5000

**Issue**: Audio plays but can't hear anything
- **Solution**: Check system volume, try refreshing page

**Issue**: Changes not saved
- **Solution**: Click "Save Changes" button (not automatic)

**Issue**: Scene doesn't update after edit
- **Solution**: Wait 2-3 seconds for preview to re-render

**Issue**: Can't delete scene
- **Solution**: Confirm the delete dialog

---

Happy animating! 🎉
