from homeassistant.helpers.discovery import async_load_platform
import logging

DOMAIN = "ble_magic_lights"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the BLE Magic Lights integration."""
    lights = config.get(DOMAIN, [])
    for lamp_conf in lights:
        name = lamp_conf.get("name")
        address = lamp_conf.get("address")
        hass.async_create_task(
            async_load_platform(
                hass,
                "light",
                DOMAIN,
                {"name": name, "address": address},
                config,
            )
        )
    return True
