def Decrypt(CipherText, KeyD, KeyN):
  PlainText = pow(CipherText, KeyD, KeyN)
  #print(f"{CipherText}    {PlainText}")
  return PlainText
