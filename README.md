# AI Smart Home PRO

Private Home Assistant custom integration — development version **0.3.0**, advisory-only.

## New in 0.3.0

- Retains up to 72 hours of indoor temperature observations in Home Assistant local `.storage` (coalesced saves; most recent readings may not be saved before a sudden power loss).
- Restores valid observations on restart, filters corrupt, stale and implausible records.
- Adds a **Datadækning** sensor indicating whether enough historical observations are available.
- Displays observed indoor temperature trend in °C/hour after 30 minutes of data.
- Existing advisory setpoint never controls hardware and remains limited to ±0.5 °C relative to target.

**Not yet a trained AI model:** datadækning reflects history coverage only, not forecast accuracy; the observed temperature slope is not a causal estimate of thermal loss. No weather forecast, tariff optimization, writing to IVT/Nilan or automatic curve changes yet.

## Manual installation/update

The repository is private; standard HACS installation may report GitHub Not Found. Use **Code → Download ZIP** on GitHub while signed in, extract and copy `custom_components/ai_smart_home_pro` to `/config/custom_components/ai_smart_home_pro` (overwriting the older integration), then restart Home Assistant. Add the integration in **Settings → Devices & services** if not already added.

Configure existing sensors. Indoor suggestion: `sensor.boiler_room_nilan_user_panel_temperature_t15` provided it reflects the room to be heated. Optional price: `sensor.energi_data_service`; check units on original entities.

No credentials or `secrets.yaml` belong in this repository.

## Tests

`python -m compileall -q custom_components`

`python -m unittest discover -s tests -v`

GitHub Actions runs both on every push. Real-world Home Assistant compatibility must still be confirmed on the user's own installation.

## Next steps

Longer-term per-zone diagnostics, sensor quality flags, weather and tariffs, validated thermal modeling, and later opt-in control with explicit safeguards.
