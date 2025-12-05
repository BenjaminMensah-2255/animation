Write-Host "🎬 Cartoon Animation Studio - Setup" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Working in: $PWD" -ForegroundColor Yellow
Write-Host ""

# Verify Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    exit 1
}

# Verify pip
Write-Host "Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip is installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️ pip not found, using python -m pip" -ForegroundColor Yellow
}

# Fix React dependencies first
Write-Host ""
Write-Host "🔄 Fixing React dependency conflict..." -ForegroundColor Yellow
npm install react@^18.2.0 react-dom@^18.2.0 --save --legacy-peer-deps

# Install all dependencies
Write-Host ""
Write-Host "📦 Installing all dependencies..." -ForegroundColor Yellow
npm install --legacy-peer-deps

# Setup backend
Write-Host ""
Write-Host "⚙️  Setting up backend..." -ForegroundColor Yellow
if (Test-Path "backend") {
    Write-Host "  Backend folder exists" -ForegroundColor Green
    cd backend
    
    # Create requirements.txt if needed
    if (-not (Test-Path "requirements.txt")) {
        @"
flask>=2.0.0
flask-cors>=3.0.0
flask-sqlalchemy>=3.0.0
python-dotenv>=1.0.0
"@ | Out-File requirements.txt
        Write-Host "  ✓ Created requirements.txt" -ForegroundColor Green
    }
    
    # Install Python packages
    Write-Host "  Installing Python packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    # Create a simple run.py if it doesn't exist
    if (-not (Test-Path "run.py")) {
        @"
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "message": "Backend is running"})

if __name__ == '__main__':
    print("🚀 Backend server starting on http://localhost:5000")
    app.run(debug=True, port=5000)
"@ | Out-File run.py
        Write-Host "  ✓ Created run.py" -ForegroundColor Green
    }
    
    cd ..
} else {
    Write-Host "⚠️ Backend folder not found - creating..." -ForegroundColor Yellow
    mkdir backend
    Write-Host "  ✓ Created backend folder" -ForegroundColor Green
}

# Create .env.local
Write-Host ""
Write-Host "📝 Creating environment file..." -ForegroundColor Yellow
if (-not (Test-Path ".env.local")) {
    "NEXT_PUBLIC_API_URL=http://localhost:5000/api" | Out-File .env.local
    Write-Host "✓ Created .env.local" -ForegroundColor Green
} else {
    Write-Host "✓ .env.local already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 SETUP COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host "  Terminal 1: cd backend && python run.py" -ForegroundColor White
Write-Host "  Terminal 2: npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Or run both at once: npm run dev:all" -ForegroundColor Cyan
Write-Host ""
Write-Host "Open: http://localhost:3000" -ForegroundColor Magenta