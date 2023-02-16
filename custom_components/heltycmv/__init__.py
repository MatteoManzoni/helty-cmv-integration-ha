"""The Helty CMV integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .cmv import HeltyCMV

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.CLIMATE, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Helty CMV from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = HeltyCMV(entry.data["host"], entry.data["port"])

    cmv_name = await hass.data[DOMAIN][entry.entry_id].get_cmv_name()

    if cmv_name is None:
        return False

    hass.data[DOMAIN][entry.entry_id].name = cmv_name

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok