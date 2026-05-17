import math
import time

def main(KeyN):
    print(math.sqrt(KeyN))
    for i in range(1, int(math.sqrt(KeyN))):
        if KeyN % i == 0:
            if checkPrime(i):
                prime1 = i
                prime2 = KeyN / i

                return prime1, prime2
            

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
    print(main(818878535543882929)) # example public key used to try and crack is 818878535543882929 
    print(time.time() - starttime) # output was 29.58 seconds

    # p = 629050217
    # q = 1301769737