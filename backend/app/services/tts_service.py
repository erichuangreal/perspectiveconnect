import os
import time
import uuid
from gtts import gTTS
from app.config import settings

def tts_to_file(text: str) -> str:
    os.makedirs(settings.AUDIO_STORAGE_DIR, exist_ok=True)
    name = f"tts_{int(time.time())}_{uuid.uuid4().hex}.mp3"
    path = os.path.join(settings.AUDIO_STORAGE_DIR, name)
    gTTS(text=text, lang="en").save(path)
    return path
