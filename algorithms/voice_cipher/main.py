import time
import matplotlib.pyplot as plt

from fernet import FernetCryptor
from trivium import TriviumCryptor

if __name__ == '__main__':
    
    path_dir = '../../voice_files/'

    filename = [
        'audio.wav'
    ]

    algorithms = [
        'FERNET',
        'TRIVIUM'
    ]

    for algo in algorithms:
        print(algo, end='\n')

        # choose encryptor
        enc = None
        if(algo == 'FERNET'):
            enc = FernetCryptor()
        elif(algo == 'TRIVIUM'):
            enc = TriviumCryptor()

        encrypt_time = []
        decrypt_time = []
        
        for f in filename:
            with open(path_dir + f, 'rb') as fo:
                plaintext = fo.read()

            # encryption time
            ts = time.time()
            ciphertext = enc.encrypt(plaintext)
            te = time.time()
            enc_time = te - ts

            encrypt_time.append(enc_time)

            # decryption time
            ts = time.time()
            decrypttext = enc.decrypt(ciphertext)
            te = time.time()
            dec_time = te - ts

            decrypt_time.append(dec_time)

            # if decryption fails
            if(plaintext != decrypttext):
                print('Wrong Decryption')
                break

    #     # plot curve for each algorithm
    #     plt.plot(x, encrypt_time, label=algo)
    #     # plot curve for each algorithm
    #     plt.plot(x, decrypt_time, linestyle='dashed', label=algo)

    # # show plot
    # plt.legend()
    # plt.show()
    # print(end = '\n')