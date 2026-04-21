import numpy as np

def FFT(data, FREQ):
    vlaues = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(len(data), 1/FREQ)

    return freqs, vlaues


if __name__ == "__main__":
    print()
