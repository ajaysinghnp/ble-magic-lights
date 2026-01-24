"""BLE Magic Lights - Light platform for Home Assistant."""

from homeassistant.components.light import (
    LightEntity,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_EFFECT,
    COLOR_MODE_ONOFF,
    COLOR_MODE_BRIGHTNESS,
    COLOR_MODE_HS,
)
from .ble_device import BleMagicLightDevice

PLATFORMS = ["light"]


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up BLE Magic Light from a config entry."""
    device = BleMagicLightDevice(entry.data["address"])
    async_add_entities([BLEMagicLight(entry.title, device)])


class BLEMagicLight(LightEntity):
    """Representation of a BLE Magic Light."""

    _attr_supported_color_modes = {
        COLOR_MODE_ONOFF,
        COLOR_MODE_BRIGHTNESS,
        COLOR_MODE_HS,
    }
    _attr_color_mode = COLOR_MODE_ONOFF
    _attr_supported_features = SUPPORT_BRIGHTNESS | SUPPORT_COLOR | SUPPORT_EFFECT

    def __init__(self, name, device: BleMagicLightDevice):
        self._attr_name = name
        self._device = device
        self._is_on = False
        self._brightness = 255
        self._hs_color = (0, 0)
        self._effect = None
        self._available_effects = list(device.commands.keys())  # all decoded commands

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def hs_color(self):
        return self._hs_color

    @property
    def effect(self):
        return self._effect

    @property
    def effect_list(self):
        return self._available_effects

    async def async_turn_on(self, **kwargs):
        """Turn on the light with optional parameters."""
        # Handle brightness / color / effect
        effect = kwargs.get("effect")
        brightness = kwargs.get("brightness")
        hs_color = kwargs.get("hs_color")

        if effect:
            payload = self._device.commands.get(effect)
            if payload:
                await self._device.send(effect)
                self._effect = effect
        elif hs_color:
            self._hs_color = hs_color
            # Map HS to closest static color payload
            # Example: only use static_red / static_green / static_blue as demo
            h, s = hs_color
            if h < 60:
                await self._device.send("static_red")
            elif h < 180:
                await self._device.send("static_green")
            else:
                await self._device.send("static_blue")
            self._effect = None
        else:
            # Default turn on
            await self._device.send("turn_on")
            self._effect = None

        if brightness:
            self._brightness = brightness  # Optional: can scale payloads if desired

        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the light."""
        await self._device.send("turn_off")
        self._is_on = False
        self._effect = None
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        """Disconnect BLE when entity is removed."""
        await self._device.disconnect()
