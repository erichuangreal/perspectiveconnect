from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import JSON
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class TrainingSession(Base):
    __tablename__ = "training_sessions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    transcript = Column(Text, nullable=False)
    feedback = Column(Text, nullable=False)

    audio_path = Column(String(512), nullable=True)
    tts_audio_path = Column(String(512), nullable=True)

    voice_features_json = Column(JSON, nullable=False)
    model_name = Column(String(64), nullable=False)
    duration_seconds = Column(Float, nullable=True)
    analytics_json = Column(JSON, nullable=True)
