from cryptography.fernet import Fernet
 
key = Fernet.generate_key()
 
fernet = Fernet(key)
 
with open('key.key', 'wb') as filekey:
    filekey.write(key)
 
with open('key.key', 'rb') as filekey:
    key = filekey.read()
 
with open('audio.wav', 'rb') as file:
    orignal_file = file.read()
 
encrypted = fernet.encrypt(orignal_file)
 
with open('enc audio.wav', 'wb') as file:
    file.write(encrypted)
 
fernet = Fernet(key)
 
with open('enc audio.wav', 'rb') as file:
    encrypted_file = file.read()
 
decrypted = fernet.decrypt(encrypted_file)
 
with open('dec audio.wav', 'wb') as file:
    file.write(decrypted)