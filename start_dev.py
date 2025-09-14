#!/usr/bin/env python3
"""
Development startup script for Car Price Prediction App
Starts both the FastAPI backend and React frontend
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    os.chdir("backend")
    subprocess.run([sys.executable, "app.py"])

def start_frontend():
    """Start the React frontend development server"""
    print("⚛️ Starting React frontend server...")
    os.chdir("..")
    subprocess.run(["npm", "run", "dev"])

def main():
    print("🚗 Starting Car Price Prediction App Development Environment")
    print("=" * 60)
    
    # Check if backend dependencies are installed
    try:
        import fastapi
        import uvicorn
        import pandas
        import sklearn
        print("✅ Backend dependencies found")
    except ImportError:
        print("❌ Backend dependencies not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
    
    # Check if frontend dependencies are installed
    if not os.path.exists("node_modules"):
        print("📦 Installing frontend dependencies...")
        subprocess.run(["npm", "install"])
    
    # Check if model is trained
    if not os.path.exists("backend/car_price_model.pkl"):
        print("🤖 Training ML model...")
        subprocess.run([sys.executable, "backend/run_training.py"])
    
    print("\n🎯 Starting servers...")
    print("Backend API: http://127.0.0.1:8002")
    print("Frontend App: http://localhost:8080")
    print("API Docs: http://127.0.0.1:8002/docs")
    print("\nPress Ctrl+C to stop both servers")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
