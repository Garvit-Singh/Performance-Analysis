from Crypto import Random
from Crypto.Cipher import DES3

class DES3Cryptor:
    def __init__(self, key):
        self.key = key
        self.iv = Random.new().read(DES3.block_size)

    def getIV(self):
        return self.iv
        
    def encrypt(self, plaintext):
        return DES3.new(key=self.key, mode=DES3.MODE_CBC, IV=self.iv).encrypt(plaintext)
    
    def decrypt(self, ciphertext):
        return DES3.new(key=self.key, mode=DES3.MODE_CBC, IV=self.iv).decrypt(ciphertext)