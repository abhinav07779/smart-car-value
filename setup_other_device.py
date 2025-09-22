#!/usr/bin/env python3
"""
Complete setup script for running the Car Price Prediction backend on other devices
"""
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ pip is available")
            return True
        else:
            print("❌ pip is not available")
            return False
    except Exception as e:
        print(f"❌ Error checking pip: {e}")
        return False

def install_dependencies():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.path.dirname(__file__), "backend")
        if not os.path.exists(backend_dir):
            print("❌ Backend directory not found!")
            return False
        
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], cwd=backend_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_model_files():
    """Check if model files exist"""
    print("\n🔍 Checking model files...")
    models_dir = os.path.join(os.path.dirname(__file__), "backend", "models")
    required_files = ["model.joblib", "preprocessor.joblib", "model_info.json"]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(models_dir, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file} - MISSING!")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing model files: {', '.join(missing_files)}")
        print("Please ensure all model files are present in backend/models/")
        return False
    
    return True

def test_backend_startup():
    """Test if backend can start"""
    print("\n🚀 Testing backend startup...")
    try:
        # Import the app to test if it loads
        sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
        from app import app
        print("✅ Backend app loads successfully")
        return True
    except Exception as e:
        print(f"❌ Backend app failed to load: {e}")
        return False

def create_startup_script():
    """Create a simple startup script"""
    print("\n📝 Creating startup script...")
    startup_script = """#!/usr/bin/env python3
import os
import sys
import uvicorn

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Car Price Prediction API on port {port}")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
"""
    
    with open("start_backend.py", "w") as f:
        f.write(startup_script)
    print("✅ Created start_backend.py")

def main():
    """Main setup function"""
    print("🚗 Car Price Prediction Backend Setup")
    print("=" * 50)
    
    # Check system requirements
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check model files
    if not check_model_files():
        return False
    
    # Test backend
    if not test_backend_startup():
        return False
    
    # Create startup script
    create_startup_script()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nTo start the backend:")
    print("  python start_backend.py")
    print("\nTo test the API:")
    print("  curl http://localhost:8000/health")
    print("  curl http://localhost:8000/")
    print("\nAPI Documentation:")
    print("  http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
