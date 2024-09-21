from __future__ import annotations
from typing import Any

import logging

from homeassistant.helpers.entity import DeviceInfo
from .const import (
    DOMAIN
)
from homeassistant.components.button import ButtonEntity


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    cmv = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([HeltyCMVResetFilter(cmv)], True)


class HeltyCMVResetFilter(ButtonEntity):

    def __init__(self, cmv):
        self._cmv = cmv
        self._attr_is_on = None
        self._attr_unique_id = f"{self._cmv.cmv_id}_filter_reset"
        self._attr_name = f"{self._cmv.name} CMV Filter Usage Reset"

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

    async def async_press(self) -> None:
        await self._cmv.reset_cmv_filters