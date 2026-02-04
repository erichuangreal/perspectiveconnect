import numpy as np
import librosa
import parselmouth
from app.services.wav_service import ensure_wav

def extract_voice_features(audio_path: str) -> dict:
    wav_path = ensure_wav(audio_path)
    y, sr = librosa.load(wav_path, mono=True)

    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    pitch_track = []
    for t in range(pitches.shape[1]):
        idx = magnitudes[:, t].argmax()
        p = float(pitches[idx, t])
        if p > 0:
            pitch_track.append(p)
    if len(pitch_track) == 0:
        pitch_track = [0.0]
    pitch_track = np.array(pitch_track, dtype=np.float64)

    S = np.abs(librosa.stft(y))
    loudness = librosa.amplitude_to_db(S, ref=np.max)

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    spectral_flatness = float(librosa.feature.spectral_flatness(y=y).mean())
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr).mean(axis=1)
    spectral_rolloff = float(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85).mean())

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    syllable_count = float(np.sum(onset_env > np.mean(onset_env)))
    total_duration = float(librosa.get_duration(y=y, sr=sr))
    syllables_per_second = float(syllable_count / total_duration) if total_duration > 0 else 0.0

    jitter = None
    shimmer = None
    hnr = None
    voice_quality_note = "ok"
    try:
        snd = parselmouth.Sound(wav_path)
        if snd.n_channels > 1:
            snd = snd.convert_to_mono()

        if snd.get_total_duration() < 0.6:
            voice_quality_note = "audio too short for jitter/shimmer/hnr"
        else:
            pitch_floor = 75
            pitch_ceiling = 500

            pp = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)", pitch_floor, pitch_ceiling)
            jitter = float(parselmouth.praat.call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3))
            shimmer = float(parselmouth.praat.call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6))

            harm = parselmouth.praat.call(snd, "To Harmonicity (cc)", 0.01, pitch_floor, 0.1, 1.0)
            hnr = float(parselmouth.praat.call(harm, "Get mean", 0, 0))
    except Exception:
        voice_quality_note = "praat failed, returning None for jitter/shimmer/hnr"

    return {
        "pitch_mean": float(np.mean(pitch_track)),
        "pitch_std": float(np.std(pitch_track)),
        "loudness_mean": float(np.mean(loudness)),
        "loudness_std": float(np.std(loudness)),
        "spectral_centroid_mean": float(np.mean(spectral_centroid)),
        "spectral_bandwidth_mean": float(np.mean(spectral_bandwidth)),
        "mfccs_mean": [float(x) for x in np.mean(mfccs, axis=1)],
        "syllables_per_second": float(syllables_per_second),
        "spectral_flatness_mean": float(spectral_flatness),
        "spectral_contrast_mean": [float(x) for x in spectral_contrast.tolist()],
        "spectral_rolloff_mean": float(spectral_rolloff),
        "jitter": jitter,
        "shimmer": shimmer,
        "hnr": hnr,
        "voice_quality_note": voice_quality_note,
        "duration_seconds": total_duration,
    }
