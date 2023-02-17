"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import (
    DOMAIN
)

from homeassistant.const import (
    TEMPERATURE,
    TEMP_CELSIUS,
    DEVICE_CLASS_HUMIDITY,
    PERCENTAGE,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    cmv = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([CMVIndoorTemperature(cmv), CMVOutdoorTemperature(cmv), CMVIndoorHumidity(cmv)], True)


class CMVBaseSensor(SensorEntity):
    _attr_has_entity_name = False

    def __init__(self, cmv):
        self._cmv = cmv
        self._state = None

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._cmv.cmv_id)},
            name=self._cmv.name,
            manufacturer="Helty",
            model="Flow",
        )

    @property
    def available(self) -> bool:
        return self._cmv.online


class CMVIndoorTemperature(CMVBaseSensor):
    """Representation of a Sensor."""

    device_class = TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS

    def __init__(self, cmv):
        super().__init__(cmv)
        self._attr_unique_id = f"{self._cmv.cmv_id}_indoor_temp"
        self._attr_name = f"{self._cmv.name} Indoor Temperature"

    @property
    def native_value(self) -> float | None:
        return self._state

    async def async_update(self) -> None:
        self._state = await self._cmv.get_cmv_indoor_air_temperature()


class CMVOutdoorTemperature(CMVBaseSensor):
    """Representation of a Sensor."""

    device_class = TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS

    def __init__(self, cmv):
        super().__init__(cmv)
        self._attr_unique_id = f"{self._cmv.cmv_id}_outdoor_temp"
        self._attr_name = f"{self._cmv.name} Outdoor Temperature"

    @property
    def native_value(self) -> float | None:
        return self._state

    async def async_update(self) -> None:
        self._state = await self._cmv.get_cmv_outdoor_air_temperature()


class CMVIndoorHumidity(CMVBaseSensor):
    """Representation of a Sensor."""

    device_class = DEVICE_CLASS_HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, cmv):
        super().__init__(cmv)
        self._attr_unique_id = f"{self._cmv.cmv_id}_indoor_humidity"
        self._attr_name = f"{self._cmv.name} Indoor Humidity"

    @property
    def native_value(self) -> float | None:
        return self._state

    async def async_update(self) -> None:
        self._state = await self._cmv.get_cmv_indoor_humidity()
