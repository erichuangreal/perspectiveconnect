import os
import subprocess
import uuid
from app.config import settings

def ensure_wav(input_path: str) -> str:
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".wav":
        return input_path

    os.makedirs(settings.AUDIO_STORAGE_DIR, exist_ok=True)
    out_path = os.path.join(settings.AUDIO_STORAGE_DIR, f"conv_{uuid.uuid4().hex}.wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        out_path,
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError("ffmpeg conversion failed")
    return out_path
