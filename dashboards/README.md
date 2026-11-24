# AI Smart Home PRO – dashboard i sidepanelet

Dette dashboard er lavet med **indbyggede Home Assistant-kort**, uden ekstra HACS-kort eller plugins. Det viser live temperaturer, anbefalinger, datadækning, elpris og historik.

## Installation i sidepanelet (UI, anbefalet)

1. Sørg for at AI Smart Home PRO v0.4.0 er installeret via HACS, og at integrationen er tilføjet under **Indstillinger → Enheder og tjenester**.
2. Gå til **Indstillinger → Dashboards → Tilføj dashboard**. Opret et **nyt tomt dashboard**, f.eks. `AI Smart Home PRO`, og vælg **Vis i sidepanel**. Hvis din HA-version viser andre knapper, brug den tilsvarende blanke dashboardmulighed.
3. Åbn dashboardet, gå til **Rediger dashboard → menuen med tre prikker → Raw configuration editor / Rå konfigurationseditor**.
4. Erstat dashboardets rå konfiguration med indholdet af [ai-smart-home-pro.yaml](./ai-smart-home-pro.yaml). Gem.
5. Kontrollér de faktiske entity-id'er i **Udviklerværktøjer → Tilstande**. Eksemplerne i YAML er automatisk afledt af de danske navne, og Home Assistant kan have tildelt et andet entity-id (f.eks. med suffix `_2`). Erstat ethvert entity-id, der står som `Entity not found`.

Bemærk: HACS opdaterer integrationskoden, **ikke** et separat dashboard oprettet i Home Assistants brugerflade. Når vi ændrer dashboardet i GitHub, skal YAML-koden kopieres ind i dashboardet igen. Automatiseret dashboarddistribution kan udvikles senere.

## Alternativ: YAML-dashboard

Hvis du administrerer dashboards via `configuration.yaml`, kan du kopiere dashboardfilen til `/config/dashboards/ai-smart-home-pro.yaml` og tilføje følgende under din eksisterende `lovelace:`-sektion. Opret **ikke** en ekstra `lovelace:`-nøgle, hvis du allerede har en.

```yaml
lovelace:
  dashboards:
    ai-smart-home-pro:
      mode: yaml
      title: AI Smart Home PRO
      icon: mdi:brain
      show_in_sidebar: true
      filename: dashboards/ai-smart-home-pro.yaml
```

Genindlæs dashboards eller genstart Home Assistant. Se Home Assistants officielle dokumentation om flere dashboards for din HA-version.

## Forventede entity-id'er

- `sensor.ai_smart_home_pro_indetemperatur`
- `sensor.ai_smart_home_pro_udetemperatur`
- `sensor.ai_smart_home_pro_onsket_temperatur`
- `sensor.ai_smart_home_pro_radgivende_temperatur`
- `sensor.ai_smart_home_pro_temperaturtrend`
- `sensor.ai_smart_home_pro_temperaturstatus`
- `sensor.ai_smart_home_pro_varmerad`
- `sensor.ai_smart_home_pro_datadaekning`

**Vigtigt:** Dette er forventede, ikke verificerede, entity-id'er. Kontroller dem lokalt.

Dashboardet er **kun til overvågning**. Det tilbyder ikke automatisk temperaturændring eller styring af IVT/Nilan.
