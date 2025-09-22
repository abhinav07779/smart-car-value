#!/usr/bin/env python3
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
