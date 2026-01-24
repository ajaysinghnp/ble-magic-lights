import asyncio
from bleak import BleakClient
from bleak_retry_connector import establish_connection

# -------------------------------
# All known BLE Magic Light commands
# -------------------------------
COMMANDS = {
    "turn_on": bytes.fromhex("bf01b05ee288275b1f3e64d8d47d85af1a"),
    "turn_off": bytes.fromhex("c060011068201190def3b5375b1e3e6435"),
    "static_red": bytes.fromhex("a79b0ede83e0204abc07624fc4602190c9"),
    "static_green": bytes.fromhex("d7f395b74a191c64d82b7d85af9b2e5e3d"),
    "static_blue": bytes.fromhex("0b90fe73a418791e3e6427d47d85af9b1b"),
    "static_white_low": bytes.fromhex("f5b517db0fd554d8d47d85af9b2e5e927e"),
    "static_white_high": bytes.fromhex("a49b0ede83fb204abcf89d4fc4602190e9"),
    # add all other commands here...
}


class BleMagicLightDevice:
    """Represents a single BLE Magic Light."""

    def __init__(self, address: str):
        self.address = address
        self.client: BleakClient | None = None
        self.cmd_uuid = "0000fff3-0000-1000-8000-00805f9b34fb"
        self.notify_uuid = "0000fff4-0000-1000-8000-00805f9b34fb"

    # -------------------------------
    # Notify handler
    # -------------------------------
    def notify_handler(self, sender, data: bytearray):
        print(f"🔔 Notify from {sender}: {data.hex()}")

    # -------------------------------
    # Connect / Disconnect
    # -------------------------------
    async def connect(self):
        """Establish a reliable BLE connection with retries."""
        self.client = await establish_connection(
            BleakClient, self.address, max_attempts=5, retry_delay=1.0
        )
        await self.client.start_notify(self.notify_uuid, self.notify_handler)
        await asyncio.sleep(0.3)

    async def disconnect(self):
        if self.client:
            await self.client.stop_notify(self.notify_uuid)
            await self.client.disconnect()
            self.client = None

    # -------------------------------
    # Send a command
    # -------------------------------
    async def send(self, command_name: str):
        if self.client is None:
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
