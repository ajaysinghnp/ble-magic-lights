import asyncio
from bleak import BleakClient
from .commands import COMMANDS


class BleMagicLightDevice:
    """Represents a single BLE Magic Light."""

    def __init__(self, address: str):
        self.address = address
        self.client: BleakClient | None = None
        self.cmd_uuid = "0000fff3-0000-1000-8000-00805f9b34fb"
        self.notify_uuid = "0000fff4-0000-1000-8000-00805f9b34fb"
        self.commands = COMMANDS

    # -------------------------------
    # Notify handler
    # -------------------------------
    def notify_handler(self, sender, data: bytearray):
        print(f"🔔 Notify from {sender}: {data.hex()}")

    # -------------------------------
    # Connect and setup
    # -------------------------------
    async def connect(self):
        self.client = BleakClient(self.address)
        await self.client.connect()
        print("✅ Connected:", self.client.is_connected)
        # Enable notifications
        await self.client.start_notify(self.notify_uuid, self.notify_handler)
        await asyncio.sleep(0.3)

    # -------------------------------
    # Disconnect & cleanup
    # -------------------------------
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
