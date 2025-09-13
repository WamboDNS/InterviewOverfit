# app/storage/json_store.py
from __future__ import annotations
import json, os, threading, uuid, time
from pathlib import Path
from typing import Optional, Callable, List
from pydantic import BaseModel, Field, validator

# ---- Models (paste yours here or import from your models module) ----
class AttemptSummary(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    question: str
    answer: str
    score: str
    ts: int = Field(default_factory=lambda: int(time.time()))
    @validator("score")
    def validate_score(cls, v: str) -> str:
        if not isinstance(v, str): raise ValueError("score must be a string")
        try: val = int(v)
        except ValueError: raise ValueError("score must be a stringified integer")
        if val < -10 or val > 10: raise ValueError("score must be between -10 and +10")
        return f"{val:+d}"

class UserData(BaseModel):
    version: int = 1
    uid: str
    name: str = "Guest"
    email: Optional[str] = None
    xp: int = 0
    level: int = 1
    streak: int = 0
    last_attempt_ts: Optional[int] = None
    skills: dict[str, int] = Field(default_factory=dict)
    achievements: list[str] = Field(default_factory=list)
    attempts: list[AttemptSummary] = Field(default_factory=list)
    @validator("level", pre=True, always=True)
    def clamp_level(cls, v):
        try: ival = int(v)
        except Exception: ival = 1
        return max(1, min(100, ival))
    def add_attempt(self, question: str, answer: str, score: str) -> AttemptSummary:
        att = AttemptSummary(question=question, answer=answer, score=score)
        self.attempts.append(att); self.last_attempt_ts = att.ts; return att
    def grant_xp(self, amount: int) -> None:
        self.xp = max(0, self.xp + int(amount))
        self.level = max(1, int((self.xp / 300) ** 0.77) + 1)
    def earn_achievement(self, key: str) -> None:
        if key not in self.achievements: self.achievements.append(key)

# ---- Paths helper ----
class Paths:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.users_dir = self.root / "data" / "users"
        self.users_dir.mkdir(parents=True, exist_ok=True)
    def user_file(self, uid: str) -> Path:
        return self.users_dir / f"{uid}.json"

# ---- JSON store with atomic IO & in-process locks ----
class JsonStore:
    def __init__(self, root: str | Path):
        self.paths = Paths(Path(root))
        self._locks: dict[Path, threading.Lock] = {}
        self._global = threading.Lock()

    def _lock(self, path: Path) -> threading.Lock:
        with self._global:
            return self._locks.setdefault(path, threading.Lock())

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

    # ---- Public API ----
    def create_user(self, uid: str, name: str = "Guest", email: Optional[str] = None) -> UserData:
        p = self.paths.user_file(uid); lk = self._lock(p)
        with lk:
            if p.exists(): return self._load(uid)
            user = UserData(uid=uid, name=name, email=email)
            self._atomic_write(p, json.loads(user.json())); return user

    def get_user(self, uid: str) -> Optional[UserData]:
        p = self.paths.user_file(uid)
        return self._load(uid) if p.exists() else None

    def upsert_user(self, user: UserData) -> UserData:
        p = self.paths.user_file(user.uid); lk = self._lock(p)
        with lk:
            self._atomic_write(p, json.loads(user.json())); return user

    def update_user(self, uid: str, fn: Callable[[UserData], Optional[UserData]]) -> UserData:
        """Atomically load → mutate via fn(UserData) → save → return."""
        p = self.paths.user_file(uid); lk = self._lock(p)
        with lk:
            user = self._load_or_create(uid)
            maybe = fn(user)
            if isinstance(maybe, UserData): user = maybe
            self._atomic_write(p, json.loads(user.json())); return user

    def list_user_ids(self) -> List[str]:
        return sorted([p.stem for p in self.paths.users_dir.glob("*.json")])

    # ---- internals ----
    def _load(self, uid: str) -> UserData:
        p = self.paths.user_file(uid); lk = self._lock(p)
        with lk:
            raw = self._read_json(p)
        return UserData.parse_obj(raw)

    def _load_or_create(self, uid: str) -> UserData:
        p = self.paths.user_file(uid)
        if p.exists(): return self._load(uid)
        user = UserData(uid=uid); self._atomic_write(p, json.loads(user.json())); return user