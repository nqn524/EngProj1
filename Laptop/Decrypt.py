KeyD = 56354
KeyN = 984123

def Decrypt(CipherText):
    PlainText = pow(CipherText, KeyD, KeyN)
    return PlainText
