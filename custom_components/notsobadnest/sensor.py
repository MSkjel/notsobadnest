from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensor for passed config_entry in HA."""
    api = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = hass.coordinator

    new_devices = []
    for sn, protect in api.protects.items():
        new_devices.append(NestIPSensor(coordinator, protect, api))
        new_devices.append(NestSerialNumberSensor(coordinator, protect, api))
        new_devices.append(NestReplaceBySensor(coordinator, protect, api))
        new_devices.append(NestACBatterySensor(coordinator, protect, api))
        new_devices.append(NestBatteryLevelSensor(coordinator, protect, api))
        new_devices.append(NestSteamDetectionSensor(coordinator, protect, api))

    if new_devices:
        async_add_entities(new_devices)


class NestProtectSensorBase(CoordinatorEntity, SensorEntity):
    """Representation of a dummy Cover."""

    def __init__(self, coordinator, protect, api) -> None:
        """Initialize the sensor."""
        self._protect = protect
        self._api = api
        super().__init__(coordinator)

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._protect.serial)},
            "name": self._protect.name,
            "sw_version": self._protect.software_version,
            "model": self._protect.model,
            "manufacturer": "Google Nest",
        }

    @property
    def available(self) -> bool:
        """Return True if protect is available."""
        return self._api.available


class NestIPSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_ip_address"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._protect.ip

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} IP Address"

    @property
    def entity_category(self):
        """Icon of the entity."""
        return "diagnostic"


class NestSerialNumberSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_serial_number"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._protect.serial

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Serial Number"

    @property
    def entity_category(self):
        """Icon of the entity."""
        return "diagnostic"


class NestReplaceBySensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_replace_by"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._protect.replace_by

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Replace By"

    @property
    def entity_category(self):
        """Icon of the entity."""
        return "diagnostic"


class NestACBatterySensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_ac_battery"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return "AC" if self._protect.ac_power else "Battery"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Power Type"

    @property
    def icon(self):
        """Icon of the entity."""
        return "mdi:power"

    @property
    def entity_category(self):
        """Icon of the entity."""
        return "diagnostic"


class NestBatteryLevelSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_battery_level"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._protect.battery_level

    @property
    def native_unit_of_measurement(self):
        """Return the state of the sensor."""
        return "%"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Battery Level"

    @property
    def device_class(self):
        """Icon of the entity."""
        return "battery"

    @property
    def entity_category(self):
        """Icon of the entity."""
        return "diagnostic"


class NestSteamDetectionSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_steam_detect"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._protect.steam_detection

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Steam Detection"

    @property
    def entity_category(self):
        """Icon of the entity."""
        return "diagnostic"
