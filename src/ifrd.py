from __future__ import annotations

from src.config import IFRD_WEIGHTS


def calculate_ifrd(scores: dict[str, int]) -> float:
    missing = [key for key in IFRD_WEIGHTS if key not in scores]
    if missing:
        raise ValueError(f"missing IFRD score fields: {missing}")
    invalid = {key: value for key, value in scores.items() if key in IFRD_WEIGHTS and not 1 <= value <= 5}
    if invalid:
        raise ValueError(f"IFRD scores must be between 1 and 5: {invalid}")
    return round(sum(scores[key] * weight for key, weight in IFRD_WEIGHTS.items()), 2)


def classify_ifrd(ifrd: float) -> tuple[str, str]:
    if ifrd >= 4.0:
        return "Bom Artigo", "green"
    if ifrd >= 3.0:
        return "Intermediário", "yellow"
    return "Fraco", "red"

