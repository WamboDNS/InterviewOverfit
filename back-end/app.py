#!/usr/bin/env python3
"""
FastAPI backend for InterviewOverfit - Boss Battle Interview Game
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from model_interaction.model import InterviewBossGame

app = FastAPI(
    title="InterviewOverfit Boss Battle API", 
    version="1.0.0",
    description="Gamified interview preparation system with AI-powered boss battles"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:3001",  # Alternative React port  
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001", 
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# In-memory storage for game instances (in production, use Redis/database)
game_instances: Dict[str, InterviewBossGame] = {}

# ================== REQUEST/RESPONSE MODELS ==================

class StartGameRequest(BaseModel):
    api_key: Optional[str] = None

class SubmitAnswerRequest(BaseModel):
    answer: str

class GameStateResponse(BaseModel):
    level: int
    max_level: int
    boss_name: str
    boss_personality: str
    boss_question_types: list[str]
    boss_hp: int
    max_hp: int
    user_hp: int
    turn_count: int
    current_question: str
    game_over: bool
    victory: bool
    conversation_length: int

class QuestionResponse(BaseModel):
    success: bool
    question: str
    game_state: GameStateResponse
    error: Optional[str] = None

class AnswerResponse(BaseModel):
    success: bool
    score: int
    feedback: str
    damage_dealt: int
    damage_taken: int
    game_state: GameStateResponse
    error: Optional[str] = None

class GameResponse(BaseModel):
    success: bool
    message: str
    game_state: Optional[GameStateResponse] = None
    error: Optional[str] = None

# ================== UTILITY FUNCTIONS ==================

def create_game_state_response(game: InterviewBossGame) -> GameStateResponse:
    """Convert game state to API response format."""
    state = game.get_game_state()
    return GameStateResponse(**state)

def get_default_error_state() -> GameStateResponse:
    """Create default error game state."""
    return GameStateResponse(
        level=1, max_level=3, boss_name="", boss_personality="", 
        boss_question_types=[], boss_hp=0, max_hp=100, user_hp=0, 
        turn_count=0, current_question="", game_over=True, 
        victory=False, conversation_length=0
    )

# ================== API ENDPOINTS ==================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "InterviewOverfit Boss Battle API"}

@app.get("/api/info")
async def api_info():
    """Get API information."""
    return {
        "name": "InterviewOverfit Boss Battle API",
        "version": "1.0.0",
        "description": "Gamified interview preparation system with AI-powered boss battles",
        "game_info": {
            "levels": 3,
            "bosses": ["Senior Developer Sarah", "Engineering Manager Marcus", "Staff Engineer Dr. Chen"],
            "max_hp": 100,
            "score_range": [-10, 10]
        },
        "endpoints": {
            "start_game": "POST /api/game/{uid}/start",
            "submit_answer": "POST /api/game/{uid}/answer", 
            "get_question": "GET /api/game/{uid}/question",
            "get_status": "GET /api/game/{uid}/status",
            "reset_game": "POST /api/game/{uid}/reset",
            "end_game": "DELETE /api/game/{uid}",
            "get_history": "GET /api/game/{uid}/history"
        }
    }

@app.post("/api/game/{uid}/start", response_model=QuestionResponse)
async def start_game(uid: str, request: StartGameRequest = Body(...)):
    """Start a new boss battle game."""
    try:
        # Use provided API key or environment variable
        api_key = request.api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            return QuestionResponse(
                success=False,
                question="",
                game_state=get_default_error_state(),
                error="API key is required. Please provide ANTHROPIC_API_KEY."
            )
        
        # Create new game instance
        game = InterviewBossGame(api_key=api_key)
        game_instances[uid] = game
        
        # Get first question
        question = game.get_question()
        game_state = create_game_state_response(game)
        
        return QuestionResponse(
            success=True,
            question=question,
            game_state=game_state
        )
        
    except Exception as e:
        return QuestionResponse(
            success=False,
            question="",
            game_state=get_default_error_state(),
            error=f"Failed to start game: {str(e)}"
        )

@app.get("/api/game/{uid}/status", response_model=GameStateResponse)
async def get_game_status(uid: str):
    """Get current game status."""
    if uid not in game_instances:
        raise HTTPException(status_code=404, detail="No active game found for this user")
    
    game = game_instances[uid]
    return create_game_state_response(game)

@app.get("/api/game/{uid}/question", response_model=QuestionResponse)
async def get_question(uid: str):
    """Get the current or next question."""
    if uid not in game_instances:
        return QuestionResponse(
            success=False,
            question="",
            game_state=get_default_error_state(),
            error="No active game found. Please start a new game first."
        )
    
    try:
        game = game_instances[uid]
        
        if game.game_over:
            return QuestionResponse(
                success=False,
                question="Game is over. Please start a new game.",
                game_state=create_game_state_response(game),
                error="Game is over"
            )
        
        # If there's no current question or we need a new one
        if not game.current_question:
            question = game.get_question()
        else:
            question = game.current_question
            
        return QuestionResponse(
            success=True,
            question=question,
            game_state=create_game_state_response(game)
        )
        
    except Exception as e:
        return QuestionResponse(
            success=False,
            question="",
            game_state=get_default_error_state(),
            error=f"Failed to get question: {str(e)}"
        )

@app.post("/api/game/{uid}/answer", response_model=AnswerResponse)
async def submit_answer(uid: str, request: SubmitAnswerRequest = Body(...)):
    """Submit an answer to the current question."""
    if uid not in game_instances:
        return AnswerResponse(
            success=False,
            score=0,
            feedback="No active game found. Please start a new game first.",
            damage_dealt=0,
            damage_taken=0,
            game_state=get_default_error_state(),
            error="No active game found"
        )
    
    try:
        game = game_instances[uid]
        
        # Store HP before answer submission
        boss_hp_before = game.boss_hp
        user_hp_before = game.user_hp
        
        # Submit answer
        response = game.submit_answer(request.answer)
        
        # Calculate damage dealt/taken
        boss_hp_after = game.boss_hp
        user_hp_after = game.user_hp
        damage_dealt = max(0, boss_hp_before - boss_hp_after)
        damage_taken = max(0, user_hp_before - user_hp_after)
        
        # Parse score from response (use game's internal parsing)
        score, feedback = game._parse_score(response)
        
        # Clean up feedback by removing score tags
        feedback_lines = feedback.split('\n')
        clean_feedback = []
        for line in feedback_lines:
            if not line.strip().startswith('<score>') and not line.strip() == '</END_SCORE>':
                clean_feedback.append(line)
        feedback = '\n'.join(clean_feedback).strip()
        
        # If game is over, clean up the instance
        if game.game_over:
            del game_instances[uid]
        
        return AnswerResponse(
            success=True,
            score=score,
            feedback=feedback,
            damage_dealt=damage_dealt,
            damage_taken=damage_taken,
            game_state=create_game_state_response(game)
        )
        
    except Exception as e:
        return AnswerResponse(
            success=False,
            score=0,
            feedback="",
            damage_dealt=0,
            damage_taken=0,
            game_state=get_default_error_state(),
            error=f"Failed to submit answer: {str(e)}"
        )

@app.post("/api/game/{uid}/reset", response_model=QuestionResponse)
async def reset_game(uid: str):
    """Reset the current game."""
    try:
        # Create new game instance (use environment API key)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return QuestionResponse(
                success=False,
                question="",
                game_state=get_default_error_state(),
                error="ANTHROPIC_API_KEY environment variable is required"
            )
            
        game = InterviewBossGame(api_key=api_key)
        game_instances[uid] = game
        
        # Get first question
        question = game.get_question()
        
        return QuestionResponse(
            success=True,
            question=question,
            game_state=create_game_state_response(game)
        )
        
    except Exception as e:
        return QuestionResponse(
            success=False,
            question="",
            game_state=get_default_error_state(),
            error=f"Failed to reset game: {str(e)}"
        )

@app.delete("/api/game/{uid}")
async def end_game(uid: str):
    """End the current game and clean up resources."""
    if uid in game_instances:
        del game_instances[uid]
        return {"success": True, "message": "Game ended successfully"}
    else:
        return {"success": False, "message": "No active game found"}

@app.get("/api/game/{uid}/history")
async def get_conversation_history(uid: str):
    """Get the conversation history for the current game."""
    if uid not in game_instances:
        raise HTTPException(status_code=404, detail="No active game found")
    
    game = game_instances[uid]
    history = game.get_conversation_history()
    
    return {
        "success": True,
        "conversation_history": history,
        "total_messages": len(history),
        "game_state": create_game_state_response(game)
    }

# ================== DEVELOPMENT SERVER ==================

if __name__ == "__main__":
    import uvicorn
    
    print("🎮 Starting InterviewOverfit Boss Battle Server...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("🛑 Press Ctrl+C to stop")
    
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
