import numpy as np

def FFT(data, FREQ):
    vlaues = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(len(data), 1/FREQ)

    #return vlaues, freqs
    return _removeLowerMags(vlaues, freqs)

def _maxVal(data):
    biggest = data[0]
    
    for i in range(1, len(data)):
        if biggest < data[i]:
            biggest = data[i]

    return biggest


def _removeLowerMags(vals, freqs):
    biggest = _maxVal(vals)

    returnVals = []
    returnFreq = []

    for i in range(0, len(vals)):
        if vals[i] > 0.05 * biggest:
            returnVals.append(float(vals[i]))
            returnFreq.append(float(freqs[i]))

    return returnVals, returnFreq
