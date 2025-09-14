#!/usr/bin/env python3
"""
Server startup script for Car Price Prediction API
"""

import uvicorn
from .config import HOST, PORT, DEBUG

if __name__ == "__main__":
    print("🚗 Starting Car Price Prediction API Server...")
    print(f"📍 Server will run on: http://{HOST}:{PORT}")
    print(f"📚 API Documentation: http://{HOST}:{PORT}/docs")
    print(f"🔧 Debug mode: {DEBUG}")
    print("=" * 50)
    
    uvicorn.run(
        "backend.app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
