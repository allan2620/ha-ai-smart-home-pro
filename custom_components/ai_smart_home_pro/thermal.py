"""Pure diagnostic calculations for indoor/outdoor temperature observations."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from math import isfinite
from typing import Iterable


def calculate_trend(samples: Iterable[tuple[datetime, float]]) -> float | None:
    """Observed °C/hour over at least 30 minutes, not a forecast."""
    samples = list(samples)
    if len(samples) < 2:
        return None
    last_time, last_value = samples[-1]
    for stamp, value in samples:
        elapsed = (last_time - stamp).total_seconds() / 3600
        if elapsed >= 0.5:
            return round((last_value - value) / elapsed, 3)
    return None


def quality_label(samples: Iterable[tuple[datetime, float]]) -> str:
    """History coverage indicator, not confidence in predictions."""
    samples = list(samples)
    if len(samples) < 2:
        return "Afventer målinger"
    hours = (samples[-1][0] - samples[0][0]).total_seconds() / 3600
    if len(samples) >= 72 and hours >= 12:
        return "God datadækning"
    if len(samples) >= 12 and hours >= 2:
        return "Delvis datadækning"
    return "For lidt historik"


def restore_history(raw: object, now: datetime, hours: int = 72) -> list[tuple[datetime, float]]:
    """Validate stored single-temperature observations."""
    if not isinstance(raw, list):
        return []
    cutoff = now - timedelta(hours=hours)
    valid = []
    for item in raw[-(hours * 12 + 100):]:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            continue
        try:
            stamp = datetime.fromisoformat(item[0])
            value = float(item[1])
        except (ValueError, TypeError, OverflowError):
            continue
        if stamp.tzinfo and cutoff <= stamp <= now and isfinite(value) and 5 <= value <= 40:
            valid.append((stamp.astimezone(timezone.utc), value))
    valid.sort(key=lambda x: x[0])
    return valid[-hours * 12:]


def restore_pairs(raw: object, now: datetime, hours: int = 72) -> list[tuple[datetime, float, float]]:
    """Restore safe indoor/outdoor observations; reject impossible readings."""
    if not isinstance(raw, list):
        return []
    cutoff = now - timedelta(hours=hours)
    valid = []
    for item in raw[-(hours * 12 + 100):]:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            continue
        try:
            stamp = datetime.fromisoformat(item[0])
            indoor, outdoor = float(item[1]), float(item[2])
        except (ValueError, TypeError, OverflowError):
            continue
        if (
            stamp.tzinfo and cutoff <= stamp <= now
            and isfinite(indoor) and 5 <= indoor <= 40
            and isfinite(outdoor) and -45 <= outdoor <= 55
        ):
            valid.append((stamp.astimezone(timezone.utc), indoor, outdoor))
    valid.sort(key=lambda x: x[0])
    return valid[-hours * 12:]


def mean_temperature_gap(pairs: Iterable[tuple[datetime, float, float]]) -> float | None:
    """Mean indoor-minus-outdoor °C across most recent 24 hours of pairs."""
    pairs = list(pairs)
    if len(pairs) < 12:
        return None
    cutoff = pairs[-1][0] - timedelta(hours=24)
    recent = [(t, i, o) for t, i, o in pairs if t >= cutoff]
    if len(recent) < 12 or (recent[-1][0] - recent[0][0]) < timedelta(hours=2):
        return None
    return round(sum(i - o for _, i, o in recent) / len(recent), 2)


def heating_observation(trend: float | None, indoor: float | None, target: float) -> str:
    """Describe measurements without interpreting cause or controlling heating."""
    if trend is None or indoor is None:
        return "Afventer temperaturhistorik"
    if indoor < target - 0.5 and trend < -0.05:
        return "Under mål og faldende"
    if indoor > target + 0.5 and trend > 0.05:
        return "Over mål og stigende"
    if abs(trend) <= 0.05:
        return "Temperaturen er omtrent stabil"
    return "Temperaturen stiger" if trend > 0 else "Temperaturen falder"
