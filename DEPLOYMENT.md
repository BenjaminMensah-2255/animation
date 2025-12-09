# 🚀 Deployment Guide: Cartoon Animation Studio

Complete step-by-step guide to deploy your application online using Vercel (frontend) and PythonAnywhere (backend).

---

## 📋 Deployment Overview

| Component | Platform | Cost | Setup Time |
|-----------|----------|------|-----------|
| Frontend | Vercel | $0-20/month | 5 minutes |
| Backend | PythonAnywhere | $5-50/month | 10 minutes |
| Database | PythonAnywhere MySQL | Included | 2 minutes |
| Storage | Cloudinary (free tier) | $0-100/month | 5 minutes |
| **Total** | - | **$5-170/month** | **22 minutes** |

---

## 🎯 Pre-Deployment Checklist

- [ ] Git repository initialized and pushed to GitHub
- [ ] All code committed (no local-only changes)
- [ ] `.env.local` created with all required variables
- [ ] `GOOGLE_API_KEY` obtained from Google AI Studio
- [ ] GitHub account created
- [ ] Vercel account created (free)
- [ ] Railway account created (free)

---

## Part 1: Frontend Deployment (Vercel) - 5 minutes

### Step 1: Push Code to GitHub

```bash
cd D:\projects\MCBTP\animation

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: Cartoon Animation Studio"

# Create repository on GitHub at https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/animation.git
git branch -M main
git push -u origin main
```

### Step 2: Connect Vercel to GitHub

1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign up"** (or Log in if you have an account)
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub repositories

### Step 3: Import Project to Vercel

1. On Vercel dashboard, click **"New Project"**
2. Select **"Import Git Repository"**
3. Search for and select **"animation"** repository
4. Click **"Import"**

### Step 4: Configure Environment Variables

1. In the **"Configure Project"** section:
2. Find **"Environment Variables"**
3. Add the following variables:

```
NEXT_PUBLIC_API_URL = https://animation-backend.railway.app
GOOGLE_API_KEY = your_key_here
```

**Note:** You'll set the Railway URL after deploying the backend (Step 6 below)

### Step 5: Deploy Frontend

1. Click **"Deploy"**
2. Wait 2-3 minutes for build to complete
3. Once done, you'll see: **"Congratulations! Your site is live"**
4. Copy your URL (e.g., `https://animation-123.vercel.app`)

✅ **Frontend is now live!**

---

## Part 2: Backend Deployment (PythonAnywhere) - 10 minutes

### Step 1: Create PythonAnywhere Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Click **"Pricing"** or **"Sign up"**
3. Choose a plan (Beginner: $5/month recommended)
4. Complete registration
5. Verify your email

### Step 2: Upload Code to PythonAnywhere

You have two options:

**Option A: Using Git (Recommended)**

1. In PythonAnywhere dashboard, go to **"Consoles"**
2. Click **"$ Bash"** to open terminal
3. Clone your repository:

```bash
cd /home/YOUR_USERNAME
git clone https://github.com/YOUR_USERNAME/animation.git
cd animation
```

**Option B: Upload via Web**

1. Go to **"Files"** tab
2. Navigate to `/home/YOUR_USERNAME/`
3. Click **"Upload a file"**
4. Upload your code as ZIP and extract

### Step 3: Create Virtual Environment

In PythonAnywhere **Bash Console**:

```bash
cd /home/YOUR_USERNAME/animation
mkvirtualenv --python=/usr/bin/python3.10 animation
pip install -r backend/requirements.txt
```

### Step 4: Configure Web App

1. Go to **"Web"** tab in PythonAnywhere
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**
5. Click **"Next"**

### Step 5: Configure WSGI File

1. In **"Web"** tab, find **"Code"** section
2. Click on WSGI configuration file (should be at `/var/www/benmen2255_pythonanywhere_com_wsgi.py`)
3. In PythonAnywhere Bash Console, run this command to create the WSGI file:

```bash
cat > /var/www/benmen2255_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os

# Add paths
project_home = '/home/benmen2255/animation'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

sys.path.insert(0, '/home/benmen2255/animation/backend')

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBBYxnl0wfYRgM3uCsSwAsVkfufvgxE8Mg'
os.environ['FLASK_DEBUG'] = '0'

# Activate virtual environment
import site
site.addsitedir('/home/benmen2255/.virtualenvs/animation/lib/python3.10/site-packages')

# Import and run Flask app
from run import app as application
EOF
```

4. Verify it was created:

```bash
cat /var/www/benmen2255_pythonanywhere_com_wsgi.py
```

5. Make it executable:

```bash
chmod 644 /var/www/benmen2255_pythonanywhere_com_wsgi.py
```

### Step 6: Configure Virtual Environment Path

1. In **"Web"** tab, find **"Virtualenv"** section
2. Set to: `/home/YOUR_USERNAME/.virtualenvs/animation`
3. Click the checkmark to confirm

### Step 7: Set Source Code Path

1. In **"Web"** tab, find **"Source code"** section
2. Set to: `/home/YOUR_USERNAME/animation`
3. Click the checkmark to confirm

### Step 8: Add Environment Variables

1. Go to **"Files"** tab
2. Navigate to `/home/YOUR_USERNAME/animation`
3. Create `.env` file with:

```
FLASK_ENV=production
GOOGLE_API_KEY=your_api_key_here
FLASK_DEBUG=0
DATABASE_URL=mysql://YOUR_USERNAME:PASSWORD@YOUR_USERNAME.mysql.pythonanywhere-services.com/YOUR_USERNAME$animation
```

### Step 9: Reload Web App

1. Go back to **"Web"** tab
2. Click **"Reload YOUR_USERNAME.pythonanywhere.com"** button (green button at top)
3. Wait 10-20 seconds for reload to complete

### Step 10: Test Backend

Navigate to: `https://YOUR_USERNAME.pythonanywhere.com/api/projects`

Should return:
```json
{
  "success": true,
  "data": [],
  "meta": {...}
}
```

✅ **Backend is now deployed on PythonAnywhere!**

### Step 11: Get Your Backend URL

Your backend URL is: `https://YOUR_USERNAME.pythonanywhere.com`

Copy this URL for the next step.

---

## Part 3: Database Setup (PythonAnywhere MySQL) - 2 minutes

### Step 1: Create Database

1. In PythonAnywhere, go to **"Databases"** tab
2. Click **"Create a new database"**
3. Name it: `YOUR_USERNAME$animation`
4. Choose **"MySQL"**
5. Set strong password
6. Click **"Create"**

### Step 2: Initialize Database Tables

In **PythonAnywhere Bash Console**:

```bash
cd /home/YOUR_USERNAME/animation
source /home/YOUR_USERNAME/.virtualenvs/animation/bin/activate

# Create tables
python -c "from backend.app.models.database import init_db; init_db()"
```

### Step 3: Verify Database Connection

```bash
# Test connection
python -c "from backend.app.models.database import get_db; print(get_db())"
```

✅ **Database is configured!**

---

## Part 4: Storage Configuration (Cloudinary) - 5 minutes

### Step 1: Create Cloudinary Account

1. Go to [cloudinary.com](https://cloudinary.com)
2. Click **"Sign Up"**
3. Complete registration
4. Go to Dashboard
5. Copy your **"Cloud Name"** and **"API Key"**

### Step 2: Add Cloudinary to Backend

Install package in PythonAnywhere Bash Console:

```bash
cd /home/YOUR_USERNAME/animation
source /home/YOUR_USERNAME/.virtualenvs/animation/bin/activate
pip install cloudinary
pip freeze > backend/requirements.txt
```

Create `backend/app/services/storage_service.py`:

```python
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import os

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

class StorageService:
    @staticmethod
    def upload_audio(file_path, filename):
        """Upload audio to Cloudinary"""
        result = cloudinary.uploader.upload(
            file_path,
            resource_type='video',
            folder='animation/audio'
        )
        return result['secure_url']
    
    @staticmethod
    def upload_video(file_path, filename):
        """Upload video to Cloudinary"""
        result = cloudinary.uploader.upload(
            file_path,
            resource_type='video',
            folder='animation/videos'
        )
        return result['secure_url']
```

### Step 3: Update WSGI File with Cloudinary Credentials

Update `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

project_home = '/home/YOUR_USERNAME/animation'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

sys.path.insert(0, '/home/YOUR_USERNAME/animation/backend')

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['GOOGLE_API_KEY'] = 'YOUR_API_KEY_HERE'
os.environ['CLOUDINARY_CLOUD_NAME'] = 'your_cloud_name'
os.environ['CLOUDINARY_API_KEY'] = 'your_api_key'
os.environ['CLOUDINARY_API_SECRET'] = 'your_api_secret'

from run import app as application
```

### Step 4: Reload PythonAnywhere

Go to **"Web"** tab and click **"Reload"** button.

✅ **Storage configured!**

---

## 🔗 Post-Deployment Configuration

### Step 1: Update Vercel with Backend URL

1. Go to **Vercel Dashboard**
2. Select your project
3. Go to **"Settings"** → **"Environment Variables"**
4. Update `NEXT_PUBLIC_API_URL` with your PythonAnywhere backend URL:
   ```
   NEXT_PUBLIC_API_URL = https://YOUR_USERNAME.pythonanywhere.com
   ```
5. Click **"Save"**
6. Go to **"Deployments"** and click **"Redeploy"** on latest deployment

### Step 2: Update CORS Settings

In `backend/run.py`, update CORS configuration:

```python
from flask_cors import CORS

CORS(app, origins=[
    'https://your-vercel-url.vercel.app',
    'http://localhost:3000'  # For local development
])
```

Replace `your-vercel-url` with your actual Vercel domain.

### Step 3: Update API Client

In `src/lib/api.ts`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const api = {
  async getProjects() {
    const response = await fetch(`${API_URL}/api/projects`);
    if (!response.ok) throw new Error('Failed to fetch projects');
    return response.json();
  },
  // ... rest of API calls
};
```

### Step 4: Push Changes and Redeploy

```bash
# Push backend changes to GitHub
git add backend/
git commit -m "Update Cloudinary and CORS configuration"
git push origin main

# Vercel automatically redeploys
# Reload PythonAnywhere web app
```

✅ **All services connected!**

---

## 🧪 Post-Deployment Testing

### Test Frontend

```bash
# Visit your Vercel URL
https://your-app.vercel.app

# Check:
✅ Page loads without errors
✅ No console errors (press F12)
✅ All images/icons display
✅ Navigation works
```

### Test Backend API

```bash
# Test projects endpoint
curl https://YOUR_USERNAME.pythonanywhere.com/api/projects

# Should return:
{
  "success": true,
  "data": [],
  "meta": {...}
}
```

### Test Full Flow

1. Create a project on the app
2. Generate a story
3. Preview animation (verify audio plays)
4. Export video (verify file downloads)
5. Check Railway logs for errors

---

## 📊 Monitoring & Logs

### View Vercel Logs

1. Go to Vercel Dashboard
2. Select your project
3. Go to **"Deployments"**
4. Click on a deployment
5. View **"Logs"** tab

### View PythonAnywhere Logs

1. Go to **"Web"** tab
2. Scroll to **"Log files"** section
3. Click on:
   - **"Error log"** - For Python errors
   - **"Server log"** - For HTTP requests
   - **"Access log"** - For all requests

### Check PythonAnywhere Status

```bash
# In PythonAnywhere Bash Console
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

### Common Issues

| Issue | Solution |
|-------|----------|
| 404 on backend routes | Check CORS configuration and backend URL in Vercel |
| "ModuleNotFoundError" | Reinstall packages in virtual environment: `pip install -r backend/requirements.txt` |
| Audio not playing | Verify Cloudinary credentials and file upload path |
| Database connection error | Check MySQL connection string in WSGI file |
| "Permission denied" | Run `chmod +x /home/YOUR_USERNAME/animation/backend/run.py` in Bash Console |

---

## 💰 Cost Optimization

### Free Tier Setup (Perfect for MVP)

**Monthly Cost: ~$5**

```
✅ Vercel:           FREE (Hobby plan, unlimited sites)
✅ PythonAnywhere:   FREE (1GB storage, 100MB CPU seconds/day - very limited)
✅ Cloudinary:       FREE (25GB storage, 25K transformations)
Total:               $0 (Development phase)
```

### Production Setup (Beginner - Recommended)

**Monthly Cost: ~$10-15**

```
✅ Vercel:           FREE (Hobby plan)
💰 PythonAnywhere:   $5/month (Beginner plan - 30GB storage, 3.6M CPU seconds/month)
✅ Cloudinary:       FREE (Free tier)
Total:               ~$5-10/month
```

### Production Setup (Intermediate)

**Monthly Cost: ~$20-30**

```
💰 Vercel Pro:       $20/month (priority support, analytics)
💰 PythonAnywhere:   $8/month (Starter plan - 100GB storage, 7.2M CPU seconds/month)
💰 Cloudinary Pro:   Free or $10/month
Total:               ~$28-30/month
```

### Production Setup (Growing Business)

**Monthly Cost: ~$50-100**

```
💰 Vercel Pro:       $20/month
💰 PythonAnywhere:   $25/month (Premium plan - 300GB storage)
💰 Cloudinary Pro:   $10-50/month (based on usage)
💰 Domain:           $1-2/month
Total:               ~$56-97/month
```

---

## 🔐 Security Best Practices

### Secure Your Secrets

✅ **DO:**
- Use PythonAnywhere WSGI file for environment variables (not in code)
- Never hardcode API keys in source files
- Use Vercel environment variables for secrets
- Never commit `.env.local` to GitHub

❌ **DON'T:**
- Hardcode API keys in code
- Share credentials via Slack/email
- Commit `.env` files to repository
- Use weak database passwords

### Enable Security Features

1. **Vercel:**
   - Go to **Settings** → **Security**
   - Enable **"HTTPS"** (default: on)
   - Enable **"Environment Variable Encryption"**

2. **PythonAnywhere:**
   - Use strong database password
   - Enable **"Password protect web app"** (in Web tab)
   - Keep Python version updated

3. **GitHub:**
   - Enable **"Branch Protection"** rules
   - Require pull request reviews before merge
   - Enable **"Secret Scanning"**

### Hide Sensitive Information in Bash

When creating files in PythonAnywhere, set proper permissions:

```bash
chmod 600 /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py
```

---

## 📈 Performance Optimization

### Frontend Performance

**Vercel provides:**
- ✅ Automatic code splitting
- ✅ Image optimization
- ✅ Edge caching (CDN)
- ✅ Automatic minification

### Backend Performance

**Optimize with:**
```python
# Enable caching
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/projects')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_projects():
    return jsonify(projects)
```

### Database Performance

**PostgreSQL optimization:**
- Create indexes on frequently queried columns
- Use connection pooling
- Archive old records

---

## 🔄 Continuous Deployment (CI/CD)

### Automatic Deployments

Both Vercel and PythonAnywhere require different approaches:

**Vercel automatically deploys when you push to GitHub:**

```bash
# Make changes locally
git add .
git commit -m "Fix: improve animation rendering"

# Push to GitHub
git push origin main

# Vercel automatically redeploys ✅
```

**PythonAnywhere requires manual reload:**

```bash
# After pushing changes, in PythonAnywhere:
# 1. Pull latest code in Bash Console:
cd /home/YOUR_USERNAME/animation
git pull origin main

# 2. Go to Web tab and click "Reload" button
# 3. Changes are live!
```

### Automatic Backend Reload on Deploy

To auto-reload PythonAnywhere when code changes, you can use GitHub Actions:

Create `.github/workflows/reload-pythonanywhere.yml`:

```yaml
name: Reload PythonAnywhere

on:
  push:
    branches: [main]

jobs:
  reload:
    runs-on: ubuntu-latest
    steps:
      - name: Call PythonAnywhere API
        run: |
          curl -X POST \
            https://www.pythonanywhere.com/api/v0/user/YOUR_USERNAME/webapps/YOUR_USERNAME.pythonanywhere.com/reload/ \
            -H "Authorization: Token YOUR_API_TOKEN"
```

Get your API token from PythonAnywhere **Account** → **API token**

---

## 🆘 Troubleshooting

### Frontend won't load

```
Error: "Cannot connect to API"

Solution:
1. Check NEXT_PUBLIC_API_URL in Vercel variables (should be https://YOUR_USERNAME.pythonanywhere.com)
2. Verify PythonAnywhere backend is running (check Web tab - should say "Running")
3. Clear browser cache (Ctrl+Shift+Delete)
4. Check browser console (F12) for errors
5. Verify CORS is configured correctly in backend/run.py
```

### Backend crashes or won't load

```
Error: "ModuleNotFoundError: No module named 'flask'"

Solution:
1. Check virtual environment is activated in WSGI file
2. Verify requirements.txt is installed: pip install -r backend/requirements.txt
3. Check Python version is 3.10+ in PythonAnywhere settings
4. Look at error log in Web tab → Log files
```

### Python 500 Internal Server Error

```
Error: "HTTP 500 - Internal Server Error"

Solution:
1. Check PythonAnywhere error log: Web tab → Error log
2. Look for specific error messages (usually indicates missing imports, typo, etc.)
3. Common: ImportError (missing package) → reinstall requirements.txt
4. Common: IndentationError (code syntax) → check Python indentation
```

### Database connection fails

```
Error: "Can't connect to MySQL server"

Solution:
1. Verify database was created: Databases tab should show YOUR_USERNAME$animation
2. Check DATABASE_URL in WSGI file is correct
3. Verify database password in WSGI file matches
4. Try resetting database password in Databases tab
5. Test connection in Bash: python -c "from backend.app.models.database import get_db; print(get_db())"
```

### Cloudinary upload fails

```
Error: "401 Unauthorized" or "Upload failed"

Solution:
1. Verify CLOUDINARY_CLOUD_NAME in WSGI file (check spelling)
2. Verify CLOUDINARY_API_KEY is correct
3. Regenerate API secret if unsure
4. Test Cloudinary account is active and valid
5. Check file permissions on uploaded files
```

### Static files (CSS, images) not loading

```
Error: "CSS not applied" or "Images missing"

Solution:
1. Run: npm run build
2. In Vercel, check "Public" folder is included
3. Clear browser cache
4. Check browser console for 404 errors on static files
```

### "Permission denied" errors

```
Error: "Permission denied" when accessing files

Solution:
bash
chmod +x /home/YOUR_USERNAME/animation/backend/run.py
chmod 755 /home/YOUR_USERNAME/animation/storage/audio
chmod 755 /home/YOUR_USERNAME/animation/storage/videos
```

---

## ✅ Deployment Checklist

- [ ] GitHub repository created and code pushed
- [ ] Vercel project created and deployed
- [ ] Vercel environment variables configured
- [ ] Railway backend service deployed
- [ ] Railway PostgreSQL database created
- [ ] Railway environment variables configured
- [ ] Cloudinary account created (optional but recommended)
- [ ] Vercel redeployed with backend URL
- [ ] Frontend loads without errors
- [ ] Backend API responds (test with curl)
- [ ] Full flow tested (create story → view animation → export)
- [ ] Database populated with test data
- [ ] Logs monitored for errors
- [ ] Performance acceptable (<3s page load)

---

## 🎉 You're Live!

Your app is now deployed online! Share these URLs:

```
Frontend:  https://your-app.vercel.app
Backend:   https://YOUR_USERNAME.pythonanywhere.com
```

---

## 📞 Support Resources

- [Vercel Documentation](https://vercel.com/docs)
- [PythonAnywhere Documentation](https://help.pythonanywhere.com)
- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [GitHub Documentation](https://docs.github.com)

---

## 🚀 Next Steps

1. **Share with Users** - Send your Vercel URL to users
2. **Set Custom Domain** - Point your domain to Vercel
3. **Setup Analytics** - Add Google Analytics to track usage
4. **Enable Monitoring** - Setup error tracking with Sentry
5. **Scale Infrastructure** - Upgrade plans as needed

---

<div align="center">

**Happy Deploying! 🚀**

Questions? Check the documentation or create a GitHub issue.

</div>
