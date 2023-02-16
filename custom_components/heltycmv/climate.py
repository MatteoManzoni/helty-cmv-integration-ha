from __future__ import annotations
from datetime import timedelta
import async_timeout
import logging

from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import DeviceInfo
from .const import (
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_HIGHEST,
    PRESET_BOOST,
    PRESET_NIGHT,
    PRESET_COOLING,
    PRESET_MANUAL,
    FAN_AUTO,
    DOMAIN
)
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_FAN_ONLY,
    SUPPORT_FAN_MODE,
    SUPPORT_PRESET_MODE
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    cmv = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([HeltyCMV(cmv)], True)


class HeltyCMV(ClimateEntity):
    _attr_fan_modes = [
        FAN_LOW,
        FAN_MEDIUM,
        FAN_HIGH,
        FAN_HIGHEST
    ]
    _attr_hvac_modes = [HVAC_MODE_FAN_ONLY]
    _attr_preset_modes = [
        PRESET_BOOST,
        PRESET_NIGHT,
        PRESET_COOLING,
        PRESET_MANUAL
        ]
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_supported_features = SUPPORT_PRESET_MODE | SUPPORT_FAN_MODE

    _attr_has_entity_name = False

    def __init__(self, cmv):
        self._cmv = cmv
        self._attr_fan_mode = None
        self._attr_preset_mode = None
        self._attr_unique_id = f"{self._cmv.cmv_id}_cmv_control"
        self._attr_name = f"{self._cmv.name} CMV Control"

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

    @property
    def hvac_mode(self) -> str:
        return HVAC_MODE_FAN_ONLY

    @property
    def preset_mode(self) -> str | None:
        return self._attr_preset_mode

    @property
    def fan_mode(self) -> str | None:
        return self._attr_fan_mode

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        if fan_mode == "":
            self._attr_fan_mode = FAN_AUTO
            return None
        if not await self._cmv.set_cmv_mode(fan_mode):
            raise Exception("Cannot set {} fan mode".format(fan_mode))

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if not await self._cmv.set_cmv_mode(preset_mode):
            raise Exception("Cannot set {} preset mode".format(preset_mode))

    async def async_update(self) -> None:
        cmv_state = await self._cmv.get_cmv_op_status()
        if cmv_state:
            self._attr_fan_mode = cmv_state.get("fan_mode", None)
            self._attr_preset_mode = cmv_state.get("preset", None)
