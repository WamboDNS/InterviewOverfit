# app/services/interview_session.py
from __future__ import annotations
import json, os, time, uuid
from pathlib import Path
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, validator


# ---- Attempt, Message, and Session Models ----

class AttemptSummary(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    question: str
    answer: str
    score: str                             # "-10" .. "+10" (string)
    ts: int = Field(default_factory=lambda: int(time.time()))

    @validator("score")
    def validate_score(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("score must be a string")
        try:
            val = int(v)
        except ValueError:
            raise ValueError("score must be a stringified integer")
        if val < -10 or val > 10:
            raise ValueError("score must be between -10 and +10")
        return f"{val:+d}"


Role = Literal["interviewer", "candidate", "system"]

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    role: Role
    content: str
    ts: int = Field(default_factory=lambda: int(time.time()))


class InterviewSession(BaseModel):
    """
    A single interview session where the LLM freely asks questions.
    - messages: full chat log (interviewer/candidate/system)
    - attempts: denormalized Q/A + score for quick analytics
    """
    session_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    uid: str
    domain: Optional[str] = None          # e.g., "SWE", "MLE", "DS", "PM"
    started_at: int = Field(default_factory=lambda: int(time.time()))
    ended_at: Optional[int] = None
    messages: List[ChatMessage] = Field(default_factory=list)
    attempts: List[AttemptSummary] = Field(default_factory=list)
    meta: dict = Field(default_factory=dict)  # freeform flags/config for the run

    def add_message(self, role: Role, content: str) -> ChatMessage:
        msg = ChatMessage(role=role, content=content)
        self.messages.append(msg)
        return msg

    def record_attempt(self, question: str, answer: str, score: str) -> AttemptSummary:
        att = AttemptSummary(question=question, answer=answer, score=score)
        self.attempts.append(att)
        # Keep chat log consistent (optional but handy)
        self.messages.append(ChatMessage(role="interviewer", content=question))
        self.messages.append(ChatMessage(role="candidate", content=answer))
        return att

    def close(self) -> None:
        self.ended_at = int(time.time())


# ---- File-backed Session Manager (JSON, atomic writes) ----

class SessionPaths:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.base = self.root / "data" / "sessions"
        self.base.mkdir(parents=True, exist_ok=True)

    def user_dir(self, uid: str) -> Path:
        d = self.base / uid
        d.mkdir(parents=True, exist_ok=True)
        return d

    def session_file(self, uid: str, session_id: str) -> Path:
        return self.user_dir(uid) / f"{session_id}.json"

    def index_file(self, uid: str) -> Path:
        # Optional lightweight index of session_ids for quick lists
        return self.user_dir(uid) / "_index.json"


class SessionStore:
    """
    Minimal JSON session store:
      - Each session -> data/sessions/<uid>/<session_id>.json
      - Optional per-user _index.json to list sessions quickly
      - Atomic writes via temp + os.replace
    """
    def __init__(self, root: str | Path):
        self.paths = SessionPaths(Path(root))

    # --- IO helpers ---
    @staticmethod
    def _atomic_write(path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + f".tmp-{uuid.uuid4().hex}")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
        os.replace(tmp, path)

    @staticmethod
    def _read_json(path: Path) -> dict:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    # --- Public API ---
    def create_session(self, uid: str, domain: Optional[str] = None, meta: Optional[dict] = None) -> InterviewSession:
        sess = InterviewSession(uid=uid, domain=domain, meta=meta or {})
        self.save(sess)
        self._upsert_index(uid, sess.session_id)
        return sess

    def load(self, uid: str, session_id: str) -> Optional[InterviewSession]:
        f = self.paths.session_file(uid, session_id)
        if not f.exists():
            return None
        raw = self._read_json(f)
        return InterviewSession.parse_obj(raw)

    def save(self, session: InterviewSession) -> None:
        f = self.paths.session_file(session.uid, session.session_id)
        self._atomic_write(f, json.loads(session.json()))

    def list_sessions(self, uid: str) -> List[str]:
        idx = self.paths.index_file(uid)
        if idx.exists():
            try:
                data = self._read_json(idx)
                if isinstance(data, dict) and "session_ids" in data:
                    return list(data["session_ids"])
            except Exception:
                pass
        # fallback: scan directory
        return sorted([p.stem for p in self.paths.user_dir(uid).glob("*.json") if p.stem != "_index"])

    def _upsert_index(self, uid: str, session_id: str) -> None:
        idx = self.paths.index_file(uid)
        payload = {"session_ids": []}
        if idx.exists():
            try:
                payload = self._read_json(idx)
            except Exception:
                payload = {"session_ids": []}
        if session_id not in payload["session_ids"]:
            payload["session_ids"].append(session_id)
        self._atomic_write(idx, payload)