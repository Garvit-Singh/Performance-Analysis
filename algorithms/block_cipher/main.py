import time
import matplotlib.pyplot as plt

from aes import *
from rc2 import *
from des3 import *
from blowfish import *
from present import *

if __name__ == '__main__':
    
    path_dir = '../../txt_files/'

    filename = [
        '1KB.txt',
        '2KB.txt',
        '4KB.txt',
        '8KB.txt',
        '16KB.txt',
        '32KB.txt',
        '64KB.txt',
        '128KB.txt',
        '256KB.txt',
        '512KB.txt',
        '1MB.txt',
        '2MB.txt',
        '4MB.txt',
        '16MB.txt',
        '32MB.txt'
    ]

    algorithms = [
        'AES',
        '3DES', 
        'BLOWFISH',
        'ARC2',
        'PRESENT'
    ]

    keys = [
        b'gVkYp3s6v9y$B&E)',
        # b'kXn2r5u8z%C*F-JaNdRgUkXp', 
        # 'n2r5u8x/A?D(G+KbPeShVmYq3s6v9y$B'
    ]

    x = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]

    # rows fill
    for k in keys:

        print('Key Length : ', len(k)*8)

        for algo in algorithms:
            print(algo, end='\n')

            # choose encryptor
            enc = None
            if(algo == 'AES'):
                enc = AESCryptor(k)
            elif(algo == '3DES'):
                enc = DES3Cryptor(k)
            elif(algo == 'BLOWFISH'):
                enc = BlowfishCryptor(k)
            elif(algo == 'ARC2'):
                enc = RC2Cryptor(k)
            elif(algo == 'PRESENT'):
                enc = PresentCryptor(k)

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

            # plot curve for each algorithm
            plt.plot(x, encrypt_time, label=algo)
            # plot curve for each algorithm
            plt.plot(x, decrypt_time, linestyle='dashed', label=algo)

        # show plot
        plt.legend()
        plt.show()
        print(end = '\n')