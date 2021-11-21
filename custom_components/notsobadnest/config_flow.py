"""Config flow for Not So Bad Nest integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .api import NestAPI

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({vol.Required("refresh_token"): str})


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:

    return await NestAPI(hass, data["refresh_token"]).setup()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for notsobadnest."""

    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                if await validate_input(self.hass, user_input):
                    return self.async_create_entry(
                        title="Not So Bad Nest", data=user_input
                    )
                else:
                    errors["base"] = "Bad Refresh Token"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
