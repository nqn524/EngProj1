import threading
import asyncio
from time import sleep

from GraphData import SetupGraphs, GraphData, plt
from BLEreciever import ble, q, connected

startTime = -1

def start_ble():
    try:
        asyncio.run(ble())
    except Exception as e:
        print("BLE error:", e)

def plotting(axs):
    global startTime

    try:
        while True:
            if not q.empty():
                x, y, z, t = q.get();

                if startTime == -1:
                    startTime = t

                t -= startTime
                print(f"X: {x}, Y: {y}, Z: {z}, time: {t}")

                GraphData(axs, x, y, z, t)
                #plt.pause(0.001)
    except Exception as e:
        print("Plot error:", e)

if __name__ == "__main__":

    q.put(None)
    print(q.get())

    ble_thread = threading.Thread(target=start_ble, daemon=True);
    ble_thread.start();

    sleep(10)
    
    if q.empty():
        print("Failed connecting to client")
        ble_thread
    else:
        axs = SetupGraphs([], [], [], [])
        plotting(axs)