"""BLE Magic Lights - Light platform for Home Assistant."""

from homeassistant.components.light import (
    LightEntity,
    ColorMode,
    LightEntityFeature,
)
from .ble_device import BleMagicLightDevice

PLATFORMS = ["light"]


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up BLE Magic Light from a config entry."""
    device = BleMagicLightDevice(entry.data["address"])
    async_add_entities([BLEMagicLight(entry.title, device)], update_before_add=False)


class BLEMagicLight(LightEntity):
    """Representation of a BLE Magic Light."""

    _attr_supported_color_modes = {
        ColorMode.ONOFF,
        ColorMode.BRIGHTNESS,
        ColorMode.HS,
    }

    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_features = LightEntityFeature.EFFECT

    def __init__(self, name, device: BleMagicLightDevice):
        self._attr_name = name
        self._attr_unique_id = device.address
        self._device = device
        self._is_on = False
        self._brightness = 255
        self._hs_color = (0, 0)
        self._effect = None
        # Expose available commands/effects from the device commands dict
        self._available_effects = list(device.commands.keys())

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

    async def _ensure_connected(self):
        """Ensure BLE client is connected before sending commands."""
        if self._device.client is None or not getattr(
            self._device.client, "is_connected", False
        ):
            await self._device.connect()

    async def async_turn_on(self, **kwargs):
        """Turn on the light with optional parameters.

        Supports `effect`, `brightness`, and `hs_color` (mapped to static colors).
        """
        effect = kwargs.get("effect")
        brightness = kwargs.get("brightness")
        hs_color = kwargs.get("hs_color")

        await self._ensure_connected()

        if effect:
            if effect in self._device.commands:
                await self._device.send(effect)
                self._effect = effect
            else:
                raise ValueError(f"Unknown effect: {effect}")
        elif hs_color:
            self._hs_color = hs_color
            h, s = hs_color
            if h < 60:
                await self._device.send("static_red")
            elif h < 180:
                await self._device.send("static_green")
            else:
                await self._device.send("static_blue")
            self._effect = None
        else:
            await self._device.send("turn_on")
            self._effect = None

        if brightness is not None:
            self._brightness = brightness

        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the light."""
        await self._ensure_connected()
        await self._device.send("turn_off")
        self._is_on = False
        self._effect = None
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        """Disconnect BLE when entity is removed."""
        await self._device.disconnect()
