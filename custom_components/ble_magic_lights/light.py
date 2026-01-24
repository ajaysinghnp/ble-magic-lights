from homeassistant.components.light import LightEntity
from homeassistant.const import COLOR_MODE_ONOFF
from .ble_device import BleMagicLightDevice


async def async_setup_entry(hass, entry, async_add_entities):
    device = BleMagicLightDevice(entry.data["address"])
    async_add_entities([BleMagicLight(entry.title, device)])


class BleMagicLight(LightEntity):
    _attr_supported_color_modes = {COLOR_MODE_ONOFF}
    _attr_color_mode = COLOR_MODE_ONOFF

    def __init__(self, name, device: BleMagicLightDevice):
        self._attr_name = name
        self._device = device
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._device.send("turn_on")
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._device.send("turn_off")
        self._is_on = False
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        await self._device.disconnect()
