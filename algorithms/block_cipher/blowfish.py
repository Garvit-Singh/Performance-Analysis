from Crypto import Random
from Crypto.Cipher import Blowfish

class BlowfishCryptor:
    def __init__(self, key):
        self.key = key
        self.iv = Random.new().read(Blowfish.block_size)

    def getIV(self):
        return self.iv
        
    def encrypt(self, plaintext):
        return Blowfish.new(key=self.key, mode=Blowfish.MODE_CBC, IV=self.iv).encrypt(plaintext)
    
    def decrypt(self, ciphertext):
        return Blowfish.new(key=self.key, mode=Blowfish.MODE_CBC, IV=self.iv).decrypt(ciphertext)