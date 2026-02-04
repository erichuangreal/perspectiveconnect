import os
import time
import uuid
from app.config import settings

def save_upload_to_storage(upload_file) -> str:
    os.makedirs(settings.AUDIO_STORAGE_DIR, exist_ok=True)
    ext = os.path.splitext(upload_file.filename or "")[1].lower()
    if ext not in [".wav", ".mp3", ".m4a", ".webm", ".ogg"]:
        ext = ".webm"
    name = f"{int(time.time())}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.AUDIO_STORAGE_DIR, name)
    with open(path, "wb") as f:
        f.write(upload_file.file.read())
    return path
