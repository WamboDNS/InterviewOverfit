# 🚀 Quick Start Guide

## Fix for Import Issues

If you're getting `ModuleNotFoundError: No module named 'dataloader'`, here's how to fix it:

### 1. Install Dependencies
```bash
uv sync
```

### 2. Start the Backend
```bash
# From the project root directory
uv run uvicorn src.app.app:app --reload --port 8000
```

### 3. Start the Frontend
```bash
# Option 1: Streamlit (Recommended)
python start_streamlit.py

# Option 2: Gradio (Alternative)
python start_gradio.py
```

## Alternative Backend Startup Methods

If the above doesn't work, try these alternatives:

### Method 1: Using Python Module
```bash
cd /Users/denis/Projects/InterviewOverfit
python -m uvicorn src.app.app:app --reload --port 8000
```

### Method 2: Using the existing startup script
```bash
python start_server.py
```

### Method 3: Direct Python execution
```bash
cd /Users/denis/Projects/InterviewOverfit
PYTHONPATH=/Users/denis/Projects/InterviewOverfit python -m uvicorn src.app.app:app --reload --port 8000
```

## Troubleshooting

### Import Issues
- Make sure you're running from the project root directory
- Ensure all dependencies are installed with `uv sync`
- The imports have been fixed to use absolute paths (`src.dataloader` instead of `dataloader`)

### Backend Connection Issues
- Check that the backend is running on `http://localhost:8000`
- Use the "Check Connection" button in the frontend sidebar
- Make sure no other service is using port 8000

### Frontend Issues
- Streamlit runs on `http://localhost:8501`
- Gradio runs on `http://localhost:7860`
- Make sure ports 8501 and 7860 are available

## What's Fixed

✅ **Import paths corrected**: Changed from relative imports to absolute imports
✅ **Missing `re` module**: Added `import re` to the backend
✅ **Code logic fixed**: Fixed undefined variables in the score parsing logic
✅ **Startup scripts**: Enhanced with better error handling and backend checking

## Ready to Go!

Your Interview Boss Battle frontend is now ready with:
- 🎨 Beautiful Streamlit interface with modern UI
- 🎮 Alternative Gradio interface for simplicity
- 🔧 Fixed import issues
- 📱 Mobile-responsive design
- ⚡ Real-time game state updates

Just run the commands above and you'll be battling interview bosses in no time! 🎮⚔️
