"""Read-only advisory model.

This is a transparent rule-based baseline, not a trained AI model.
Never calls services or writes device values.
"""
from __future__ import annotations

from datetime import timedelta, datetime, timezone
from collections import deque

from .thermal import calculate_trend
from math import isfinite

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_INDOOR,
    CONF_OUTDOOR,
    CONF_PRICE,
    CONF_POWER,
    CONF_TARGET,
    DEFAULT_TARGET,
    SCAN_INTERVAL_SECONDS,
)


def numeric_state(hass: HomeAssistant, entity_id: str | None) -> float | None:
    """Read valid, finite numeric sensor state; do not silently substitute zero."""
    if not entity_id:
        return None
    state = hass.states.get(entity_id)
    if state is None or state.state in ("unknown", "unavailable", "none"):
        return None
    try:
        value = float(state.state)
        return value if isfinite(value) else None
    except (ValueError, TypeError):
        return None


def calculate_advice(
    indoor: float | None, outdoor: float | None, target: float
) -> tuple[float | None, str]:
    """Return suggested setpoint and text, without controlling equipment."""
    if indoor is None or outdoor is None:
        return None, "Afventer gyldige temperaturmålinger"
    # Fixed cap avoids aggressive recommendations before system calibration.
    difference = target - indoor
    if difference > 0.5:
        adjustment = min(0.5, difference / 2)
        message = "Indetemperaturen er under målet; undersøg varmebehovet"
    elif difference < -0.5:
        adjustment = max(-0.5, difference / 2)
        message = "Indetemperaturen er over målet; undersøg overopvarmning"
    else:
        adjustment = 0.0
        message = "Indetemperaturen ligger tæt på målet"
    # Outdoor temperature is displayed but does not yet calibrate the advice.
    return round(target + adjustment, 1), message


class SmartHomeCoordinator(DataUpdateCoordinator[dict]):
    """Aggregate configured entities for informational sensors."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name="AI Smart Home PRO",
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.entry = entry
        self._indoor_history = deque(maxlen=288)

    async def _async_update_data(self) -> dict:
        """Compute advisory data without network calls or device writes."""
        cfg = self.entry.data
        indoor = numeric_state(self.hass, cfg[CONF_INDOOR])
        outdoor = numeric_state(self.hass, cfg[CONF_OUTDOOR])
        price = numeric_state(self.hass, cfg.get(CONF_PRICE))
        power = numeric_state(self.hass, cfg.get(CONF_POWER))
        target = float(cfg.get(CONF_TARGET, DEFAULT_TARGET))
        if indoor is not None and 5 <= indoor <= 40:
            self._indoor_history.append((datetime.now(timezone.utc), indoor))
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        while self._indoor_history and self._indoor_history[0][0] < cutoff:
            self._indoor_history.popleft()
        trend = calculate_trend(self._indoor_history)
        recommended, advice = calculate_advice(indoor, outdoor, target)
        return {
            "indoor": indoor,
            "outdoor": outdoor,
            "price": price,
            "power": power,
            "target": target,
            "recommended": recommended,
            "advice": advice,
            "trend": trend,
            "sample_count": len(self._indoor_history),
        }
