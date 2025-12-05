# Testing Guide - Cartoon Animation Studio

## Quick Start Testing

### 1. Start the Backend

```powershell
cd backend
python run.py
```

Expected output:
```
WARNING in app.run() is not recommended for use in production!
Running on http://127.0.0.1:5000
```

### 2. Start the Frontend

In a new terminal:
```powershell
npm run dev
```

Expected output:
```
▲ Next.js 16.0.7
- Local:        http://localhost:3000
```

### 3. Test the Application

Visit http://localhost:3000

## Manual API Testing

### Using PowerShell/curl:

**Create a Project**
```powershell
$body = @{
    name = "Test Animation"
    description = "A test story"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/projects/create" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Get Characters**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/stories/characters" `
  -Method GET
```

**Generate Story**
```powershell
$projectId = "your-project-id-here"
$body = @{
    project_id = $projectId
    prompt = "A brave little bear finds a magic forest"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/stories/create" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## Frontend Testing Scenarios

### Scenario 1: Create First Project

1. Go to http://localhost:3000
2. Click "Create Your First Animation" or navigate to /projects/new
3. Enter project name: "My First Story"
4. Enter description: "A magical adventure"
5. Click "Create Project"
6. Should redirect to editor page

**Expected Result**: Project created, editor loads

### Scenario 2: Generate Story from Prompt

1. In editor, go to "Story" tab
2. In prompt field, type: "A princess and a dragon become friends"
3. Click "Generate Story"
4. Should generate 3 example scenes

**Expected Result**: 
- Scenes display with narration text
- Each scene shows sequence number and title

### Scenario 3: Edit a Scene

1. Go to "Scenes" tab
2. Click on Scene 1
3. Tab should switch to "Edit"
4. Should show:
   - Scene preview (black box - SVG rendering)
   - Narration textarea
   - Duration input
   - Characters section
   - Audio section

**Expected Result**: Scene editor components visible and interactive

### Scenario 4: Add Character to Scene

1. In Scene editor, scroll to "Characters" section
2. Click "+ Hero" button
3. Should add character below
4. Character shows with controls to:
   - Change expression (dropdown)
   - Adjust X position (0-1)
5. Can click "Remove" to delete

**Expected Result**: Character added and visible in controls

### Scenario 5: Generate Audio Narration

1. In Scene editor, make sure narration text exists
2. Scroll to "Audio" section
3. Click "Generate Audio"
4. Should show narration text in blue box
5. Should show estimated duration
6. Should display "✓ Audio generated" message

**Expected Result**: 
- Audio generated successfully
- Duration estimated and displayed

### Scenario 6: Save Scene Changes

1. Make any changes (update narration, add character, etc.)
2. Click "Save Changes" button
3. Should show success message

**Expected Result**: Scene updates saved in database

### Scenario 7: View Project List

1. Navigate to /projects
2. Should see list of all projects
3. Each project shows:
   - Name
   - Description
   - Created date
   - Edit button
   - Delete button

**Expected Result**: Projects display correctly

### Scenario 8: Delete Project

1. On Projects page, click Delete (trash icon) on any project
2. Confirm deletion
3. Project should disappear from list

**Expected Result**: Project and all associated data deleted

## Database Verification

Check that database was created and has data:

```powershell
# Navigate to backend storage
cd storage/projects

# List files
ls

# Should see: animation.db
```

Connect to database directly:
```powershell
sqlite3 animation.db
```

Then run SQL queries:
```sql
SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM stories;
SELECT COUNT(*) FROM scenes;
SELECT COUNT(*) FROM audio_tracks;
.tables  # List all tables
```

## Common Issues & Solutions

### "API not reachable" Error

**Problem**: Frontend can't connect to backend

**Solution**:
1. Verify backend running: `http://localhost:5000/api/projects`
2. Check `.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:5000/api`
3. Restart frontend: `npm run dev`

### Database Locked

**Problem**: "Database is locked" error

**Solution**:
1. Close all terminal windows
2. Delete `backend/storage/projects/animation.db`
3. Run backend again to reinit

### Audio Generation Fails

**Problem**: Text-to-speech audio not generating

**Possible Solutions**:
- On Windows: Install speech voices via Settings > Speech
- Run: `pip install --upgrade pyttsx3`
- Check `storage/audio/` directory exists

### Video Export Not Working

**Problem**: Export fails or no MP4 created

**Solution**:
1. Install FFmpeg:
   - **Windows**: Download from ffmpeg.org or use: `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`
2. Verify: `ffmpeg -version`
3. Restart backend

## Performance Testing

### Test with Multiple Scenes

1. Create project
2. Generate story (creates 3 scenes)
3. Each scene ~3 seconds = 90 frames total at 30 FPS
4. Should render instantly

### Test with Large Narration

1. Create scene with very long narration
2. Estimate duration
3. Audio should still generate (may take 5-10 seconds)

### Test Multiple Characters per Scene

1. Create scene
2. Add 4+ characters
3. Animation should render smoothly

## Load Testing

To test with multiple projects:

```powershell
# Create 10 projects via API
for ($i = 1; $i -le 10; $i++) {
    $body = @{
        name = "Test Project $i"
        description = "Project $i"
    } | ConvertTo-Json
    
    Invoke-WebRequest -Uri "http://localhost:5000/api/projects/create" `
      -Method POST `
      -ContentType "application/json" `
      -Body $body
}
```

Then load Projects page - should display all 10 projects.

## Debugging Tips

### Enable Backend Debug Logs

Edit `backend/run.py`:
```python
app.run(debug=True, port=5000)  # Already set
```

Logs will show all API calls and errors.

### Check Frontend Console

Press F12 in browser to open DevTools:
- **Console tab**: JavaScript errors
- **Network tab**: API requests/responses
- **Application tab**: Local storage, cookies

### Check Database State

After testing, view database contents:
```powershell
sqlite3 backend/storage/projects/animation.db
SELECT * FROM projects;
SELECT * FROM scenes;
SELECT * FROM audio_tracks;
```

## Expected Component Behavior

### StoryCreator Component
- Input textarea for prompt
- Generate button (disabled if no text)
- Shows generated story structure after generation

### SceneEditor Component
- Displays scene preview (SVG in black box)
- Narration textarea
- Duration input
- Character selector buttons
- Save button

### CharacterSelector Component
- Shows buttons to add each character type
- Lists added characters with controls
- Shows expression selector
- Shows position input
- Remove button for each

### AudioGenerator Component
- Text input shows when narration exists
- Generate button
- Duration estimate display
- Success message after generation

### AnimationViewer Component
- Black canvas area
- Frame counter
- Play/Pause button
- Timeline slider
- Export MP4 button

## Success Criteria Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads on localhost:3000
- [ ] Can create new project
- [ ] Can generate story from prompt
- [ ] Can edit scene details
- [ ] Can add characters to scene
- [ ] Can generate audio narration
- [ ] Can save scene changes
- [ ] Can view projects list
- [ ] Can delete projects
- [ ] Database has correct data
- [ ] No console errors in browser
- [ ] All API endpoints respond

## Next Steps After Testing

1. **Deploy Frontend to Vercel**:
   - Push to GitHub
   - Connect to Vercel
   - Set environment variables

2. **Deploy Backend**:
   - Use Railway, Heroku, or similar
   - Set database URL
   - Ensure FFmpeg installed

3. **Enhance Features**:
   - Add LLM for better story generation
   - Implement actual frame rendering
   - Add lip-sync for audio
   - Create character customization

4. **Optimize**:
   - Cache generated content
   - Improve rendering performance
   - Add progress indicators for long operations
