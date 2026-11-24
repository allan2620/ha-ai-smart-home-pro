"""Small transparent trend estimator based on actual indoor observations.

This is diagnostic only: it does not claim to estimate house heat loss,
future temperatures, or energy consumption.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable


def calculate_trend(samples: Iterable[tuple[datetime, float]]) -> float | None:
    """Estimate observed °C/h from samples >= 30 min apart (up to 24h).

    Requiring an observation window avoids displaying misleading rates from
    sensor noise during a five-minute update.
    """
    samples = list(samples)
    if len(samples) < 2:
        return None
    latest_time, latest_temp = samples[-1]
    for timestamp, temperature in samples:
        elapsed = (latest_time - timestamp).total_seconds() / 3600
        if elapsed >= 0.5:
            return round((latest_temp - temperature) / elapsed, 3)
    return None
