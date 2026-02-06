import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.config import settings
from app.db import Base, engine
from app.models import User, TrainingSession
from app.schemas import RegisterIn, LoginIn, TokenOut, UserOut, TrainingSubmitOut, TrainingListItem, TrainingDetailOut
from app.security import hash_password, verify_password, create_token
from app.deps import get_db, get_current_user

from app.services.storage_service import save_upload_to_storage
from app.services.transcription_service import transcribe_with_whisper
from app.services.speech_features_service import extract_voice_features
from app.services.prompt_service import build_training_prompt
from app.services.llm_service import generate_feedback
from app.services.tts_service import tts_to_file
from app.services.analytics_service import compute_analytics

Base.metadata.create_all(bind=engine)
os.makedirs(settings.AUDIO_STORAGE_DIR, exist_ok=True)


app = FastAPI(title="perspectiveconnect api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://159.89.112.149:3000",
        "https://159.89.112.149:3000",
        "https://pc.appfounder.ca",
        "http://pc.appfounder.ca",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auth/register", response_model=TokenOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_token(user.id)}


@app.post("/auth/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.email == payload.identifier) | (User.username == payload.identifier)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token(user.id)}


@app.get("/auth/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/training/sessions", response_model=list[TrainingListItem])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(TrainingSession)
        .filter(TrainingSession.user_id == current_user.id)
        .order_by(TrainingSession.created_at.desc())
        .all()
    )

    out = []
    for s in rows:
        transcript = (s.transcript or "").strip()
        preview = transcript[:160] + ("..." if len(transcript) > 160 else "")
        vf = s.voice_features_json or {}
        out.append({
            "id": int(s.id),
            "created_at": s.created_at.isoformat(),
            "duration_seconds": vf.get("duration_seconds"),
            "transcript_preview": preview,
        })
    return out

@app.get("/training/sessions/{session_id}", response_model=TrainingDetailOut)
def get_session_detail(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    s = (
        db.query(TrainingSession)
        .filter(TrainingSession.id == session_id, TrainingSession.user_id == current_user.id)
        .first()
    )
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")

    vf = s.voice_features_json or {}
    an = s.analytics_json or {}

    return {
        "id": int(s.id),
        "created_at": s.created_at.isoformat(),
        "duration_seconds": vf.get("duration_seconds"),
        "transcript": (s.transcript or ""),
        "feedback": (s.feedback or ""),
        "voice_features": vf,
        "analytics": an,
    }

@app.get("/training/summary")
def training_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(TrainingSession)
        .filter(TrainingSession.user_id == current_user.id)
        .order_by(TrainingSession.created_at.asc())
        .all()
    )

    series = []
    for s in rows:
        vf = s.voice_features_json or {}
        an = s.analytics_json or {}
        series.append({
            "id": int(s.id),
            "created_at": s.created_at.isoformat(),
            "overall_score": an.get("overall_score"),
            "delivery_score": an.get("delivery_score"),
            "content_score": an.get("content_score"),
            "syllables_per_second": vf.get("syllables_per_second"),
            "pitch_std": vf.get("pitch_std"),
            "hnr": vf.get("hnr"),
            "filler_density": an.get("filler_density"),
        })

    return {"series": series}

@app.post("/training/submit", response_model=TrainingSubmitOut)
def submit_training(
    audio_file: UploadFile = File(...),
    goal: str = Form(default="inform"),
    audience: str = Form(default="classmates or interviewers"),
    time_limit_seconds: int = Form(default=180),
    rubric: str = Form(default="clarity, structure, technical accuracy, examples, pacing, confidence"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    audio_path = save_upload_to_storage(audio_file)

    transcript = transcribe_with_whisper(audio_path)
    voice_features = extract_voice_features(audio_path)

    # compute per-session analytics from transcript and voice features
    try:
        analytics = compute_analytics(transcript, voice_features)
    except Exception:
        analytics = {}

    prompt = build_training_prompt(
        transcript=transcript,
        voice_features=voice_features,
        goal=goal,
        audience=audience,
        time_limit_seconds=time_limit_seconds,
        rubric=rubric,
    )

    feedback = generate_feedback(prompt)

    tts_path = None
    try:
        tts_path = tts_to_file(feedback)
    except Exception:
        tts_path = None

    session = TrainingSession(
        user_id=current_user.id,
        transcript=transcript,
        feedback=feedback,
        audio_path=audio_path,
        tts_audio_path=tts_path,
        voice_features_json=voice_features,
    analytics_json=analytics,
        model_name=settings.MODEL_NAME,
        duration_seconds=voice_features.get("duration_seconds"),
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": int(session.id),
        "transcript": transcript,
        "feedback": feedback,
        "voice_features": voice_features,
    }
