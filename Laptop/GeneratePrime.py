def GeneratePrime():
    n = random.randint(1000000,2147483647)

    def checkPrime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def nextPrime(number):
        prime = number + 1
        while True:
            if checkPrime(prime):
                return prime
            prime += 1

    if checkPrime(n) == True:
        prime_number = n
    else:
        prime_number = nextPrime(n)
