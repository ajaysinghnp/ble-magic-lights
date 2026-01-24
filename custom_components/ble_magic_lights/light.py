import asyncio
import logging
from homeassistant.components.light import LightEntity
from bleak import BleakClient
from .commands import COMMANDS

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ble_magic_lights"


class BLEMagicLamp(LightEntity):
    """BLE Magic Lamp Entity."""

    def __init__(self, name, address):
        self._name = name
        self._address = address
        self._client = None
        self._is_on = False
        self._brightness = 255
        # UUIDs
        self._cmd_uuid = "0000fff3-0000-1000-8000-00805f9b34fb"
        self._notify_uuid = "0000fff4-0000-1000-8000-00805f9b34fb"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._connect()
        await self._send(COMMANDS["turn_on"])
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._connect()
        await self._send(COMMANDS["turn_off"])
        self._is_on = False
        self.async_write_ha_state()

    async def async_set_color(self, color="static_red"):
        if color in COMMANDS:
            await self._connect()
            await self._send(COMMANDS[color])

    async def _connect(self):
        if self._client is None:
            self._client = BleakClient(self._address)
            await self._client.connect()
            await self._client.start_notify(self._notify_uuid, self._notify_handler)
            await asyncio.sleep(0.3)

    async def _send(self, payload: bytes):
        # Init sequence
        await self._client.write_gatt_char(
            self._cmd_uuid, bytes.fromhex("01"), response=False
        )
        await asyncio.sleep(0.15)
        await self._client.write_gatt_char(
            self._cmd_uuid, bytes.fromhex("52"), response=False
        )
        await asyncio.sleep(0.2)
        await self._client.write_gatt_char(self._cmd_uuid, payload, response=False)
        await asyncio.sleep(0.1)

    def _notify_handler(self, sender, data: bytearray):
        _LOGGER.debug("Notify from %s: %s", sender, data.hex())
