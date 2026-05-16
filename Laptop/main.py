import threading
import asyncio
from time import sleep
import sys
import numpy as np
import tkinter as tk

from GraphData import SetupGraphs, GraphData, plt, plotX, plotY, plotZ
from BLEreciever import ble, receQ, connected, sendQ
from GenerateKey import GenerateKey
from WriteToFile import WriteToFile
from ReadFile import ReadFile

axs = None
root = None

startTime = -1
lastRecorded = 0

temp = np.sin(np.linspace(0, (100 - 1) * 1, 100))
curT = 0

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

def plotting():
    global startTime
    global lastRecorded
    global curT

    try:
        if not receQ.empty():
            x, y, z, t = receQ.get()

            if startTime == -1:
                startTime = t

            t -= startTime

            WriteToFile(x, y, z, t)
            GraphData(axs, x, y, z, t)

            lastRecorded = t
        else:
            # fallback test data so graph keeps moving
            exist = True
            #GraphData(axs, temp[curT], temp[curT], temp[curT], curT)
            #curT = (curT + 1) % len(temp)

    except Exception as e:
        print("Update error:", e)

    root.after(10, plotting)

def main():
    global axs
    global root

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
    
    while receQ.empty():
        print("Failed connecting attempt")
        sleep(1)

    axs = None
    fig = None
    root = None
    if loading:
        x, y, z, t = ReadFile(filepath)
        axs, fig, root = SetupGraphs(x, y, z, t)
    else:
        axs, fig, root = SetupGraphs([], [], [], [])


    def _start():
        sendQ.put("start")

    def _stop():
        sendQ.put("stop")


    btnStart = tk.Button(master=root, text="Start", command=_start)
    btnStop = tk.Button(master=root, text="Stop", command=_stop)
    btnStart.pack(side=tk.BOTTOM)
    btnStop.pack(side=tk.BOTTOM)

    cbX = tk.IntVar()
    cbY = tk.IntVar()
    cbZ = tk.IntVar()
    
    def _cbUpdate():
        plotX = (cbX.get() == 1)
        plotY = (cbY.get() == 1)
        plotZ = (cbZ.get() == 1)
    
    c1 = tk.Checkbutton(root, text='Plot X', variable=cbX, command=_cbUpdate)
    c1.pack(side=tk.BOTTOM)


    plotting()

    root.mainloop()

if __name__ == "__main__":
    main()