#!/usr/bin/env python3
"""
Start script for Railway deployment
"""
import uvicorn
import os

if __name__ == "__main__":
    # Get port from Railway environment variable, default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Run the FastAPI app
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
