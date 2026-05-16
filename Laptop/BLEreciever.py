import asyncio
from bleak import BleakScanner, BleakClient
import queue

from Decrypt import Decrypt

DEVICE_NAME = "CUNT"
CHAR_UUID = "2A56"
SEND_UUID = "2A57"

receQ = queue.Queue()
sendQ = queue.Queue()
connected = False

async def ble(KeyN, KeyE, KeyD):
    global connected
    
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
    connected = True

    async with BleakClient(target.address) as client:
        print("Connected!")

        async def handle_data(sender, data):
            decor = data.decode("utf-8")
            if decor == "GIVEKEY":
                await client.write_gatt_char(SEND_UUID, str(f"{KeyN},{KeyE}").encode())
                print(f"SentKey: {KeyN},{KeyE}")
            else:
                x, y, z, t = ParseData(decor, KeyN, KeyD)
                receQ.put((x,y,z,t))    

        await client.start_notify(CHAR_UUID, handle_data)

        print("Listening for data... Press Ctrl+C to exit.")
        while True:
            if not sendQ.empty():
                await client.write_gatt_char(SEND_UUID, str(sendQ.get()).encode())
            await asyncio.sleep(1)


def ParseData(data, KeyN, KeyD):
    try:
        splitData = data.split(",")
        x, y, z, t = int(splitData[0]), int(splitData[1]), int(splitData[2]), int(splitData[3])
        #print(f"X: {x}, Y: {y}, Z: {z}, t: {t}")

        x = float(Decrypt(x, KeyD, KeyN))
        y = float(Decrypt(y, KeyD, KeyN))
        z = float(Decrypt(z, KeyD, KeyN))
        t = float(Decrypt(t, KeyD, KeyN))

        x -= 5000000
        x /= 100

        y -= 5000000
        y /= 100

        z -= 5000000
        z /= 100

        t /= 1000

        return x, y, z, t
    except Exception as e:
        print("err parse: ", e)
        print()
        return 0, 0, 0, 0

if __name__ == "__main__":
    asyncio.run(ble())