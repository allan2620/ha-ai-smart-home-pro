"""Read-only advisor with locally persisted temperature observations."""
from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta, timezone
import logging
from math import isfinite

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_INDOOR, CONF_OUTDOOR, CONF_PRICE, CONF_POWER,
    CONF_TARGET, DEFAULT_TARGET, DOMAIN, SCAN_INTERVAL_SECONDS,
)
from .thermal import calculate_trend, quality_label, restore_history

_LOGGER = logging.getLogger(__name__)
HISTORY_HOURS = 72


def numeric_state(hass: HomeAssistant, entity_id: str | None) -> float | None:
    """Read valid numeric sensor values, never replace unavailable with zero."""
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


def calculate_advice(indoor: float | None, outdoor: float | None, target: float):
    """Return a conservative suggested target and a diagnostic message."""
    if indoor is None or outdoor is None:
        return None, "Afventer gyldige temperaturmålinger"
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
    return round(target + adjustment, 1), message


class SmartHomeCoordinator(DataUpdateCoordinator[dict]):
    """Collect observations and publish informational-only diagnostics."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name="AI Smart Home PRO",
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.entry = entry
        self._indoor_history = deque(maxlen=HISTORY_HOURS * 12)
        self._store = Store(hass, 1, f"{DOMAIN}_{entry.entry_id}_history")

    async def async_load_history(self) -> None:
        """Restore previous valid observations before initial refresh."""
        data = await self._store.async_load()
        now = datetime.now(timezone.utc)
        history = restore_history(data.get("samples") if isinstance(data, dict) else None, now)
        self._indoor_history.extend(history)

    def _schedule_history_save(self) -> None:
        """Coalesce disk writes via Home Assistant's storage helper."""
        self._store.async_delay_save(
            lambda: {"samples": [[stamp.isoformat(), temp] for stamp, temp in self._indoor_history]},
            600,
        )

    async def _async_update_data(self) -> dict:
        """Refresh using only existing entity states."""
        cfg = self.entry.data
        indoor = numeric_state(self.hass, cfg[CONF_INDOOR])
        outdoor = numeric_state(self.hass, cfg[CONF_OUTDOOR])
        price = numeric_state(self.hass, cfg.get(CONF_PRICE))
        power = numeric_state(self.hass, cfg.get(CONF_POWER))
        target = float(cfg.get(CONF_TARGET, DEFAULT_TARGET))
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=HISTORY_HOURS)
        while self._indoor_history and self._indoor_history[0][0] < cutoff:
            self._indoor_history.popleft()
        if indoor is not None and 5 <= indoor <= 40:
            # Skip duplicate timestamps within a minute (e.g. manual refresh).
            if not self._indoor_history or (now - self._indoor_history[-1][0]).total_seconds() >= 60:
                self._indoor_history.append((now, indoor))
                self._schedule_history_save()

        recommended, advice = calculate_advice(indoor, outdoor, target)
        return {
            "indoor": indoor, "outdoor": outdoor, "price": price,
            "power": power, "target": target, "recommended": recommended,
            "advice": advice,
            "trend": calculate_trend(self._indoor_history),
            "sample_count": len(self._indoor_history),
            "data_quality": quality_label(self._indoor_history),
        }
