uint64_t encryptData(uint64_t PlainText, uint64_t PublicKeyE, uint64_t PublicKeyN) {
  uint64_t CipherText = 1;

  PlainText = PlainText % PublicKeyN
  while (PublicKeyE > 0){
    if (PublicKeyE & 1) {
      CipherText = (CipherText * 1LL * PlainText) % PublicKeyN;
    }
    PlainText = (PlainText * 1LL * PlainText) % PublicKeyN;
    PublicKeyE = PublicKeyE / 2;
  }

  return CipherText;
}
