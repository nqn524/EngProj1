import random
import math
import GeneratePrime

def GenerateKey():
  p = GeneratePrime.GeneratePrime()
  q = GeneratePrime.GeneratePrime()
  KeyN = p * q
  k = (p-1) * (q-1)
  
  KeyE = 65537
  #while ( math.gcd( KeyE, k) != 1): #generating a suitable keyE
  #    KeyE = random.randint(1, KeyN)
  
      #Basically going randomly through suitable primes until one sticks
      
  KeyD = pow(KeyE, -1, k) #Functon performs modular inverse on KeyE (mod k) to find a suitable keyD
  return KeyN, KeyE, KeyD


