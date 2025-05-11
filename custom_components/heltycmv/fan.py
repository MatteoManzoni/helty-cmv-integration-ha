from __future__ import annotations
from typing import Any
import logging

from homeassistant.helpers.entity import DeviceInfo
from .const import (
    PRESET_BOOST,
    PRESET_NIGHT,
    PRESET_COOLING,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_HIGHEST,
    FAN_OFF,
    DOMAIN
)
from homeassistant.components.fan import FanEntity, FanEntityFeature


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    cmv = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([HeltyCMV(cmv)], True)


class HeltyCMV(FanEntity):
    _attr_preset_modes = [
        PRESET_BOOST,
        PRESET_NIGHT,
        PRESET_COOLING
        ]
    _attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE | FanEntityFeature.TURN_ON | FanEntityFeature.TURN_OFF
    _attr_speed_count = 4

    _attr_has_entity_name = False

    def __init__(self, cmv):
        self._cmv = cmv
        self._attr_percentage = None
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
    def preset_mode(self) -> str | None:
        return self._attr_preset_mode

    async def async_set_percentage(self, percentage: int) -> None:
        if not await self._cmv.set_cmv_mode(percentage):
            raise Exception("Cannot set {} fan percentage".format(percentage))

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if not await self._cmv.set_cmv_mode(preset_mode):
            raise Exception("Cannot set {} preset mode".format(preset_mode))

    async def async_turn_off(self, **kwargs: Any) -> None:
        if not await self._cmv.set_cmv_mode(FAN_OFF):
            raise Exception("Cannot set {} fan percentage to turn off fan".format(0))

    async def async_turn_on(self, **kwargs: Any) -> None:
        if not await self._cmv.set_cmv_mode(FAN_LOW):
            raise Exception("Cannot set {} fan percentage to turn off fan".format(0))

    async def async_update(self) -> None:
        cmv_state = await self._cmv.get_cmv_op_status()
        if cmv_state:
            self._attr_percentage = cmv_state.get("fan_mode", None)
            self._attr_preset_mode = cmv_state.get("preset", None)
        else:
            self._attr_percentage = None
            self._attr_preset_mode = None
