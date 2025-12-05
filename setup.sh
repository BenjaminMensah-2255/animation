#!/bin/bash
# Quick Start Script for Cartoon Animation Studio

echo "🎬 Cartoon Animation Studio - Quick Start"
echo "=========================================="
echo ""

# Check if Node.js installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

# Check if Python installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ Python version: $(python --version)"
echo ""

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

echo ""
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python -c "from app.models.database import init_db; init_db(); print('✅ Database initialized')"

cd ..

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:5000/api" > .env.local
    echo "✅ Created .env.local"
fi

echo ""
echo "🚀 Setup complete!"
echo ""
echo "To start development:"
echo "  Terminal 1: cd backend && python run.py"
echo "  Terminal 2: npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "Or run both together: npm run dev:all"
