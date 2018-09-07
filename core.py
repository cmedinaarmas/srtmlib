#core.py

#mosaic
import glob, os
from collections import defaultdict
import numpy as np
import psutil
from time import time
import multiprocessing as mp



#tile
from struct import *

import array
#import os

#import numpy as np
#import time



class Mosaic:

    #initializer
    def __init__(self,src_dir):

        self.src_dir = src_dir
        self.coloring = 'grayscale'
        self.detected_files = defaultdict(list)

        self.lat_max = None
        self.lat_min = None
        self.lon_min = None
        self.lon_max = None
        self.coordinates = None
        self.map_char = u"\u2588"

        # file metadata
        self.v = None
        self.arc = None

        self.mosaic_files = []
        self.mosaic_found = {}

        self.pid = os.getpid()

    def split_bil(self,reference):
        hemisphere = reference[0]
        coordinate= int(reference[1:])
        if hemisphere in ['s','w']:
            coordinate *= -1
        return (coordinate)


    def build_bil_set(self,verbose=True):
        for lat in range(self.lat_min, self.lat_max+1):
            for lon in range(self.lon_min, self.lon_max+1):
                hem_lat=''
                hem_lon=''

                if lat < 0:
                    hem_lat = 's'
                else:
                    hem_lat = 'n'

                if lon < 0:
                    hem_lon = 'w'
                else:
                    hem_lon = 'e'

                filename = '{0}{1}_{2}{3:03}_{4}_{5}.bil'.format(hem_lat,abs(lat),hem_lon,abs(lon),self.arc,self.v)
                self.mosaic_files.append(filename)

        if(verbose):
            for f in self.mosaic_files:
                self.is_file(f)

        return None


    def read_dir(self):

        coordinates = []
        os.chdir(self.src_dir)

        print('Exploring {0}'.format(self.src_dir))

        for file_name in glob.glob("*.bil"):

            raw_name = file_name.split('_')
            raw_name[3] = raw_name[3].split('.')[0]

            lat = self.split_bil(raw_name[0])
            lon = self.split_bil(raw_name[1])

            self.detected_files[file_name] = [lat,lon,raw_name[2],raw_name[3]]
            coordinates.append((lat,lon))

        self.coordinates = np.array(coordinates)

        self.lat_max, self.lon_max = self.coordinates.max(axis=0)
        self.lat_min, self.lon_min = self.coordinates.min(axis=0)

        #missing validations
        self.arc = self.detected_files[next(iter(self.detected_files))][2]
        self.v   = self.detected_files[next(iter(self.detected_files))][3]
        return None


    #check if file exists
    def is_file(self,src_file):

        found = os.path.isfile(self.src_dir+src_file)
        self.mosaic_found[src_file]= found

        if(found):
            print('{0}  FOUND'.format(src_file))
        else:
            print('{0}  NOT FOUND'.format(src_file))

        return None

    #print the structure of found files
    def mosaic_print_structure(self):

        print('-------')
        for i,f in enumerate(self.mosaic_files):
            if(self.mosaic_found[f]):
                print(self.map_char,end='',flush=True)
            else:
                print(' ',end='',flush=True)

            if((i+1)%(abs(1+(self.lon_max-self.lon_min)))==0):
                print()

        print('-------')
        return None

    #get process pid
    def get_pid(self):

        return self.pid

    #get current memory usage
    def mem(self, msg=False):

        process = psutil.Process(self.pid)
        mem = process.memory_info()[0]/float(2**20)
        if msg:
            print('Mem usage: {0} MB'.format(mem))

        return mem

    def load_tiles(self):


        self.mem()
        tiles = []

        start = time()
        for index,item in enumerate(self.mosaic_found.items()):
            if item[1] == True:
                tiles.append(Tile(self.src_dir+item[0],int(self.arc[0]),index))

        for tile in tiles:
            tile.load_data()

        print('{0:.4f}'.format(time()-start))

        return None

    def load_tiles_mp(self):
        self.mem()

        N = len(self.mosaic_found.items())

        procs  = []
        tiles = []
        elements = 0
        start = time()
        # create processes
        for index,item in enumerate(self.mosaic_found.items()):
            if item[1] == True:
                tiles.append(Tile(self.src_dir+item[0],int(self.arc[0]),index))
                procs.append(mp.Process(target=tiles[elements].load_data))
                elements =+ 1
        # run processes
        for p in procs:
            p.start()

        # wait for execution
        for p in procs:
            p.join()

        print('{0:.4f}s'.format(time()-start))

        return None





class Tile:

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


    def read_bytes_LC(self, bytes_to_read):
        # DEPRECATED
        # ---------
        # read binary file as unsigned char type
        # using a list comprehension

        f = open(self.src_file, "rb")
        raw_bytes = [ unpack('B',f.read(1))[0] for byte in range(bytes_to_read) ]
        f.close()
        loaded_bytes =  np.asarray(raw_bytes)

        return loaded_bytes


    def read_bytes(self, bytes_to_read):
        # read binary file as unsigned char type
        # using an array.fromfile

        raw_bytes = array.array('B')

        f = open(self.src_file, "rb")
        raw_bytes.fromfile(f,bytes_to_read)
        f.close()
        loaded_bytes = np.asarray(raw_bytes,np.int64)

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
        # decode data
        heights = self.decode_hgt(self.read_bytes(samples_per_line*bytes_per_sample*lines), wrapped)
        # special height values handling
        # TODO
        # self.heights = np.clip( np.reshape(heights,(samples_per_line,lines)),0,max_val)

        self.heights = np.reshape(heights,(samples_per_line,lines))
