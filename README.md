# AI Smart Home PRO

Private, locally running custom integration for Home Assistant. **Version 0.2.0** is an early, advisory-only prototype.

## Features

- UI setup for indoor and outdoor temperature sensors, optionally electricity price and heat pump power, and a target room temperature.
- Temperature recommendation limited to ±0.5 °C around the configured target (informational only).
- Observed indoor temperature trend in °C/hour, calculated from at least 30 minutes of readings; the first trend appears after sufficient observation.
- Current sample count and basic diagnostic sensor values.
- No device writes, external APIs, trained AI, forecast, automatic heating curve or persistent learning yet.

## Installation

### Manual (supported during development)
Download this repository as a ZIP from GitHub. Copy `custom_components/ai_smart_home_pro` to `/config/custom_components/ai_smart_home_pro` on your Home Assistant instance. Restart Home Assistant, then select **Settings → Devices & services → Add integration → AI Smart Home PRO**.

### HACS (experimental)
If you have HACS, add this private repository as a **Custom repository** with category **Integration** (access to private repositories depends on your GitHub/HACS authorization). Then install and restart. If HACS cannot access the private repository, use the manual approach.

## Suggested initial sensor choices

Indoor: `sensor.boiler_room_nilan_user_panel_temperature_t15` (only if representative of your actual living space). For outdoor temperature, use an actual temperature sensor exposed by your heat pump, e.g. `sensor.vvm_320_e_aktuel_udetemperatur_bt1_40004` when available. Optional price: `sensor.energi_data_service`.

## Important limitations

- All values are advisory; no changes to equipment.
- Trend uses RAM samples and resets on Home Assistant restart. It is **not** yet a persistent learned thermal model.
- No price optimization yet. Price and power sensors are displayed as-is, with units left unconverted; check the original sensors.
- Sensor accuracy and representativeness are crucial. Verify readings before using recommendations for decisions.
- Never commit secrets or credentials to this repository.

## Local tests

Run `python -m compileall -q custom_components` and `python -m unittest discover -s tests -v` from repository root. GitHub Actions runs those checks on push.

## Roadmap

Persistent historical learning, confidence scores, 24/48h forecasts, DK1/N1 price optimization, read-only integration adapters for Nilan / IVT, EV and irrigation, and only then separately approved safe control modes.
