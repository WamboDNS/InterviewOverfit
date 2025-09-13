#!/usr/bin/env python3
"""
Startup script for the Interview Boss Battle web application.
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Start the FastAPI server."""
    # Add the src directory to Python path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    # Check if API key is set
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  Warning: ANTHROPIC_API_KEY environment variable not set.")
        print("   You can set it in the web interface or as an environment variable.")
        print("   Example: export ANTHROPIC_API_KEY='your-key-here'")
        print()
    
    print("🚀 Starting Interview Boss Battle Server...")
    print("📱 Web interface will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    try:
        uvicorn.run(
            "app.app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["src"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for playing!")

if __name__ == "__main__":
    main()
