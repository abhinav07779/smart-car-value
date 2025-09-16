#!/usr/bin/env python3
"""
Railway startup script for Car Price Prediction API
"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    # Get port from Railway environment variable
    port = int(os.environ.get("PORT", 8000))
    
    # Start the FastAPI application
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
