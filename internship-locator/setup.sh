#!/bin/bash

# Internship Locator - Setup Script
# This script sets up the complete Internship Locator application

echo "🚀 Setting up Internship Locator..."
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install backend dependencies
echo "📚 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Backend dependencies installed successfully"
else
    echo "❌ Failed to install backend dependencies"
    exit 1
fi

cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p frontend/css
mkdir -p frontend/js
mkdir -p backend/scrapers
mkdir -p backend/utils

# Set permissions
echo "🔐 Setting permissions..."
chmod +x setup.sh

echo ""
echo "🎉 Setup completed successfully!"
echo "=================================="
echo ""
echo "📋 Next steps:"
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source ../venv/bin/activate"
echo "   python app.py"
echo ""
echo "2. Start the frontend server:"
echo "   cd frontend"
echo "   python -m http.server 3000"
echo ""
echo "3. Open your browser and go to:"
echo "   http://localhost:3000"
echo ""
echo "🔧 Backend API will be available at:"
echo "   http://localhost:5000"
echo ""
echo "📚 API Endpoints:"
echo "   GET  /api/health - Health check"
echo "   GET  /api/platforms - Get supported platforms"
echo "   POST /api/search - Search internships"
echo ""
echo "🌐 Supported Platforms:"
echo "   - LinkedIn"
echo "   - Indeed"
echo "   - Glassdoor"
echo "   - Handshake"
echo ""
echo "⚠️ Note: This application is for educational purposes."
echo "   Please respect the terms of service of job sites."
echo ""
echo "Happy internship hunting! 🎯" 