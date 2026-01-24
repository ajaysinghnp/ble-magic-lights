import asyncio
from bleak import BleakClient
from .const import CMD_UUID, NOTIFY_UUID

COMMANDS = {
    "turn_on": bytes.fromhex("bf01b05ee288275b1f3e64d8d47d85af1a"),
    "turn_off": bytes.fromhex("c060011068201190def3b5375b1e3e6435"),
    "static_red": bytes.fromhex("a79b0ede83e0204abc07624fc4602190c9"),
    "static_green": bytes.fromhex("d7f395b74a191c64d82b7d85af9b2e5e3d"),
    "static_blue": bytes.fromhex("0b90fe73a418791e3e6427d47d85af9b1b"),
    "white_low": bytes.fromhex("f5b517db0fd554d8d47d85af9b2e5e927e"),
    "white_high": bytes.fromhex("a49b0ede83fb204abcf89d4fc4602190e9"),
}


class BleMagicLightDevice:
    """Low-level BLE Magic Light handler"""

    def __init__(self, address: str):
        self.address = address
        self.client: BleakClient | None = None

    async def connect(self):
        if self.client and self.client.is_connected:
            return

        self.client = BleakClient(self.address)
        await self.client.connect()

        await self.client.start_notify(NOTIFY_UUID, self._notify)

        # Mandatory init sequence
        await self._write(bytes.fromhex("01"))
        await asyncio.sleep(0.15)
        await self._write(bytes.fromhex("52"))
        await asyncio.sleep(0.2)

    async def disconnect(self):
        if self.client:
            await self.client.stop_notify(NOTIFY_UUID)
            await self.client.disconnect()

    async def send(self, command: str):
        await self.connect()
        await self._write(COMMANDS[command])

    async def _write(self, data: bytes):
        await self.client.write_gatt_char(CMD_UUID, data, response=False)

    def _notify(self, sender, data: bytearray):
        # Reserved for reverse-engineering / ACK handling
        pass
