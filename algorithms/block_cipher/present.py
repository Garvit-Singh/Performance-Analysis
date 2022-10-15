import binascii
import struct
import numpy as np

class Present:

        def __init__(self,key,rounds=32):
                """Create a PRESENT cipher object
                key:    the key as a 128-bit
                rounds: the number of rounds as an integer, 32 by default
                """
                self.rounds = rounds
                if len(key) * 8 == 128:
                        self.roundkeys = generateRoundkeys128(string2number(key),self.rounds)
                        self.roundkeys = np.array(self.roundkeys).astype(np.int64)
                else:
                        raise ValueError("Key must be a 128-bit")

        def encrypt(self,state):
                """Encrypt 1 block (8 bytes)

                Input:  numpy blocks of int64
                Output: ciphertext block as raw string
                """
                sb = np.vectorize(sBoxLayer)
                n2s = np.vectorize(number2string_N)
                
                for i in range (self.rounds-1):
                        state = np.bitwise_xor(state,self.roundkeys[i])
                        state = sb(state)
                        state = pLayer(state)
                cipher = np.bitwise_xor(state,self.roundkeys[-1])
                return n2s(cipher,8)

        def decrypt(self,state):
                """Decrypt 1 block (8 bytes)

                Input:  ciphertext block as raw string
                Output: plaintext block as raw string
                """
                sb = np.vectorize(sBoxLayer_dec)
                n2s = np.vectorize(number2string_N)

                for i in range (self.rounds-1):
                        state = np.bitwise_xor(state,self.roundkeys[-i-1])
                        state = pLayer_dec(state)
                        state = sb(state)
                decipher = np.bitwise_xor(state,self.roundkeys[0])
                return n2s(decipher,8)

        def get_block_size(self):
                return 8

#        0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
Sbox= [0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2]
Sbox_inv = [Sbox.index(x) for x in range(16)]
PBox = [0,16,32,48,1,17,33,49,2,18,34,50,3,19,35,51,
        4,20,36,52,5,21,37,53,6,22,38,54,7,23,39,55,
        8,24,40,56,9,25,41,57,10,26,42,58,11,27,43,59,
        12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]
PBox_inv = [PBox.index(x) for x in range(64)]

def generateRoundkeys128(key,rounds):
        """Generate the roundkeys for a 128-bit key

        Input:
                key:    the key as a 128-bit integer
                rounds: the number of rounds as an integer
        Output: list of 64-bit roundkeys as integers"""
        roundkeys = []
        for i in range(1,rounds+1): # (K1 ... K32)
                # rawkey: used in comments to show what happens at bitlevel
                roundkeys.append(key >>64)
                #1. Shift
                key = ((key & (2**67-1)) << 61) + (key >> 67)
                #2. SBox
                key = (Sbox[key >> 124] << 124)+(Sbox[(key >> 120) & 0xF] << 120)+(key & (2**120-1))
                #3. Salt
                #rawKey[62:67] ^ i
                key ^= i << 62
        return roundkeys

def addRoundKey(state,roundkey):
        return state ^ roundkey

def sBoxLayer(state):
        """SBox function for encryption

        Input:  64-bit integer
        Output: 64-bit integer"""

        output = 0
        for i in range(16):
                output += np.left_shift((Sbox[np.bitwise_and(( np.right_shift(state, (i*4))) , 0xF)] ), (i*4))
        return output

def sBoxLayer_dec(state):
        """Inverse SBox function for decryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in range(16):
                output += np.left_shift(Sbox_inv[np.bitwise_and((np.right_shift( state, (i*4))), 0xF)], (i*4))
        return output

def pLayer(state):
        """Permutation layer for encryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in range(64):
                output += np.left_shift((np.bitwise_and((np.right_shift(state, i)),  0x01)), PBox[i])
        return output

def pLayer_dec(state):
        """Permutation layer for decryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in range(64):
                output += np.left_shift((np.bitwise_and((np.right_shift(state, i)),  0x01)), PBox_inv[i])
        return output

def string2number(i):
    """ Convert a string to a number

    Input: string (big-endian)
    Output: long or integer
    """
   
    val = int.from_bytes(i, byteorder='little')
   
    return val


def number2string_N(i, N=8):
    """Convert a number to a string of fixed size

    i: long or integer
    N: length of string
    Output: string (big-endian)
    """
    bytestr = struct.pack('q', i)
    return bytestr

def string2number_N(s, N=8):
    s = struct.unpack('Q', s)
    s = np.reshape(s, -1)
    return s

class PresentCryptor:
    def __init__(self, key):
        self.key = key
        self.cipher = Present(key)

    def encrypt(self, message):
        n = 8
        block_ciphers = [message[i:i+n] for i in range(0, len(message), n)]
        block_ciphers = np.array(block_ciphers)
        s2n = np.vectorize(string2number)
        block_ciphers = s2n(block_ciphers)
        return b"".join(self.cipher.encrypt(block_ciphers))

    def decrypt(self, ciphertext):
        n = 8
        plaintext = [ciphertext[i:i+n] for i in range(0, len(ciphertext), n)]
        plaintext = np.array(plaintext).reshape(-1)
        s2n = np.vectorize(string2number_N)
        plaintext = s2n(plaintext)
        plaintext = np.array(plaintext).reshape(-1)
        plaintext = self.cipher.decrypt(plaintext)
        return b"".join(plaintext)

if __name__ == "__main__":
    k = b"this mai kung fu"
    message = b"abcdefghhgfedcba"
    prs = PresentCryptor(k)

    ciphertext = prs.encrypt(message)
    print(ciphertext)

    plaintext = prs.decrypt(ciphertext)
    print(plaintext)