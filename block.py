from struct import *
import numpy as np
import time

class Block:

    #initializer
    def __init__(self, src_file, arc, index):
        self.src_file = src_file
        self.arc = arc
        self.index = index
        self.heights = None

        self.shape = None
        if arc == 1:
            self.shape = (3601,3601)
        elif arc == 3:
            self.shape = (1201,1201)
        else:
            self.shape = (0,0)


    def read_bytes(self, bytes_to_read):
        # read binary file as unsigned char type
        # return np array

        f = open(self.src_file, "rb")
        raw_bytes = [ unpack('B',f.read(1))[0] for byte in range(bytes_to_read) ]
        f.close()
        loaded_bytes =  np.asarray(raw_bytes)

        return loaded_bytes


    def decode_hgt(self, src_bytes, wrapped):

        # decode height stored in big endian format
        size = src_bytes.shape[0]
        heights = []

        if not wrapped:
            heights = [ ((src_bytes[i+1]<<8) + src_bytes[i]) for i in range(0, size, 2) ]
        else:
            heights = [ src_bytes[i] for i in range(0, size, 2) ]
        decoded = np.asarray(heights)

        return decoded


    def load_data(self, wrapped=False):

        samples_per_line, lines = self.shape
        bytes_per_sample = 2
        max_val = 8480

        # read from file
        data = self.read_bytes(samples_per_line*bytes_per_sample*lines)
        # decode data
        heights = self.decode_hgt(data, wrapped)
        self.heights = np.reshape(heights,(samples_per_line,lines))
        #self.heights = np.clip( np.reshape(heights,(samples_per_line,lines)),0,max_val)
