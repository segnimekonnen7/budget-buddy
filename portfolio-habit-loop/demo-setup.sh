#!/bin/bash

# 🎯 Habit Loop - Demo Setup Script
# This script sets up the Habit Loop application for portfolio demonstrations

echo "🎯 Setting up Habit Loop for Portfolio Demo..."
echo "=============================================="

# Check if we're in the right directory
if [ ! -d "../habit-loop" ]; then
    echo "❌ Error: Please run this script from the portfolio-habit-loop directory"
    echo "   Expected structure: portfolio-habit-loop/demo-setup.sh"
    echo "   With habit-loop/ directory at the same level"
    exit 1
fi

# Navigate to the habit-loop directory
cd ../habit-loop

echo "📁 Current directory: $(pwd)"

# Check if backend and frontend directories exist
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Backend or frontend directories not found"
    echo "   Expected: habit-loop/backend/ and habit-loop/frontend/"
    exit 1
fi

echo "✅ Found backend and frontend directories"

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use"
        return 1
    else
        echo "✅ Port $port is available"
        return 0
    fi
}

# Check if ports are available
echo ""
echo "🔍 Checking port availability..."
check_port 8000
check_port 3000

# Kill any existing processes on these ports
echo ""
echo "🧹 Cleaning up existing processes..."
pkill -f "uvicorn.*8000" 2>/dev/null || true
pkill -f "next.*3000" 2>/dev/null || true
pkill -f "npm.*dev" 2>/dev/null || true

sleep 2

# Start backend
echo ""
echo "🚀 Starting Backend Server..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Start backend in background
echo "🌐 Starting FastAPI server on port 8000..."
nohup uvicorn app.main:app --reload --port 8000 --host 0.0.0.0 > /dev/null 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running successfully"
    echo "   Health check: http://localhost:8000/health"
    echo "   API docs: http://localhost:8000/docs"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo ""
echo "🎨 Starting Frontend Server..."
cd ../frontend

# Install dependencies
echo "📥 Installing Node.js dependencies..."
npm install > /dev/null 2>&1

# Start frontend in background
echo "🌐 Starting Next.js server on port 3000..."
nohup npm run dev > /dev/null 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

# Test frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running successfully"
    echo "   Application: http://localhost:3000"
else
    echo "❌ Frontend failed to start"
    exit 1
fi

echo ""
echo "🎉 Habit Loop is now running!"
echo "=============================="
echo ""
echo "🌐 Frontend Application: http://localhost:3000"
echo "📚 Backend API Docs: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo ""
echo "🎯 Demo Features to Show:"
echo "   • Create new habits with the 'New Habit' button"
echo "   • Check in on habits to build streaks"
echo "   • View responsive design on different screen sizes"
echo "   • Explore the API documentation"
echo ""
echo "🛑 To stop the servers:"
echo "   pkill -f 'uvicorn.*8000'"
echo "   pkill -f 'next.*3000'"
echo ""
echo "📊 Portfolio Integration:"
echo "   • Use the README.md for technical details"
echo "   • Use PROJECT_SUMMARY.md for portfolio text"
echo "   • Use PORTFOLIO_INTEGRATION.md for interview prep"
echo ""
echo "✨ Ready for your portfolio demonstration!"
