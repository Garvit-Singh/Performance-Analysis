# import binascii
# import sys
# import os
from collections import deque
from itertools import repeat

class Trivium:
    def __init__(self, key, iv):
        """in the beginning we need to transform the key as well as the IV.
        Afterwards we initialize the state."""
        self.state = None
        self.counter = 0
        self.key = key  # self._setLength(key)
        self.iv = iv  # self._setLength(iv)

        # Initialize state
        # len 100
        init_list = list(map(int, list(self.key)))
        init_list += list(repeat(0, 20))
        # len 84
        init_list += list(map(int, list(self.iv)))
        init_list += list(repeat(0, 4))
        # len 111
        init_list += list(repeat(0, 108))
        init_list += list([1, 1, 1])
        self.state = deque(init_list)

        # Do 4 full cycles, drop output
        for i in range(4*288):
            self._gen_keystream()

    def encrypt(self, message):
        """To be implemented"""
        pass

    def decrypt(self, cipher):
        """To be implemented"""
        pass

    def keystream(self):
        """output keystream
        only use this when you know what you are doing!!"""
        while self.counter < 2**64:
            self.counter += 1
            yield self._gen_keystream()

    def _setLength(self, input_data):
        """we cut off after 80 bits, alternatively we pad these with zeros."""
        input_data = "{0:080b}".format(input_data)
        if len(input_data) > 80:
            input_data = input_data[:(len(input_data)-81):-1]
        else:
            input_data = input_data[::-1]
        return input_data

    def _gen_keystream(self):
        """this method generates triviums keystream"""

        a_1 = self.state[90] & self.state[91]
        a_2 = self.state[181] & self.state[182]
        a_3 = self.state[292] & self.state[293]

        t_1 = self.state[65] ^ self.state[92]
        t_2 = self.state[168] ^ self.state[183]
        t_3 = self.state[249] ^ self.state[294]

        out = t_1 ^ t_2 ^ t_3

        s_1 = a_1 ^ self.state[177] ^ t_1
        s_2 = a_2 ^ self.state[270] ^ t_2
        s_3 = a_3 ^ self.state[68] ^ t_3

        self.state.rotate(1)

        self.state[0] = s_3
        self.state[100] = s_1
        self.state[184] = s_2

        return out

# # %%
# def get_bytes_from_file(filename):
#     return open(filename, "rb").read()

def _hex_to_bytes(s):
    _allbytes = dict([("%02X" % i, i) for i in range(256)])
    return [_allbytes[s[i:i+2].upper()] for i in range(0, len(s), 2)]

# def bits_to_hex(b):
#     return "".join(["%02X" % sum([b[i + j] << j for j in range(8)]) for i in range(0, len(b), 8)])

def hex_to_bits(s):
    return [(b >> i) & 1 for b in _hex_to_bytes(s) for i in range(8)]


def get_next_stream_byte(triv):
    next_key_bit = triv.keystream().__next__
    rtn = 0
    for j in range(8):
        rtn+=int(next_key_bit()) << j
    return rtn

class TriviumCryptor():
    def __init__(self):
        self.KEY = "0F62B5085BAE0154A7FA"
        self.KEY = hex_to_bits(self.KEY)[::-1]
        self.IV = "288FF65DC42B92F960C7"
        self.IV = hex_to_bits(self.IV)[::-1]
    
    def encrypt(self, message):
        self.triv = Trivium(self.KEY, self.IV)
        buffer = bytearray()
        for mybyte in message:
            newbyte = (mybyte ^ get_next_stream_byte(self.triv)) & 0xFF
            buffer.append(newbyte)
        return buffer

    def decrypt(self, cipher):
        self.triv = Trivium(self.KEY, self.IV)
        buffer = bytearray()
        for mybyte in cipher:
            newbyte = (mybyte ^ get_next_stream_byte(self.triv)) & 0xFF
            buffer.append(newbyte)
        return buffer
