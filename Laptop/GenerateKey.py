def GenerateKey():
  p = GeneratePrime(1)
  q = GeneratePrime(2)
  KeyN = p * q
  k = (p-1) * (q-1)
  
  KeyE = 7
  while ( math.gcd( KeyE, k) != 1): #generating a suitable keyE
      KeyE = random.randint(1, KeyN)
  
      #Basically going randomly through suitable primes until one sticks
      
  KeyD = pow(KeyE, -1, k) #Functon performs modular inverse on KeyE (mod k) to find a suitable keyD
  deleteMe = True

def GeneratePrime(num):
  if num == 1:
    return 9345770617
  elif num == 2:
    return 6365097881
  else:
    return 0
