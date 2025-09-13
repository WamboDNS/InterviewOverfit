from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pathlib import Path
import sys

# Add the shared directory to the Python path
SHARED_DIR = Path(__file__).parent.parent / "shared"
sys.path.append(str(SHARED_DIR))

from game_logic import create_game_logic

app = FastAPI(title="InterviewOverfit API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game logic
game_logic = create_game_logic()

@app.get("/")
async def root():
    return {"message": "InterviewOverfit API is running!"}

@app.get("/api/game-config")
async def get_game_config():
    """Get the game configuration from the shared JSON file"""
    try:
        config_path = SHARED_DIR / "gameConfig.json"
        if not config_path.exists():
            raise HTTPException(status_code=404, detail="Game configuration not found")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading game configuration: {str(e)}")

@app.get("/api/game-data")
async def get_game_data():
    """Get the game data (bosses, questions, etc.) from the shared data"""
    try:
        # This would typically load from a database or shared data file
        # For now, we'll return a simple response
        return {
            "message": "Game data endpoint - implement based on your needs",
            "available_roles": ["SDE", "DS", "MLE"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading game data: {str(e)}")

@app.post("/api/evaluate-answer")
async def evaluate_answer(request: dict):
    """Evaluate a user's answer using the shared game logic"""
    try:
        content = request.get("content", "")
        question = request.get("question", "")
        
        if not content or not question:
            raise HTTPException(status_code=400, detail="Content and question are required")
        
        # Use the shared GameLogic class to evaluate the answer
        result = game_logic.evaluate_answer(content, question)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating answer: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
