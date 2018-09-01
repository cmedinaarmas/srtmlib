import glob, os
from collections import defaultdict
import numpy as np
import psutil

from tqdm import tqdm

import block as bl

class Strm:

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
        
        for file_name in tqdm(glob.glob("*.bil")):

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

    def load_blocks(self):
        self.mem()
        blocks = []
        
        print('Id  Load    Decode  Allocated Mem')
        for index,item in enumerate(self.mosaic_found.items()):
            if item[1] == True:
                blocks.append(bl.Block(self.src_dir+item[0],int(self.arc[0]),index))
        
        for block in blocks:
            block.load_data()
            
            print('{0:02d}  {1:.4f}s {2:.4f}s {3:.2f}MB'.format(block.index, block.load_t,block.decode_t,self.mem()))
        return None

