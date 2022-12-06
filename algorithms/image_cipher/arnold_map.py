import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

def ArnoldCatTransform(img, num):
    rows, cols, ch = img.shape
    n = rows
    img_arnold = np.zeros([rows, cols, ch])
    for x in range(0, rows):
        for y in range(0, cols):
            img_arnold[x][y] = img[(x+y)%n][(x+2*y)%n]  
    return img_arnold 
 
def ArnoldCatEncryption(img, key=20):
    for i in range (0,key):
        img = ArnoldCatTransform(img, i)
    return img
 
def ArnoldCatDecryption(img, key):
    rows, cols, ch = img.shape
    dimension = rows
    decrypt_it = dimension
    if (dimension%2==0) and 5**int(round(math.log(dimension/2,5))) == int(dimension/2):
        decrypt_it = 3*dimension
    elif 5**int(round(math.log(dimension,5))) == int(dimension):
        decrypt_it = 2*dimension
    elif (dimension%6==0) and  5**int(round(math.log(dimension/6,5))) == int(dimension/6):
        decrypt_it = 2*dimension
    else:
        decrypt_it = int(12*dimension/7)
    for i in range(key,decrypt_it):
        img = ArnoldCatTransform(img, i)
    return img

class ArnoldCryptor():
    def __init__(self, key):
        self.key = key 

    def encrypt(self, img):
        return ArnoldCatEncryption(img, self.key)

    def decrypt(self, img):
        return ArnoldCatDecryption(img, self.key)