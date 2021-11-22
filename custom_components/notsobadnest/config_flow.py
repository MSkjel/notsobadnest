"""Config flow for Not So Bad Nest integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from voluptuous.validators import Boolean

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .api import NestAPI

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Optional("refresh_token"): str,
        vol.Optional("issue_token"): str,
        vol.Optional("cookie"): str,
        vol.Optional("nest_field_test", default=False): bool,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    refresh_token = data["refresh_token"] if "refresh_token" in data else None
    nest_field_test = data["nest_field_test"] if "nest_field_test" in data else None
    issue_token = data["issue_token"] if "issue_token" in data else None
    cookie = data["cookie"] if "cookie" in data else None

    if refresh_token is not None and len(refresh_token) > 0:
        if len(refresh_token) > 65 and refresh_token.startswith("1//"):
            return await NestAPI(
                hass, refresh_token=refresh_token, nest_field_test=nest_field_test
            ).setup()
        else:
            raise InvalidToken
    elif (
        issue_token is not None
        and cookie is not None
        and len(issue_token) > 0
        and len(cookie) > 0
    ):
        return await NestAPI(hass, issue_token=issue_token, cookie=cookie).setup()
    else:
        raise InvalidCookie


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
            except InvalidToken:
                _LOGGER.exception("Invalid refresh_token")
                errors["base"] = "invalid_token"
            except InvalidCookie:
                _LOGGER.exception("Invalid Cookie and or Issue Token")
                errors["base"] = "invalid_cookie"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class InvalidToken(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid token."""


class InvalidCookie(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid token."""
