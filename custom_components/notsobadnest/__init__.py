"""The Detailed Not So Bad Nest integration."""
from __future__ import annotations

import asyncio
import async_timeout
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .api import NestAPI

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[str] = ["binary_sensor", "sensor"]


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Not So Bad Nest component."""
    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Not So Bad Nest from a config entry."""
    try:
        hass.data[DOMAIN][entry.entry_id] = NestAPI(
            hass, entry.data["refresh_token"], entry.data["nest_field_test"]
        )
    except KeyError:
        hass.data[DOMAIN][entry.entry_id] = NestAPI(hass, entry.data["refresh_token"])

    await hass.data[DOMAIN][entry.entry_id].setup()

    async def async_update_data():
        with async_timeout.timeout(12):
            return await hass.data[DOMAIN][entry.entry_id].update()

    hass.coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="protectsensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=5),
    )

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True

    # async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    # unload_ok = all(
    #    await asyncio.gather(
    #        *[
    #            hass.config_entries.async_forward_entry_unload(
    #                entry, component)
    #            for component in PLATFORMS
    #        ]
    #    )
    # )
    # if unload_ok:
    #    hass.data[DOMAIN].pop(entry.entry_id)

    # return unload_ok
