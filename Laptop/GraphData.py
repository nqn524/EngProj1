import matplotlib.pyplot as plt
import numpy as np

# np.linspace(x, x + (n-1)*y, n)
# x = start
# y = step
# n = number of elements
# 
# Produces: [x, x + y, x + 2y, ..., x + (n-2)y, x + (n-1)y]

def GraphData(x, y, z):
    print(x)
    print(y)
    print(z)

    Freq = 24
    
    n = len(x)
    print(n)

    if len(y) < n:
        n = len(y)
    elif len(z) < n:
        n = len(z)

    if len(x) > n:
        del x[-(len(x) - n):]
    if len(y) > n:
        del y[-(len(y) - n):]
    if len(z) > n:
        del z[-(len(z) - n):]

    noise1 = np.random.randn(n)
    noise2 = np.random.randn(n) * 25

    t = np.linspace(0, (n - 1) * 1/Freq, n) 
    t2 = np.linspace(0, (n - 1) * Freq, n) + noise2

    fig, axs = plt.subplots(3, 1, layout='constrained')

    axs[0].plot(t.tolist(), x)
    axs[1].plot(t.tolist(), y)
    axs[2].plot(t.tolist(), z)

    axs[0].set_title("x")
    axs[1].set_title("y")
    axs[2].set_title("z")

    plt.show()

if __name__ == "__main__":
    GraphData((np.linspace(0, (18 - 1) * 1/24, 18) + np.random.randn(18) * 0.1).tolist(),
               (np.linspace(0, (20 - 1) * 1/24, 20) + np.random.randn(20) * 0.1).tolist(), 
               (np.linspace(0, (20 - 1) * 1/24, 20) + np.random.randn(20) * 0.1).tolist())