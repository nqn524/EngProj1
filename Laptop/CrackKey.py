import math
import time

def main(KeyN):
    print(math.sqrt(KeyN))
    for i in range(0, int(math.sqrt(KeyN))):
        if checkPrime(i):
            if KeyN % i == 0:
                prime1 = i
                prime2 = KeyN / i

                return prime1, prime2
        if i % 1000000 == 0:
            print(i)
            

    return -1, -1

def checkPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    starttime = time.time()
    print(main(818878535543882929))
    print(time.time() - starttime)

    # p = 629050217
    # q = 1301769737