from Crypto import Random
from Crypto.Cipher import AES

class AESCryptor:
    def __init__(self, key):
        self.key = key
        self.iv = Random.new().read(AES.block_size)

    def getIV(self):
        return self.iv

    def encrypt(self, message):
        return AES.new(key=self.key, mode=AES.MODE_CBC, IV=self.iv).encrypt(message)

    def decrypt(self, ciphertext):
        return AES.new(key=self.key, mode=AES.MODE_CBC, IV=self.iv).decrypt(ciphertext)
