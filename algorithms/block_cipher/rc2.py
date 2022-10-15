from Crypto import Random
from Crypto.Cipher import ARC2

class RC2Cryptor:
    def __init__(self, key):
        self.key = key
        self.iv = Random.new().read(ARC2.block_size)

    def getIV(self):
        return self.iv

    def encrypt(self, message):
        return ARC2.new(key=self.key, mode=ARC2.MODE_CBC, IV=self.iv).encrypt(message)

    def decrypt(self, ciphertext):
        return ARC2.new(key=self.key, mode=ARC2.MODE_CBC, IV=self.iv).decrypt(ciphertext)
