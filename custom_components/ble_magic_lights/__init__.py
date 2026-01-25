"""BLE Magic Lights integration for Home Assistant."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .ble_device import BleMagicLightDevice

PLATFORMS = ["light"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up BLE Magic Lights from a config entry."""

    # Ensure friendly name shows in Integrations page
    if not entry.title:
        entry.title = "BLE Magic Lights"

    # Store device instance in hass.data
    hass.data.setdefault("ble_magic_lights", {})
    hass.data["ble_magic_lights"][entry.entry_id] = BleMagicLightDevice(
        entry.data["address"]
    )

    # Forward setup to light platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload BLE Magic Lights config entry."""

    # Remove device instance
    hass.data.get("ble_magic_lights", {}).pop(entry.entry_id, None)

    # Unload platform
    return await hass.config_entries.async_forward_entry_unload(entry, PLATFORMS)
