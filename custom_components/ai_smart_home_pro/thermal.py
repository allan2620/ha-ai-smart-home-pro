"""Diagnostic calculations for indoor temperature observations.

No causal heat-loss inference or automatic equipment control.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from math import isfinite
from typing import Iterable


def calculate_trend(samples: Iterable[tuple[datetime, float]]) -> float | None:
    """Observed °C/h across at least 30 minutes of readings."""
    samples = list(samples)
    if len(samples) < 2:
        return None
    latest_time, latest_temp = samples[-1]
    for timestamp, temperature in samples:
        elapsed = (latest_time - timestamp).total_seconds() / 3600
        if elapsed >= 0.5:
            return round((latest_temp - temperature) / elapsed, 3)
    return None


def quality_label(samples: Iterable[tuple[datetime, float]]) -> str:
    """Label history coverage, not prediction accuracy."""
    samples = list(samples)
    if len(samples) < 2:
        return "Afventer målinger"
    span = (samples[-1][0] - samples[0][0]).total_seconds() / 3600
    if len(samples) >= 72 and span >= 12:
        return "God datadækning"
    if len(samples) >= 12 and span >= 2:
        return "Delvis datadækning"
    return "For lidt historik"


def restore_history(raw: object, now: datetime, hours: int = 72) -> list[tuple[datetime, float]]:
    """Validate stored readings, discard corrupt/out-of-window values."""
    if not isinstance(raw, list):
        return []
    cutoff = now - timedelta(hours=hours)
    result = []
    for item in raw[-(hours * 12 + 100):]:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            continue
        try:
            stamp = datetime.fromisoformat(item[0])
            value = float(item[1])
        except (TypeError, ValueError, OverflowError):
            continue
        if (
            stamp.tzinfo is not None
            and cutoff <= stamp <= now
            and isfinite(value)
            and 5 <= value <= 40
        ):
            result.append((stamp.astimezone(timezone.utc), value))
    result.sort(key=lambda sample: sample[0])
    return result[-hours * 12:]
