@echo off
echo 🚗 Starting Car Price Prediction Backend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    cd backend
    pip install -r requirements.txt
    cd ..
)

REM Start the backend
echo 🚀 Starting backend on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python start_backend.py
