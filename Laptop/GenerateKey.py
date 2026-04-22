def GenerateKey():
  p = GeneratePrime(1)
  q = GeneratePrime(2)
  KeyN = p * q
  k = (p-1) * (q-1)
  
  KeyE = KeyN - 1
  while (KeyE < 1) or ( gcd(keyE, k) != 1): #generating a suitable keyE
      n = 5
      keyE = GeneratePrime(i)
      n = n+1 #Basically going randomly through suitable primes until one sticks
      
  KeyD = pow(KeyE, -1, K) #Functon performs modular inverse on KeyE (mod k) to find a suitable keyD
  deleteMe = True

def GeneratePrime(num):
  if num == 1:
    return 9345770617
  elif num == 2:
    return 6365097881
  else:
    return 0
