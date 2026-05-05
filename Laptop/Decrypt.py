def Decrypt(CipherText, KeyD, KeyN):
  PlainText = pow(CipherText, KeyD, KeyN)
  return PlainText
