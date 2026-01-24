"""BLE Magic Lights Light platform."""

from homeassistant.components.light import (
    LightEntity,
    SUPPORT_COLOR,
    SUPPORT_EFFECT,
)
from homeassistant.const import COLOR_MODE_BRIGHTNESS, COLOR_MODE_HS
from .ble_device import BleMagicLightDevice

# -------------------------------
# Effects mapping
# -------------------------------
EFFECTS = {
    "Seven Color Gradient": "seven_color_gradient",
    "Seven Color Gradient High": "seven_color_gradient_high_speed",
    "Seven Color Gradient Low": "seven_color_gradient_low",
    "Rapid Blinking": "rapid_blinking_low",
    "Three Color Gradient": "three_color_gradient",
    "Green Gradient": "green_gradient",
    "Blue Strobe": "blue_strobe",
    "White Flow High": "white_flow_high_speed",
    "Blue Flow High": "blue_flow_high_speed",
    "Purple on Blue High": "purple_on_blue_high_speed",
    "Yellow on Blue High": "yellow_on_blue_high_speed",
    "Green on Blue High": "green_on_blue_high_speed",
    "Red on Blue High": "red_on_blue_high_speed",
    "White on Green High": "white_on_green_high_speed",
    "Multi on Red": "multi_on_red",
    "Static Light Red": "static_red",
    "Static Light Green": "static_green",
    "Static Light Blue": "static_blue",
    "Static White Low": "static_white_low",
    "Static White High": "static_white_high",
    "Static Light Yellow": "static_light_yellow",
    "Static Yellow Green": "static_yellow_green",
    "Static Light Green": "static_light_green",
    "Static Light White": "static_light_white",
    "Static White Green": "static_white_green",
    "Static Light Sky Blue": "static_light_sky_blue_high",
    "Static Light Green Low": "static_light_green_low",
    "Static Purple Low": "static_purple_low",
    "Static Warm Medium": "static_warm_medium",
}


# -------------------------------
# Setup Entry
# -------------------------------
async def async_setup_entry(hass, entry, async_add_entities):
    """Set up BLE Magic Light from config entry."""
    device = BleMagicLightDevice(entry.data["address"])
    async_add_entities([BleMagicLight(entry.title, device)])


# -------------------------------
# Light Entity
# -------------------------------
class BleMagicLight(LightEntity):
    """Representation of a BLE Magic Light."""

    _attr_supported_color_modes = {COLOR_MODE_BRIGHTNESS, COLOR_MODE_HS}
    _attr_color_mode = COLOR_MODE_BRIGHTNESS
    _attr_supported_features = SUPPORT_COLOR | SUPPORT_EFFECT

    def __init__(self, name, device: BleMagicLightDevice):
        self._attr_name = name
        self._device = device
        self._is_on = False
        self._hs_color = (0, 0)
        self._effect = None

    # -------------------------------
    # Properties
    # -------------------------------
    @property
    def is_on(self):
        return self._is_on

    @property
    def effect(self):
        return self._effect

    @property
    def effect_list(self):
        return list(EFFECTS.keys())

    @property
    def hs_color(self):
        return self._hs_color

    # -------------------------------
    # Async Commands
    # -------------------------------
    async def async_turn_on(self, **kwargs):
        # Handle effect first
        effect = kwargs.get("effect")
        hs_color = kwargs.get("hs_color")

        if effect:
            cmd_key = EFFECTS.get(effect)
            if cmd_key:
                await self._device.send(cmd_key)
                self._effect = effect
                self._is_on = True
                self.async_write_ha_state()
                return

        # Handle color
        if hs_color:
            # Map to closest static color (you can improve with a proper color lookup)
            self._hs_color = hs_color
            # Example: pick static_white_high if brightness > 50
            if hs_color[1] > 50:
                await self._device.send("static_white_high")
            else:
                await self._device.send("static_white_low")
            self._effect = None
            self._is_on = True
            self.async_write_ha_state()
            return

        # Default turn on
        await self._device.send("turn_on")
        self._is_on = True
        self._effect = None
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._device.send("turn_off")
        self._is_on = False
        self._effect = None
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        await self._device.disconnect()
