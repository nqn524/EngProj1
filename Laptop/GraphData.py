import matplotlib.pyplot as plt
import numpy as np
import FFT

# np.linspace(x, x + (n-1)*y, n)
# x = start
# y = step
# n = number of elements
# 
# Produces: [x, x + y, x + 2y, ..., x + (n-2)y, x + (n-1)y]

def SetupGraphs():
    fig = plt.figure()
    axs = fig.add_subplot(2,1,1)

    plt.title = "x"

    plt.plot([1,2,3,4,5], [1,4,9,16,25])
    plt.plot([1,2,3,4,5], [25,16,9,4,1])
    plt.plot([1,2,3,4,5], [25,1,4,16,9])

    plt.show()

    return axs

def GraphData(axs, x, y, z):
    print(x)
    print(y)
    print(z)

    Freq = 24.0
    
    n = len(x)

    if len(y) < n:
        n = len(y)
    elif len(z) < n:
        n = len(z)

    print(n)

    if len(x) > n:
        del x[-(len(x) - n):]
    if len(y) > n:
        del y[-(len(y) - n):]
    if len(z) > n:
        del z[-(len(z) - n):]

    t = np.linspace(0, (n - 1) * (1.0/Freq), n) 
    print(t)
   
    axs.clear()

    axs.plot(t.tolist(), x)
    axs.plot(t.tolist(), y)
    axs.plot(t.tolist(), z)

    

if __name__ == "__main__":
    axs = SetupGraphs()
    GraphData(axs, (np.linspace(0, (18 - 1) * 1.0/24.0, 18) + np.random.randn(18) * 0.1).tolist(),
               (np.linspace(0, (20 - 1) * 1.0/24.0, 20) + np.random.randn(20) * 0.1).tolist(), 
               (np.linspace(0, (20 - 1) * 1.0/24.0, 20) + np.random.randn(20) * 0.1).tolist())
