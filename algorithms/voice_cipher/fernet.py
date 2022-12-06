from cryptography.fernet import Fernet

class FernetCryptor():
    def __init__(self):
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        
    def encrypt(self, message):
        return self.fernet.encrypt(message)

    def decrypt(self, ciphertext):
        return self.fernet.decrypt(ciphertext)