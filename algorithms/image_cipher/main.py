import time
import cv2
import matplotlib.pyplot as plt

from arnold_map import ArnoldCryptor

if __name__ == '__main__':
    
    path_dir = '../../image_files/'

    filename = [
    ]

    algorithms = [
        'ARNOLD',
        'CHAOTIC'
    ]

    for algo in algorithms:
        print(algo, end='\n')

        # choose encryptor
        enc = None
        if(algo == 'ARNOLD'):
            enc = ArnoldCryptor(key=20)
        elif(algo == 'CHAOTIC'):
            enc = None

        encrypt_time = []
        decrypt_time = []
        
        for f in filename:
            plain_img = cv2.imread(f)

            # encryption time
            ts = time.time()
            cipher_img = enc.encrypt(plain_img)
            te = time.time()
            enc_time = te - ts

            encrypt_time.append(enc_time)

            # decryption time
            ts = time.time()
            decrypt_img = enc.decrypt(cipher_img)
            te = time.time()
            dec_time = te - ts

            decrypt_time.append(dec_time)

            # if decryption fails
            if(plain_img != decrypt_img):
                print('Wrong Decryption')
                # cv2.imwrite(f.split('.')[0] + "_ArnoldcatEnc.png", decryptimg)
                break

    #     # plot curve for each algorithm
    #     plt.plot(x, encrypt_time, label=algo)
    #     # plot curve for each algorithm
    #     plt.plot(x, decrypt_time, linestyle='dashed', label=algo)

    # # show plot
    # plt.legend()
    # plt.show()
    # print(end = '\n')