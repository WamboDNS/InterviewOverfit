# app/main.py
from __future__ import annotations
from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from pathlib import Path

from app.storage.json_store import JsonStore, UserData
from app.services.interview_session import (
    SessionStore, InterviewSession, ChatMessage, AttemptSummary
)

app = FastAPI(title="InterviewOverfit API", version="0.1.0")
PROJECT_ROOT = Path(__file__).parents[1]
user_store = JsonStore(root=PROJECT_ROOT)
session_store = SessionStore(root=PROJECT_ROOT)

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

# ---------------- Endpoints ----------------

@app.get("/health")
def health():
    return {"status": "ok"}

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

@app.get("/sessions/{uid}", response_model=List[str])
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

# ---- Quick run hint (uvicorn) ----
# uvicorn app.main:app --reload
