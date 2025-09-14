#!/usr/bin/env python3
"""Local development startup script."""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Starting Habit Loop locally...")
    
    # Add backend to Python path
    backend_path = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_path))
    
    # Change to backend directory
    os.chdir(backend_path)
    
    # Import and create database
    from app.db.session import engine, Base
    from app.models import *
    
    print("📊 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Seed demo data
    print("🌱 Seeding demo data...")
    from app.scripts.seed_demo import seed_demo_data
    seed_demo_data()
    print("✅ Demo data seeded")
    
    # Start the server
    print("🌐 Starting FastAPI server...")
    print("📱 Frontend will be available at: http://localhost:3000")
    print("🔗 Backend API will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("\n🎯 Demo login: demo@habitloop.local")
    print("💡 Check the console for magic link in development mode")
    print("\n" + "="*60)
    
    # Start uvicorn
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--reload", 
        "--port", "8000",
        "--host", "0.0.0.0"
    ])

if __name__ == "__main__":
    main()
