"""Diagnostic and recommendation sensors for AI Smart Home PRO."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SmartHomeCoordinator


DESCRIPTIONS = (
    SensorEntityDescription(key="indoor", name="Indetemperatur", native_unit_of_measurement="°C", icon="mdi:home-thermometer"),
    SensorEntityDescription(key="outdoor", name="Udetemperatur", native_unit_of_measurement="°C", icon="mdi:thermometer"),
    SensorEntityDescription(key="price", name="Elpris (kildens enhed)", icon="mdi:currency-eur"),
    SensorEntityDescription(key="power", name="Varmepumpeeffekt (kildens enhed)", icon="mdi:flash"),
    SensorEntityDescription(key="target", name="Ønsket temperatur", native_unit_of_measurement="°C", icon="mdi:thermometer-check"),
    SensorEntityDescription(key="recommended", name="Rådgivende temperatur", native_unit_of_measurement="°C", icon="mdi:lightbulb-thermometer"),
    SensorEntityDescription(key="advice", name="Varmeråd", icon="mdi:comment-text-outline"),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: SmartHomeCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AISmartHomeSensor(coordinator, entry, desc) for desc in DESCRIPTIONS])


class AISmartHomeSensor(CoordinatorEntity[SmartHomeCoordinator], SensorEntity):
    """Present local calculation results without device control."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: SmartHomeCoordinator,
        entry: ConfigEntry, description: SensorEntityDescription
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="AI Smart Home PRO",
            manufacturer="Local custom integration",
            model="Advisory baseline",
        )

    @property
    def native_value(self):
        """Return None for missing measurement, not a fabricated value."""
        return self.coordinator.data.get(self.entity_description.key)
