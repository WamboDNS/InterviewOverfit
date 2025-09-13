#!/usr/bin/env python3
"""
Startup script for the Interview Boss Battle Streamlit frontend.
This script helps you start the Streamlit app with proper configuration.
"""

import subprocess
import sys
import os
from pathlib import Path
import time

def check_backend():
    """Check if backend is running and provide helpful information."""
    print("🔍 Checking backend status...")
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            print("✅ Backend is running on http://localhost:8000")
            return True
        else:
            print(f"⚠️  Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def start_backend():
    """Offer to start the backend."""
    print("\n🚀 Would you like to start the backend?")
    print("1. Yes, start backend in background")
    print("2. No, I'll start it manually")
    print("3. Exit")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            print("🔄 Starting backend in background...")
            try:
                # Start backend in background
                backend_process = subprocess.Popen([
                    "uv", "run", "uvicorn", "src.app.app:app", "--reload", "--port", "8000"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Wait a moment for backend to start
                print("⏳ Waiting for backend to start...")
                time.sleep(3)
                
                # Check if it's running
                if check_backend():
                    print("✅ Backend started successfully!")
                    return True
                else:
                    print("❌ Failed to start backend")
                    return False
            except Exception as e:
                print(f"❌ Error starting backend: {e}")
                return False
        elif choice == "2":
            print("📋 To start the backend manually, run:")
            print("   uv run uvicorn src.app.app:app --reload")
            print("   or")
            print("   python -m uvicorn src.app.app:app --reload")
            return False
        elif choice == "3":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

def main():
    """Start the Streamlit application."""
    print("🎮 Interview Boss Battle - Modern Frontend")
    print("=" * 60)
    print("A gamified interview preparation system")
    print("Built with Streamlit and FastAPI")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ Error: streamlit_app.py not found in current directory")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Check backend status
    backend_running = check_backend()
    
    if not backend_running:
        print("\n⚠️  Backend is required for the frontend to work properly.")
        backend_running = start_backend()
    
    if not backend_running:
        print("\n⚠️  Starting frontend without backend connection...")
        print("Some features may not work until the backend is running.")
    
    print("\n🚀 Starting Streamlit frontend...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🎨 Features:")
    print("   • Beautiful, modern UI with animations")
    print("   • Real-time game state updates")
    print("   • Interactive boss battle interface")
    print("   • Progress tracking and statistics")
    print("   • Conversation history")
    print("\n💡 Tips:")
    print("   • Use the sidebar to configure your game")
    print("   • Check backend status in the sidebar")
    print("   • View conversation history for review")
    print("   • Monitor your progress with the charts")
    print("\nPress Ctrl+C to stop the app")
    print("=" * 60)
    
    # Start Streamlit with enhanced configuration
    try:
        subprocess.run([
            "uv", "run", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false",
            "--server.headless", "false",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped. Thanks for playing!")
        print("🎮 Hope you enjoyed the Interview Boss Battle!")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have uv installed: pip install uv")
        print("2. Make sure dependencies are installed: uv sync")
        print("3. Try running manually: uv run streamlit run streamlit_app.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
