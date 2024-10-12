from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_MAC
from homeassistant.helpers.typing import ConfigType

from .NeewerLight import NeewerLight

DOMAIN = "neewerlight"
PLATFORMS = ["light"]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Neewer Light component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Neewer Light from a config entry."""
    instance = NeewerLight(entry.data[CONF_MAC])
    hass.data[DOMAIN][entry.entry_id] = instance
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        instance = hass.data[DOMAIN].pop(entry.entry_id)
        await instance.disconnect()
    return unload_ok
