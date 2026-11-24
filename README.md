# AI Smart Home PRO

A private Home Assistant custom integration for **advisory-first** energy and heating optimization.

## First release

- Config flow: choose indoor temperature, outdoor temperature, electricity price, and optional heat-pump power sensors.
- Read-only diagnostics: indoor temperature, outdoor temperature, price, suggested heating setpoint, estimated heating trend, and current operating advice.
- Local deterministic calculations, no cloud dependency or API keys.
- Safe default: **never writes to heating, ventilation or charging devices**.

## Installation (development)

Copy `custom_components/ai_smart_home_pro` into your Home Assistant `/config/custom_components/` folder, restart Home Assistant, then use **Settings > Devices & services > Add integration > AI Smart Home PRO**.

The integration is under development. Readings and recommendations must be validated against real measurements before considering automatic equipment control. Never expose credentials or `secrets.yaml` in this repository.

## Roadmap

1. Advisory-only baseline and configurable sensors
2. Historical data and adaptive thermal model with confidence metrics
3. Forecast and DK1/N1 tariff-aware optimization
4. Optional Nilan, IVT, EV, and irrigation adapters, each with explicit safety limits and opt-in control
5. HACS packaging, tests and releases
