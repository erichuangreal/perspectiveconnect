from typing import Any, Dict

def build_training_prompt(
    transcript: str,
    voice_features: Dict[str, Any],
    goal: str,
    audience: str,
    time_limit_seconds: int,
    rubric: str,
) -> str:
    return f"""
Presentation context
Goal: {goal}
Audience: {audience}
Time limit seconds: {time_limit_seconds}
Rubric: {rubric}

Presentation transcript
{transcript}

Voice features (numbers)
{voice_features}

Coaching reference ranges
Speech rate: 2.0 to 3.5 syllables per second is typical for clear speaking, above 4.0 often sounds rushed
Pitch variability: low pitch_std can sound monotone, very high pitch_std can sound nervous
Loudness variability: low loudness_std can sound flat, very high can sound uneven
HNR: higher usually indicates clearer tone, very low can indicate breathiness or noise

Now give coaching following the required structure.
""".strip()
