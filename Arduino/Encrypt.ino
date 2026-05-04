uint64_t encryptData(uint64_t PlainText, uint64_t PublicKeyE, uint64_t PublicKeyN) {
  uint64_t CipherText = 1;

  PlainText %= PublicKeyN;

  while (PublicKeyE > 0) {
    if (PublicKeyE & 1) {
      CipherText = mulmod(CipherText, PlainText, PublicKeyN);
    }
    PlainText = mulmod(PlainText, PlainText, PublicKeyN);
    PublicKeyE >>= 1;
  }

  return CipherText;
}

uint64_t mulmod(uint64_t a, uint64_t b, uint64_t mod) {
  uint64_t result = 0;
  a %= mod;

  while (b > 0) {
    if (b & 1) {
      result = (result + a) % mod;
    }
    a = (a << 1) % mod;
    b >>= 1;
  }

  return result;
}
