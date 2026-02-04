import os
from app.config import settings
from app.services.wav_service import ensure_wav


def _get_openai_client():
    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError("OpenAI client is unavailable: %s" % e)
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def transcribe_with_whisper(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        return ""
    wav_path = ensure_wav(audio_path)
    client = _get_openai_client()
    with open(wav_path, "rb") as f:
        text = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text",
        )
    return (text or "").strip()
