"""BLE Magic Light device abstraction using Home Assistant's Bluetooth stack."""

import asyncio
import logging

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant

from .commands import COMMANDS

_LOGGER = logging.getLogger(__name__)


class BleMagicLightDevice:
    """Represents a single BLE Magic Light."""

    def __init__(self, hass: HomeAssistant, address: str):
        self.hass = hass
        self.address = address
        self.client: BleakClient | None = None
        self.cmd_uuid = "0000fff3-0000-1000-8000-00805f9b34fb"
        self.notify_uuid = "0000fff4-0000-1000-8000-00805f9b34fb"
        self.commands = COMMANDS

    # -------------------------------
    # Notify handler
    # -------------------------------
    def _notify_handler(self, sender, data: bytearray):
        _LOGGER.debug("Notify from %s: %s", sender, data.hex())

    # -------------------------------
    # Resolve BLEDevice through HA
    # -------------------------------
    def _resolve_ble_device(self) -> BLEDevice:
        """Resolve a BLEDevice from the Home Assistant Bluetooth stack."""
        ble_device = bluetooth.async_ble_device_from_address(
            self.hass, self.address, connectable=True
        )
        if ble_device is None:
            raise RuntimeError(
                f"Could not resolve BLE device for address {self.address}. "
                "Ensure the device is powered on and in range."
            )
        return ble_device

    # -------------------------------
    # Connect and setup
    # -------------------------------
    async def connect(self):
        """Connect to the BLE device via the HA Bluetooth stack."""
        ble_device = self._resolve_ble_device()
        self.client = await establish_connection(BleakClient, ble_device, self.address)
        _LOGGER.info("Connected to %s: %s", self.address, self.client.is_connected)
        # Enable notifications
        await self.client.start_notify(self.notify_uuid, self._notify_handler)
        await asyncio.sleep(0.3)

    # -------------------------------
    # Disconnect & cleanup
    # -------------------------------
    async def disconnect(self):
        if self.client:
            try:
                await self.client.stop_notify(self.notify_uuid)
            except Exception:  # noqa: BLE001
                _LOGGER.debug("Failed to stop notifications", exc_info=True)
            await self.client.disconnect()
            self.client = None

    # -------------------------------
    # Send a command
    # -------------------------------
    async def send(self, command_name: str):
        if self.client is None or not self.client.is_connected:
            raise RuntimeError("Device not connected")
        payload = COMMANDS.get(command_name)
        if not payload:
            raise ValueError(f"Unknown command: {command_name}")

        # Init sequence required for all commands
        await self.client.write_gatt_char(
            self.cmd_uuid, bytes.fromhex("01"), response=False
        )
        await asyncio.sleep(0.15)
        await self.client.write_gatt_char(
            self.cmd_uuid, bytes.fromhex("52"), response=False
        )
        await asyncio.sleep(0.2)

        # Send actual payload
        await self.client.write_gatt_char(self.cmd_uuid, payload, response=False)
        await asyncio.sleep(0.1)

    # -------------------------------
    # High-level commands
    # -------------------------------
    async def turn_on(self):
        await self.send("turn_on")

    async def turn_off(self):
        await self.send("turn_off")

    async def static_red(self):
        await self.send("static_red")

    async def static_white(self, intensity="high"):
        if intensity == "high":
            await self.send("static_white_high")
        else:
            await self.send("static_white_low")
