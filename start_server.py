#!/usr/bin/env python3
"""
Start the Interview Boss Battle FastAPI server
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import uvicorn
    from app.app import app
    
    print("🚀 Starting Interview Boss Battle API Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 API Info: http://localhost:8000/api/info")
    print("❤️  Health Check: http://localhost:8000/health")
    print("\n" + "="*50)
    print("🎮 Ready for Node.js frontend integration!")
    print("="*50 + "\n")
    
    # Start the server
    uvicorn.run(
        "app.app:app",  # Use import string for proper reload support
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
