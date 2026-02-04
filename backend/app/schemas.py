from pydantic import BaseModel, EmailStr
from typing import Optional, Any, Dict, List
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Any, Dict

class TrainingListItem(BaseModel):
    id: int
    created_at: str
    duration_seconds: Optional[float] = None
    transcript_preview: str

class TrainingDetailOut(BaseModel):
    id: int
    created_at: str
    duration_seconds: Optional[float] = None
    transcript: str
    feedback: str
    voice_features: Dict[str, Any]
    analytics: Dict[str, Any]

class RegisterIn(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginIn(BaseModel):
    identifier: str
    password: str

class TokenOut(BaseModel):
    token: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

class TrainingSubmitOut(BaseModel):
    session_id: int
    transcript: str
    feedback: str
    voice_features: Dict[str, Any]

class TrainingListItem(BaseModel):
    id: int
    created_at: datetime
    duration_seconds: Optional[float]
    transcript_preview: str

class TrainingDetailOut(BaseModel):
    id: int
    created_at: datetime
    transcript: str
    feedback: str
    voice_features: Dict[str, Any]
    duration_seconds: Optional[float]
