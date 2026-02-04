from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Text, String, Float
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import JSON
from app.db import Base

class TrainingSession(Base):
    __tablename__ = "training_sessions"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    transcript = Column(Text, nullable=False)
    feedback = Column(Text, nullable=False)
    audio_path = Column(String(512), nullable=True)
    tts_audio_path = Column(String(512), nullable=True)
    voice_features_json = Column(JSON, nullable=False)
    model_name = Column(String(64), nullable=False)
    duration_seconds = Column(Float, nullable=True)
