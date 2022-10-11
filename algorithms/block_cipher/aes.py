from Crypto import Random
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import os
import os.path
import time
class AESCrypter:
    def __init__(self, key):
        self.key = key
    
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name, remove_file=False):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        if remove_file:
            os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name, remove_file=False):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4] + ".dec", 'wb') as fo:
            fo.write(dec)
        if remove_file:
            os.remove(file_name)

if __name__ == "__main__":
    key = get_random_bytes(16) 
    enc = AESCrypter(key)
    enc.encrypt_file("README")
    enc.decrypt_file("README.enc")
    clear = lambda: os.system('cls')