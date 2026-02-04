import os
import time
import uuid
import librosa
import numpy as np
import parselmouth
from app.config import settings

def save_upload_to_storage(upload_file) -> str:
    os.makedirs(settings.AUDIO_STORAGE_DIR, exist_ok=True)
    ext = os.path.splitext(upload_file.filename or "")[1].lower() or ".wav"
    name = f"{int(time.time())}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.AUDIO_STORAGE_DIR, name)
    with open(path, "wb") as f:
        f.write(upload_file.file.read())
    return path

def extracting_audio_qualities(audio_path: str) -> dict:
    y, sr = librosa.load(audio_path, mono=True)

    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    pitch_track = []
    for t in range(pitches.shape[1]):
        idx = magnitudes[:, t].argmax()
        p = pitches[idx, t]
        if p > 0:
            pitch_track.append(p)
    pitch_track = np.array(pitch_track) if pitch_track else np.array([0.0])

    S = np.abs(librosa.stft(y))
    loudness = librosa.amplitude_to_db(S, ref=np.max)

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    syllable_count = float(np.sum(onset_env > np.mean(onset_env)))
    total_duration = float(librosa.get_duration(y=y, sr=sr))
    syllables_per_second = syllable_count / total_duration if total_duration > 0 else 0.0

    jitter = None
    shimmer = None
    hnr = None
    try:
        snd = parselmouth.Sound(audio_path)
        if snd.n_channels > 1:
            snd = snd.convert_to_mono()
        if snd.get_total_duration() >= 0.6:
            pitch_floor = 75
            pitch_ceiling = 500
            pp = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)", pitch_floor, pitch_ceiling)
            jitter = parselmouth.praat.call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
            shimmer = parselmouth.praat.call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            harm = parselmouth.praat.call(snd, "To Harmonicity (cc)", 0.01, pitch_floor, 0.1, 1.0)
            hnr = parselmouth.praat.call(harm, "Get mean", 0, 0)
    except Exception:
        pass

    return {
        "pitch_mean": float(np.mean(pitch_track)),
        "pitch_std": float(np.std(pitch_track)),
        "loudness_mean": float(np.mean(loudness)),
        "loudness_std": float(np.std(loudness)),
        "spectral_centroid_mean": float(np.mean(spectral_centroid)),
        "spectral_bandwidth_mean": float(np.mean(spectral_bandwidth)),
        "mfccs_mean": [float(x) for x in np.mean(mfccs, axis=1)],
        "syllables_per_second": float(syllables_per_second),
        "jitter": jitter,
        "shimmer": shimmer,
        "hnr": hnr,
        "duration_seconds": total_duration,
    }
