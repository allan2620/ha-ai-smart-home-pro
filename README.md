# AI Smart Home PRO

Public Home Assistant custom integration — experimental **v0.4.0**, entirely advisory.

## Dashboard i sidepanelet

Et nyt dansk overvågningsdashboard findes i [dashboards/ai-smart-home-pro.yaml](dashboards/ai-smart-home-pro.yaml). Se [installationsvejledningen](dashboards/README.md). Dashboardet er separat fra integrationen og skal oprettes én gang under Home Assistants Dashboards; HACS installerer ikke automatisk dashboardet.

## v0.4.0 — Indoor/outdoor observation

- Retains up to 72 hours of local indoor temperature observations (introduced in v0.3).
- Now also retains paired indoor and outdoor temperatures when both readings are valid.
- New sensors: **Sammenhørende temperaturmålinger**, **Gennemsnitlig temperaturforskel 24t** (requires at least 12 pairs over >=2 hours), and **Temperaturstatus**.
- All readings are diagnostic only. The indoor–outdoor gap is NOT a measured U-value or calibrated heat-loss coefficient, and temperature changes can reflect sun, occupants, ventilation, and heating.
- Existing conservative recommendation remains informational and capped at ±0.5°C from configured target.
- Local history uses Home Assistant storage, with writes coalesced roughly every 10 minutes. Data are not retained beyond 72 hours.

## Install and update through HACS

This repository is public. Open **HACS → menu → Custom repositories**, add `https://github.com/allan2620/ha-ai-smart-home-pro` as **Integration**, then download AI Smart Home PRO. Restart Home Assistant. Future updates will depend on HACS release/version detection; if HACS does not detect v0.4.0 immediately, use the repository **Redownload** action and restart.

If already installed manually, ensure there is only one `/config/custom_components/ai_smart_home_pro` folder.

## Configuration

In **Settings → Devices & services → Add integration**, select indoor/outdoor temperature sensors; optionally price and heat-pump power sensors and desired room temperature. Example indoor: `sensor.boiler_room_nilan_user_panel_temperature_t15` only if it represents occupied living space. Optional price: `sensor.energi_data_service`. Verify units on original sources.

## Limitations

**Not a trained AI model yet.** Data coverage is not model certainty. No cloud API, no forecast, no automated IVT/Nilan control, no heating-curve changes and no price-based optimization. No secrets or local configuration files should be committed.

## Tests

`python -m compileall -q custom_components`

`python -m unittest discover -s tests -v`

GitHub Actions runs syntax and isolated computation tests. Real Home Assistant runtime compatibility needs installation testing.
