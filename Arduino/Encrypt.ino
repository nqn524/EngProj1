int encryptMessage(int PlainText, int PublicKeyE, int PublicKeyN) {
  int CipherText = 1;
  
  for (int i = 0; i < PublicKeyE; i++) {
    CipherText = (CipherText * PlainText) % PublicKeyN;
  }
  
  return CipherText;
}
