#!/usr/bin/env python3
"""
Backend startup script - runs from project root
"""

import subprocess
import sys
import os

def main():
    print("🚗 Starting Car Price Prediction Backend...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend"):
        print("❌ Error: backend directory not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if model exists
    if not os.path.exists("backend/car_price_model.pkl"):
        print("🤖 Training ML model first...")
        try:
            subprocess.run([sys.executable, "backend/run_training.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Model training failed!")
            sys.exit(1)
    
    # Start the server
    print("🚀 Starting FastAPI server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.app:app", 
            "--host", "0.0.0.0", 
            "--port", "8002", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
