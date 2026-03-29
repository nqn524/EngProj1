import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "CUNT"
CHAR_UUID = "2A56"

async def main():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    target = None
    for d in devices:
        if d.name == DEVICE_NAME:
            target = d
            break

    if not target:
        print("Device not found!")
        return

    print(f"Found device: {target.name} ({target.address})")

    async with BleakClient(target.address) as client:
        print("Connected!")

        def handle_data(sender, data):
            value = int.from_bytes(data, byteorder='little')
            print(f"Received: {value}")

        await client.start_notify(CHAR_UUID, handle_data)

        print("Listening for data... Press Ctrl+C to exit.")
        while True:
            await asyncio.sleep(1)

asyncio.run(main())