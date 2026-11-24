"""Config flow for selecting existing Home Assistant entities."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_INDOOR,
    CONF_OUTDOOR,
    CONF_PRICE,
    CONF_POWER,
    CONF_TARGET,
    DEFAULT_TARGET,
    DOMAIN,
)


class AISmartHomeFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Set up monitoring through the user interface."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Select temperature sensors and optionally electricity data."""
        if user_input is not None:
            await self.async_set_unique_id("home")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="AI Smart Home PRO", data=user_input)

        temperature = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor", device_class="temperature")
        )
        numeric_sensor = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        )
        schema = vol.Schema(
            {
                vol.Required(CONF_INDOOR): temperature,
                vol.Required(CONF_OUTDOOR): temperature,
                vol.Optional(CONF_PRICE): numeric_sensor,
                vol.Optional(CONF_POWER): numeric_sensor,
                vol.Required(CONF_TARGET, default=DEFAULT_TARGET): vol.All(
                    vol.Coerce(float), vol.Range(min=16, max=26)
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)
