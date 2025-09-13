# app/main.py
from __future__ import annotations
from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from pathlib import Path
import json
import os
import re
from datetime import datetime

from src.dataloader.jston_store import JsonStore, UserData
from src.interview_engine.interview_session import (
    SessionStore, InterviewSession, ChatMessage, AttemptSummary
)
from src.model_interaction.model import InterviewBossGame

app = FastAPI(title="InterviewOverfit API", version="0.1.0")

# Add CORS middleware for Node.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:3001",  # Alternative React port
        "http://localhost:8080",  # Vue default
        "http://localhost:4200",  # Angular default
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).parents[1]
user_store = JsonStore(root=PROJECT_ROOT)
session_store = SessionStore(root=PROJECT_ROOT)

# Game instances storage (in production, use Redis or database)
game_instances: Dict[str, InterviewBossGame] = {}

# Mount static files
app.mount("/static", StaticFiles(directory="web"), name="static")

# ---- (Optional) auth stub ----
class AuthedUser(BaseModel):
    uid: str
def get_current_user(uid: Optional[str] = None) -> AuthedUser:
    # wire real auth later (Firebase, etc.)
    if not uid:
        # for hackathon testing, default a demo uid
        uid = "demo-user"
    return AuthedUser(uid=uid)

# ---- Schemas for request bodies ----
class CreateSessionIn(BaseModel):
    domain: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class AddMessageIn(BaseModel):
    role: str  # "interviewer" | "candidate" | "system"
    content: str

class RecordAttemptIn(BaseModel):
    question: str
    answer: str
    score: str  # "-10" .. "+10"

# Boss Battle Game Schemas
class StartGameIn(BaseModel):
    api_key: Optional[str] = None

class SubmitAnswerIn(BaseModel):
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

class GameResponse(BaseModel):
    success: bool
    message: str
    game_state: GameStateResponse
    error: Optional[str] = None

class QuestionResponse(BaseModel):
    success: bool
    question: str
    game_state: GameStateResponse
    error: Optional[str] = None

class AnswerResponse(BaseModel):
    success: bool
    score: int
    feedback: str
    next_question: str
    game_state: GameStateResponse
    error: Optional[str] = None

# ---------------- Endpoints ----------------

@app.get("/")
def serve_game():
    """Serve the main game interface."""
    return FileResponse("web/index.html")

@app.get("/health")
def health():
    return {"status": "ok", "service": "Interview Boss Battle API"}

@app.get("/api/info")
def api_info():
    """Get API information for frontend integration."""
    return {
        "name": "Interview Boss Battle API",
        "version": "1.0.0",
        "description": "Gamified interview preparation system",
        "endpoints": {
            "start_game": "POST /game/{uid}/start",
            "submit_answer": "POST /game/{uid}/answer", 
            "get_question": "GET /game/{uid}/question",
            "get_status": "GET /game/{uid}/status",
            "reset_game": "POST /game/{uid}/reset",
            "end_game": "DELETE /game/{uid}",
            "get_history": "GET /game/{uid}/history"
        },
        "cors_enabled": True,
        "supported_origins": [
            "http://localhost:3000",
            "http://localhost:3001", 
            "http://localhost:8080",
            "http://localhost:4200",
            "http://localhost:5173"
        ]
    }

# --- User ---
@app.post("/users/{uid}", response_model=UserData)
def create_or_load_user(uid: str, name: Optional[str] = None, email: Optional[str] = None):
    # idempotent create; returns existing if present
    user = user_store.create_user(uid=uid, name=name or "Guest", email=email)
    return user

@app.get("/users/{uid}", response_model=UserData)
def get_user(uid: str):
    user = user_store.get_user(uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{uid}/progress")
def get_progress(uid: str):
    user = user_store.get_user(uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "uid": user.uid,
        "xp": user.xp,
        "level": user.level,
        "streak": user.streak,
        "achievements": user.achievements,
        "attempts_count": len(user.attempts),
        "last_attempt_ts": user.last_attempt_ts,
        "skills": user.skills,
    }

# --- Sessions ---
@app.post("/sessions", response_model=InterviewSession)
def create_session(
    payload: CreateSessionIn = Body(...),
    me: AuthedUser = Depends(get_current_user),
):
    # ensure user exists
    user_store.create_user(uid=me.uid)
    sess = session_store.create_session(uid=me.uid, domain=payload.domain, meta=payload.meta or {})
    return sess

@app.get("/sessions/{uid}", response_model=list[str])
def list_sessions(uid: str):
    return session_store.list_sessions(uid)

@app.get("/sessions/{uid}/{session_id}", response_model=InterviewSession)
def get_session(uid: str, session_id: str):
    sess = session_store.load(uid, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return sess

@app.post("/sessions/{uid}/{session_id}/messages", response_model=InterviewSession)
def add_message(uid: str, session_id: str, payload: AddMessageIn):
    sess = session_store.load(uid, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    # basic validation of role
    if payload.role not in {"interviewer", "candidate", "system"}:
        raise HTTPException(status_code=422, detail="role must be interviewer|candidate|system")
    sess.add_message(role=payload.role, content=payload.content)
    session_store.save(sess)
    return sess

@app.post("/sessions/{uid}/{session_id}/attempts", response_model=InterviewSession)
def record_attempt(uid: str, session_id: str, payload: RecordAttemptIn):
    # 1) append to session attempts + chat
    sess = session_store.load(uid, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    sess.record_attempt(question=payload.question, answer=payload.answer, score=payload.score)
    session_store.save(sess)

    # 2) also append to user attempts (denormalized summary)
    user = user_store.get_user(uid)
    if not user:
        # ensure user exists in strange edge case
        user = user_store.create_user(uid=uid)
    user.add_attempt(question=payload.question, answer=payload.answer, score=payload.score)
    user_store.upsert_user(user)

    return sess

@app.post("/sessions/{uid}/{session_id}/close", response_model=InterviewSession)
def close_session(uid: str, session_id: str):
    sess = session_store.load(uid, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    sess.close()
    session_store.save(sess)
    return sess

# ---------------- Boss Battle Game Endpoints ----------------

@app.post("/game/{uid}/start", response_model=QuestionResponse)
def start_boss_battle_game(
    uid: str, 
    payload: StartGameIn = Body(...),
    me: AuthedUser = Depends(get_current_user)
):
    """Start a new boss battle game for the user."""
    try:
        # Create new game instance
        game = InterviewBossGame(api_key=payload.api_key)
        game_instances[uid] = game
        
        # Get first question
        question = game.get_question()
        game_state = game.get_game_state()
        
        return QuestionResponse(
            success=True,
            question=question,
            game_state=GameStateResponse(**game_state)
        )
    except Exception as e:
        return QuestionResponse(
            success=False,
            question="",
            game_state=GameStateResponse(
                level=1, max_level=3, boss_name="", boss_personality="", 
                boss_question_types=[], boss_hp=0, max_hp=100, user_hp=0, 
                turn_count=0, current_question="", game_over=True, 
                victory=False, conversation_length=0
            ),
            error=f"Failed to start game: {str(e)}"
        )

@app.get("/game/{uid}/status", response_model=GameStateResponse)
def get_game_status(uid: str, me: AuthedUser = Depends(get_current_user)):
    """Get current game status."""
    if uid not in game_instances:
        raise HTTPException(status_code=404, detail="No active game found")
    
    game = game_instances[uid]
    game_state = game.get_game_state()
    return GameStateResponse(**game_state)

@app.post("/game/{uid}/answer", response_model=AnswerResponse)
def submit_answer(
    uid: str, 
    payload: SubmitAnswerIn = Body(...),
    me: AuthedUser = Depends(get_current_user)
):
    """Submit an answer to the current question."""
    if uid not in game_instances:
        return AnswerResponse(
            success=False,
            score=0,
            feedback="No active game found",
            next_question="",
            game_state=GameStateResponse(
                level=1, max_level=3, boss_name="", boss_personality="", 
                boss_question_types=[], boss_hp=0, max_hp=100, user_hp=0, 
                turn_count=0, current_question="", game_over=True, 
                victory=False, conversation_length=0
            ),
            error="No active game found"
        )
    
    try:
        game = game_instances[uid]
        
        # Submit answer and get response
        response = game.submit_answer(payload.answer)
        game_state = game.get_game_state()
        
        # Parse the XML-structured response
        score = 0
        feedback = ""
        next_question = ""
        
        try:
            # Extract score
            score_match = re.search(r'<score>\s*([+-]?\d+)\s*</score>', response)
            if score_match:
                score = int(score_match.group(1))
                # Clamp the score to the allowed range [-10, 10]
                score = max(-10, min(10, score))
                print(f"Extracted score: {score}")
            else:
                print(f"No score found in response: {response[:200]}...")
            
            # Extract feedback
            feedback_match = re.search(r'<feedback>\s*(.*?)\s*</feedback>', response, re.DOTALL)
            if feedback_match:
                feedback = feedback_match.group(1).strip()
                print(f"Extracted feedback: {feedback[:100]}...")
            else:
                print(f"No feedback found in response: {response[:200]}...")
            
            # Extract next question
            question_match = re.search(r'<question>\s*(.*?)\s*</question>', response, re.DOTALL)
            if question_match:
                next_question = question_match.group(1).strip()
                print(f"Extracted question: {next_question[:100]}...")
            else:
                print(f"No question found in response: {response[:200]}...")
            
        except Exception as e:
            # Fallback to old parsing if XML parsing fails
            feedback = response
            print(f"XML parsing failed: {e}")
        
        # If game is over, clean up the instance
        if game.game_over:
            del game_instances[uid]
        
        return AnswerResponse(
            success=True,
            score=score,
            feedback=feedback,
            next_question=next_question,
            game_state=GameStateResponse(**game_state)
        )
    except Exception as e:
        return AnswerResponse(
            success=False,
            score=0,
            feedback="",
            next_question="",
            game_state=GameStateResponse(
                level=1, max_level=3, boss_name="", boss_personality="", 
                boss_question_types=[], boss_hp=0, max_hp=100, user_hp=0, 
                turn_count=0, current_question="", game_over=True, 
                victory=False, conversation_length=0
            ),
            error=f"Failed to submit answer: {str(e)}"
        )

@app.get("/game/{uid}/question", response_model=QuestionResponse)
def get_next_question(uid: str, me: AuthedUser = Depends(get_current_user)):
    """Get the next question from the current boss."""
    if uid not in game_instances:
        return QuestionResponse(
            success=False,
            question="No active game found",
            game_state=GameStateResponse(
                level=1, max_level=3, boss_name="", boss_personality="", 
                boss_question_types=[], boss_hp=0, max_hp=100, user_hp=0, 
                turn_count=0, current_question="", game_over=True, 
                victory=False, conversation_length=0
            ),
            error="No active game found"
        )
    
    try:
        game = game_instances[uid]
        
        if game.game_over:
            return QuestionResponse(
                success=False,
                question="Game is over",
                game_state=GameStateResponse(**game.get_game_state()),
                error="Game is over"
            )
        
        question = game.get_question()
        game_state = game.get_game_state()
        
        return QuestionResponse(
            success=True,
            question=question,
            game_state=GameStateResponse(**game_state)
        )
    except Exception as e:
        return QuestionResponse(
            success=False,
            question="",
            game_state=GameStateResponse(
                level=1, max_level=3, boss_name="", boss_personality="", 
                boss_question_types=[], boss_hp=0, max_hp=100, user_hp=0, 
                turn_count=0, current_question="", game_over=True, 
                victory=False, conversation_length=0
            ),
            error=f"Failed to get question: {str(e)}"
        )

@app.post("/game/{uid}/reset", response_model=QuestionResponse)
def reset_game(uid: str, me: AuthedUser = Depends(get_current_user)):
    """Reset the current game."""
    try:
        # Create new game instance
        game = InterviewBossGame()
        game_instances[uid] = game
        
        # Get first question
        question = game.get_question()
        game_state = game.get_game_state()
        
        return QuestionResponse(
            success=True,
            question=question,
            game_state=GameStateResponse(**game_state)
        )
    except Exception as e:
        return QuestionResponse(
            success=False,
            question="",
            game_state=GameStateResponse(
                level=1, max_level=3, boss_name="", boss_personality="", 
                boss_question_types=[], boss_hp=0, max_hp=100, user_hp=0, 
                turn_count=0, current_question="", game_over=True, 
                victory=False, conversation_length=0
            ),
            error=f"Failed to reset game: {str(e)}"
        )

@app.delete("/game/{uid}")
def end_game(uid: str, me: AuthedUser = Depends(get_current_user)):
    """End the current game and clean up resources."""
    if uid in game_instances:
        del game_instances[uid]
        return {"success": True, "message": "Game ended successfully"}
    else:
        return {"success": False, "message": "No active game found"}

@app.get("/game/{uid}/history")
def get_conversation_history(uid: str, me: AuthedUser = Depends(get_current_user)):
    """Get the conversation history for the current game."""
    if uid not in game_instances:
        raise HTTPException(status_code=404, detail="No active game found")
    
    game = game_instances[uid]
    history = game.get_conversation_history()
    
    return {
        "conversation_history": history,
        "total_messages": len(history)
    }


@app.get("/game/{uid}/save")
def save_game_state(uid: str, filename: str = None, me: AuthedUser = Depends(get_current_user)):
    """Save game state to a file."""
    if uid not in game_instances:
        raise HTTPException(status_code=404, detail="No active game found")
    
    try:
        game = game_instances[uid]
        
        # Generate filename if not provided
        if not filename:
            filename = f"game_save.json"
            
        # Save to file
        filepath = f"saves/{filename}"
        os.makedirs("saves", exist_ok=True)  # Create saves directory if it doesn't exist
        
        game.dump_game_state_to_json(filepath)
        
        return {
            "success": True,
            "message": f"Game state saved to {filepath}",
            "filename": filename,
            "filepath": filepath,
            "save_timestamp": datetime.now().isoformat(),
            "user_id": uid
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save game state: {str(e)}")

@app.get("/game/{uid}/load")
def load_game_state(uid: str, filename: str = None, me: AuthedUser = Depends(get_current_user)):
    """Load game state from a JSON file."""
    try:
        # Generate filename if not provided
        if not filename:
            filename = f"game_save.json"
            
        # Load from file
        filepath = f"saves/{filename}"
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail=f"Save file not found: {filepath}")
        
        # Read the JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = f.read()
        
        # Create new game instance and load the state
        game = InterviewBossGame()
        loaded_data = game.load_game_state_from_json(json_data)
        
        if loaded_data:  # If loading was successful
            game_instances[uid] = game
            return {
                "success": True,
                "message": f"Game state loaded from {filepath}",
                "filename": filename,
                "filepath": filepath,
                "game_data": loaded_data
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid game state data in file")
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Save file not found: {filepath}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load game state: {str(e)}")

# ---- Quick run hint (uvicorn) ----
# uvicorn app.main:app --reload
