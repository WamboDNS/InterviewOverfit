# 🚀 Quick Start Guide

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
uv run start_streamlit.py
