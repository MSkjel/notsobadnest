from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensor for passed config_entry in HA."""
    api = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = hass.coordinator

    new_devices = []
    for sn, protect in api.protects.items():
        new_devices.append(NestSmokeAlarmSensor(coordinator, protect, api))
        new_devices.append(NestSmokeWarningSensor(coordinator, protect, api))
        new_devices.append(NestCOAlarmSensor(coordinator, protect, api))
        new_devices.append(NestCOWarningSensor(coordinator, protect, api))
        new_devices.append(NestHeatAlarmSensor(coordinator, protect, api))
        new_devices.append(NestHeatWarningSensor(coordinator, protect, api))
        new_devices.append(NestManualTestSensor(coordinator, protect, api))
        if protect.ac_power:
            new_devices.append(NestMotionSensor(coordinator, protect, api))

    if new_devices:
        async_add_entities(new_devices)


class NestProtectSensorBase(CoordinatorEntity, BinarySensorEntity):
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


class NestSmokeAlarmSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_smoke_alarm"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._protect.smoke_detected

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Smoke Alarm"

    @property
    def device_class(self):
        """Icon of the entity."""
        return "smoke"


class NestSmokeWarningSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_smoke_warning"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._protect.smoke_warning

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Smoke Warning"

    @property
    def device_class(self):
        """Icon of the entity."""
        return "smoke"


class NestCOAlarmSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_co_alarm"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._protect.co_detected

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} CO Alarm"

    @property
    def device_class(self):
        """Icon of the entity."""
        return "gas"


class NestCOWarningSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_co_warning"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._protect.co_warning

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} CO Warning"

    @property
    def device_class(self):
        """Icon of the entity."""
        return "gas"


class NestHeatAlarmSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_heat_alarm"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._protect.heat_detected

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Heat Alarm"


class NestHeatWarningSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_heat_warning"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._protect.heat_warning

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Heat Warning"


class NestManualTestSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_manual_test"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._protect.manual_test_active

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Manual Test"


class NestMotionSensor(NestProtectSensorBase):
    """Representation of a Sensor."""

    def __init__(self, coordinator, protect, api):
        """Initialize the sensor."""
        super().__init__(coordinator, protect, api)

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._protect.serial}_motion"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._protect.motion_detected

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._protect.name} Motion"

    @property
    def device_class(self):
        """Icon of the entity."""
        return "motion"
