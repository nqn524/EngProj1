import threading
import asyncio
from time import sleep
import sys

from GraphData import SetupGraphs, GraphData, plt
from BLEreciever import ble, q, connected
from GenerateKey import GenerateKey
from ReadFile import ReadFile

startTime = -1

KeyN = -1
KeyE = -1
KeyD = -1

def start_ble():
    try:
        KeyN, KeyE, KeyD = GenerateKey()
        print((KeyN, KeyE, KeyD))

        asyncio.run(ble(KeyN, KeyE, KeyD))
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

def main():
    loading = False
    filepath = ""

    for i in range(0, len(sys.argv)):
        if sys.argv[i] == "load":
            if len(sys.argv) == i + 1:
                print("No provided file path")
                return
            else:
                loading = True
                filepath = sys.argv[i+1]

    ble_thread = threading.Thread(target=start_ble, daemon=True);
    ble_thread.start();

    sleep(10)
    
    while q.empty():
        print("Failed connecting attempt")
        sleep(1)
    
    axs = None
    if loading:
        x, y, z, t = ReadFile(filepath)
        axs = SetupGraphs(x, y, z, t)
    else:
        axs = SetupGraphs([], [], [], [])
    
    plotting(axs)

if __name__ == "__main__":
    main()