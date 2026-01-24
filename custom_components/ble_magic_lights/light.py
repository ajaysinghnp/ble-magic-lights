from homeassistant.components.light import LightEntity, ColorMode
from .ble_device import BleMagicLightDevice


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up BLE Magic Light from a config entry."""
    device = BleMagicLightDevice(entry.data["address"])
    async_add_entities([BleMagicLight(entry.title, device)])


class BleMagicLight(LightEntity):
    """Representation of a BLE Magic Light."""

    _attr_supported_color_modes = {ColorMode.ONOFF}
    _attr_color_mode = ColorMode.ONOFF

    def __init__(self, name: str, device: BleMagicLightDevice):
        """Initialize the light."""
        self._attr_name = name
        self._device = device
        self._is_on = False

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        await self._device.send("turn_on")
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self._device.send("turn_off")
        self._is_on = False
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        """Disconnect when removing the entity."""
        await self._device.disconnect()
