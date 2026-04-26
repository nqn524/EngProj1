import asyncio
from bleak import BleakScanner, BleakClient
import queue

DEVICE_NAME = "CUNT"
CHAR_UUID = "2A56"

q = queue.Queue()

async def ble():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    target = None
    for d in devices:
        print(f"Found: {d.name} ({d.address})")
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
            x, y, z, t = ParseData(data.decode("utf-8"))
            q.put((x,y,z,t))

        await client.start_notify(CHAR_UUID, handle_data)

        print("Listening for data... Press Ctrl+C to exit.")
        while True:
            await asyncio.sleep(1)


def ParseData(data):
    splitData = data.split(",")
    x, y, z, t = float(splitData[0]), float(splitData[1]), float(splitData[2]), float(splitData[3])

    x -= 5000000
    x /= 100

    y -= 5000000
    y /= 100

    z -= 5000000
    z /= 100

    t /= 1000

    return x, y, z, t