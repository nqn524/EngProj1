import matplotlib.pyplot as plt
import numpy as np
import FFT
import time

# np.linspace(x, x + (n-1)*y, n)
# x = start
# y = step
# n = number of elements
# 
# Produces: [x, x + y, x + 2y, ..., x + (n-2)y, x + (n-1)y]

xData = []
yData = []
zData = []

xRecent = []
yRecent = []
zRecent = []

t = []

FREQ = 24.0
NUM_OF_REC_SAMPS = int(FREQ * 5)

SAMPLES = int(FREQ * 15)


TIME_BETWEEN_RENDERS = 1
samplesSinceLastRender = 0

def _generate_array(n, TD):
    start = TD - (SAMPLES - n) * TD
    t = start + np.arange(SAMPLES) * TD
    return t

def SetupGraphs(x, y, z):
    global xData
    global yData
    global zData

    global xRecent
    global yRecent
    global zRecent

    global t

    n = len(x)
    
    xData = np.concatenate([np.linspace(0, 0, SAMPLES - len(x)), x]).tolist()
    yData = np.concatenate([np.linspace(0, 0, SAMPLES - len(y)), y]).tolist()
    zData = np.concatenate([np.linspace(0, 0, SAMPLES - len(z)), z]).tolist()
    
    xRecent = xData[-NUM_OF_REC_SAMPS:]
    yRecent = yData[-NUM_OF_REC_SAMPS:]
    zRecent = zData[-NUM_OF_REC_SAMPS:]

    t = _generate_array(n, 1.0/FREQ).tolist()


    fig, axs = plt.subplots(2,2)
    
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    
    # Create a single line and keep reference
    axs[0,0].plot(t, xData, label="X", color="red")
    axs[0,0].plot(t, yData, label="Y", color="green")
    axs[0,0].plot(t, zData, label="Z", color="blue")
    
    axs[0,0].set_xlabel("Time")
    axs[0,0].set_ylabel("Amplitude")
    axs[0,0].set_title("Raw data")
    #axs[0,0].legend()

    axs[0,1].set_xlabel("Freq")
    #axs[0,1].set_ylabel("Amplitude")



    axs[1,0].plot(t[-NUM_OF_REC_SAMPS:], xRecent, label="X", color="red")
    axs[1,0].plot(t[-NUM_OF_REC_SAMPS:], yRecent, label="Y", color="green")
    axs[1,0].plot(t[-NUM_OF_REC_SAMPS:], zRecent, label="Z", color="blue")

    axs[1,0].set_xlabel("Time")
    axs[1,0].set_ylabel("Amplitude")
    axs[1,0].set_title("Last 10 seconds")
    #axs[1,0].legend()

    axs[1,1].set_xlabel("Freq")
    #axs[1,1].set_ylabel("Amplitude")

    plt.ion()
    plt.show(block=False)
    
    return axs

def GraphData(axs, x, y, z):
    global xData
    global yData
    global zData

    global xRecent
    global yRecent
    global zRecent

    global t


    del xData[0]
    del yData[0]
    del zData[0]

    del xRecent[0]
    del yRecent[0]
    del zRecent[0]

    del t[0]

    xData.append(x)
    yData.append(y)
    zData.append(z)

    xRecent.append(x)
    yRecent.append(y)
    zRecent.append(z)

    t.append(t[-1] + 1.0/FREQ)

    global samplesSinceLastRender

    if (samplesSinceLastRender < TIME_BETWEEN_RENDERS * FREQ):
        samplesSinceLastRender += 1
    else:
        samplesSinceLastRender = 0


        magX, freqX = FFT.FFT(xData, FREQ)
        magY, freqY = FFT.FFT(xData, FREQ)
        magZ, freqZ = FFT.FFT(xData, FREQ)

        netMag, netFreq = FFT.removeLowerMags(np.sqrt(np.square(magX) + np.square(magY) + np.square(magZ)), freqX)
        print(netMag)

        axs[1,1].cla()

        markLine, stemLine, _ = axs[1,1].stem(netFreq, netMag, label="X")
    
        #markLineX, stemLineX, _ = axs[1,1].stem(freqX, magX, label="X")
        #markLineY, stemLineY, _ = axs[1,1].stem(freqY, magY, label="Y")
        #markLineZ, stemLineZ, _ = axs[1,1].stem(freqZ, magZ, label="Z")
    #
        #plt.setp(markLineX, color="red")
        #plt.setp(stemLineX, color="red")
    #
        #plt.setp(markLineY, color="green")
        #plt.setp(stemLineY, color="green")
    #
        #plt.setp(markLineZ, color="blue")
        #plt.setp(stemLineZ, color="blue")



        linesRaw = axs[0,0].get_lines()
        linesRecent = axs[1,0].get_lines()

        linesRaw[0].set_ydata(xData)
        linesRaw[1].set_ydata(yData)
        linesRaw[2].set_ydata(zData)

        linesRecent[0].set_ydata(xRecent)
        linesRecent[1].set_ydata(yRecent)
        linesRecent[2].set_ydata(zRecent)



        linesRaw[0].set_xdata(t)
        linesRaw[1].set_xdata(t)
        linesRaw[2].set_xdata(t)

        linesRecent[0].set_xdata(t[-NUM_OF_REC_SAMPS:])
        linesRecent[1].set_xdata(t[-NUM_OF_REC_SAMPS:])
        linesRecent[2].set_xdata(t[-NUM_OF_REC_SAMPS:])


        axs[0,0].relim()
        axs[0,0].autoscale_view()

        axs[1,0].relim()
        axs[1,0].autoscale_view()

        axs[0,1].relim()
        axs[0,1].autoscale_view()

        axs[1,1].relim()
        axs[1,1].autoscale_view()

        plt.pause(0.001)




    

if __name__ == "__main__":
    t2 = np.linspace(0, (SAMPLES - 1) * 1.0/FREQ, SAMPLES)
    #axs = SetupGraphs((np.linspace(0, (18 - 1) * 1.0/24.0, 18) + np.random.randn(18) * 0.1).tolist(),
    #           (np.linspace(0, (20 - 1) * 1.0/24.0, 20) + np.random.randn(20) * 0.1).tolist(), 
    #           (np.linspace(0, (20 - 1) * 1.0/24.0, 20) + np.random.randn(20) * 0.1).tolist())

    noiseAmp = 0.00

    xAccel = (np.sin(2 * np.pi * 1 * t2) + np.sin(2 * np.pi * 2 * t2) + np.sin(2 * np.pi * 3 * t2) + np.random.randn(SAMPLES) * noiseAmp)
    yAccel = (np.sin(2 * np.pi * 1 * t2) + np.sin(2 * np.pi * 3 * t2) + np.sin(2 * np.pi * 5 * t2) + np.random.randn(SAMPLES) * noiseAmp)
    zAccel = (np.sin(2 * np.pi * 1 * t2) + np.sin(2 * np.pi * 1.5 * t2) + np.sin(2 * np.pi * 2.5 * t2) + np.random.randn(SAMPLES) * noiseAmp)

    #axs = SetupGraphs(xAccel.tolist(), yAccel.tolist(), zAccel.tolist())

    axs = SetupGraphs([],[],[])


    index = 0

    while index < len(xAccel):
        if index >= len(xAccel):
            continue

        GraphData(axs, xAccel[index], yAccel[index], zAccel[index])

        index += 1

        time.sleep(1/FREQ)


    #GraphData(axs, 1, 2, 3)

    plt.show(block=True)
