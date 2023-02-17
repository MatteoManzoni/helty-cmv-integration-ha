from __future__ import annotations
from typing import Any

import logging

from homeassistant.helpers.entity import DeviceInfo
from .const import (
    DOMAIN
)
from homeassistant.components.switch import SwitchEntity


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    cmv = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([HeltyCMVLeds(cmv)], True)


class HeltyCMVLeds(SwitchEntity):

    def __init__(self, cmv):
        self._cmv = cmv
        self._attr_is_on = None
        self._attr_unique_id = f"{self._cmv.cmv_id}_panel_leds"
        self._attr_name = f"{self._cmv.name} CMV Panel Leds"

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

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._cmv.turn_cmv_leds_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._cmv.turn_cmv_leds_off()

    async def async_update(self) -> None:
        self._attr_is_on = await self._cmv.are_cmv_leds_on()
