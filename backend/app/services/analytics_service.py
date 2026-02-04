import re
from typing import Dict, Any, Tuple, List

FILLERS = [
    "um", "uh", "like", "basically", "actually", "literally",
    "you know", "kind of", "sort of", "i mean"
]

VAGUE_PHRASES = [
    "things", "stuff", "a lot", "somehow", "maybe", "probably", "pretty much",
    "in a way", "etc"
]

def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def _score_band(x: float, good_lo: float, good_hi: float, bad_lo: float, bad_hi: float) -> float:
    """
    0..1 score:
    - 1 if within [good_lo, good_hi]
    - falls linearly to 0 at bad_lo or bad_hi
    """
    if x is None:
        return 0.5
    if good_lo <= x <= good_hi:
        return 1.0
    if x < good_lo:
        return _clamp((x - bad_lo) / (good_lo - bad_lo), 0.0, 1.0)
    return _clamp((bad_hi - x) / (bad_hi - good_hi), 0.0, 1.0)

def _count_phrases(text: str, phrases: List[str]) -> Dict[str, int]:
    t = text.lower()
    counts = {}
    for p in phrases:
        # word-boundary-ish match for single words, substring for multiword
        if " " in p:
            counts[p] = len(re.findall(re.escape(p), t))
        else:
            counts[p] = len(re.findall(r"\b" + re.escape(p) + r"\b", t))
    return counts

def _split_sentences(text: str) -> List[str]:
    # lightweight sentence split
    parts = re.split(r"[.!?]+", text)
    return [p.strip() for p in parts if p.strip()]

def compute_analytics(transcript: str, voice_features: Dict[str, Any]) -> Dict[str, Any]:
    transcript = (transcript or "").strip()
    vf = voice_features or {}

    syllables_per_second = vf.get("syllables_per_second")
    pitch_std = vf.get("pitch_std")
    loudness_std = vf.get("loudness_std")
    hnr = vf.get("hnr")

    # Delivery subscores (0..1)
    rate_score = _score_band(
        float(syllables_per_second) if syllables_per_second is not None else None,
        good_lo=2.0, good_hi=3.5,
        bad_lo=1.0, bad_hi=5.0
    )

    pitch_var_score = _score_band(
        float(pitch_std) if pitch_std is not None else None,
        good_lo=18.0, good_hi=55.0,
        bad_lo=5.0, bad_hi=90.0
    )

    loudness_stability_score = _score_band(
        float(loudness_std) if loudness_std is not None else None,
        good_lo=5.0, good_hi=12.0,
        bad_lo=2.0, bad_hi=22.0
    )

    clarity_score = None
    if hnr is not None:
        # HNR varies by recording conditions; keep broad
        clarity_score = _score_band(float(hnr), good_lo=12.0, good_hi=30.0, bad_lo=5.0, bad_hi=35.0)
    else:
        clarity_score = 0.6

    delivery_score_01 = (rate_score + pitch_var_score + loudness_stability_score + clarity_score) / 4.0

    # Content checks
    filler_counts = _count_phrases(transcript, FILLERS)
    vague_counts = _count_phrases(transcript, VAGUE_PHRASES)

    total_words = max(1, len(re.findall(r"\b\w+\b", transcript.lower())))
    total_fillers = sum(filler_counts.values())
    filler_density = total_fillers / total_words  # fraction

    sentences = _split_sentences(transcript)
    avg_sentence_words = 0.0
    if sentences:
        avg_sentence_words = sum(len(re.findall(r"\b\w+\b", s)) for s in sentences) / len(sentences)

    # Content subscores (0..1)
    filler_score = _clamp(1.0 - (filler_density / 0.06), 0.0, 1.0)  # 6% fillers = 0
    sentence_score = _score_band(avg_sentence_words, good_lo=10, good_hi=22, bad_lo=5, bad_hi=35)
    vague_score = _clamp(1.0 - (sum(vague_counts.values()) / max(1, len(sentences))) / 2.5, 0.0, 1.0)

    content_score_01 = (filler_score + sentence_score + vague_score) / 3.0

    # Flags
    flags = []
    if syllables_per_second is not None and syllables_per_second > 4.0:
        flags.append("rushed pacing")
    if syllables_per_second is not None and syllables_per_second < 1.8:
        flags.append("slow pacing")
    if pitch_std is not None and pitch_std < 12.0:
        flags.append("monotone risk")
    if loudness_std is not None and loudness_std > 14.0:
        flags.append("uneven loudness")
    if total_fillers >= 6:
        flags.append("high filler usage")

    delivery_score = round(delivery_score_01 * 100)
    content_score = round(content_score_01 * 100)
    overall_score = round(0.6 * delivery_score + 0.4 * content_score)

    return {
        "overall_score": overall_score,
        "delivery_score": delivery_score,
        "content_score": content_score,
        "filler_counts": filler_counts,
        "vague_counts": vague_counts,
        "total_words": total_words,
        "total_fillers": total_fillers,
        "filler_density": filler_density,
        "avg_sentence_words": avg_sentence_words,
        "flags": flags,
    }
