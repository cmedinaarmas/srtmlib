#core.py
# Class
#   - Mosaic
#   - Tile

# dependencies
 
# mosaic
import glob, os
from collections import defaultdict
import numpy as np
import multiprocessing as mp

# tile
import array


# class definitions

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
        self.tile_positions = {}

        self.tile_size = 0

        #tiles
        self.tiles = []
        self.heighs = None

    def split_bil(self,reference):
        hemisphere = reference[0]
        coordinate= int(reference[1:])
        if hemisphere in ['s','w']:
            coordinate *= -1
        return (coordinate)


    def build_bil_set(self,verbose=True):
        for i,lat in enumerate(range(self.lat_min, self.lat_max+1)):
            for j,lon in enumerate(range(self.lon_min, self.lon_max+1)):
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
                self.tile_positions[filename] = [i,j]
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
        for i, f in enumerate(self.mosaic_files):
            if(self.mosaic_found[f]):
                print(self.map_char,end='',flush=True)
            else:
                print(' ',end='',flush=True)
            
            if((i+1)%(abs(1+(self.lon_max-self.lon_min)))==0):
                print()

        print('-------')
        return None


    #DEPRECATED
    def load_tiles(self):

        tiles = []

        for index, item in enumerate(self.mosaic_found.items()):
            if item[1] == True:
                tiles.append(Tile(self.src_dir+item[0],int(self.arc[0]),index))

        for tile in tiles:
            tile.load_data()

        return None


    def load_tiles_mp(self):

        N = len(self.mosaic_found.items())

        procs  = []
        #tiles = []
        elements = 0

        # create processes
        for item in self.mosaic_found.items():
            if item[1] == True:
                pos = self.tile_positions[item[0]]

                self.tiles.append(Tile(self.src_dir+item[0],int(self.arc[0]),pos[0],pos[1]))
                procs.append(mp.Process(target=self.tiles[elements].load_data))
                elements =+ 1
        # run processes
        for p in procs:
            p.start()

        # wait for execution
        for p in procs:
            p.join()

        # store heights
        self.tile_size = self.tiles[0].shape[0]
        
        return None

    # 
    def merge_tiles(self):
        # compute size of mosaic in tiles
        c = 1 + self.lon_max - self.lon_min
        r = 1 + self.lat_max - self.lat_min

        print('c={0},r={1}'.format(c,r))
        # number of pixels
        cols = c * (self.tile_size - 1)
        rows = r * (self.tile_size - 1)
        print('cols={0},rows={1}'.format(cols,rows))
        # number of pixels
        self.data = np.empty((rows,cols),dtype=np.int64)
        print(self.data.shape)
        
        for tile in self.tiles:
            self.add_tile(tile, self.tile_size-1)
        pass

    # add a tile to the mosaic
    def add_tile(self, tile, sz):
        r = tile.i * sz
        c = tile.j * sz
        
        self.data[r:(r+sz),c:(c+sz)] = tile.heights
        pass

class Tile:

    #initializer
    def __init__(self, src_file, arc, i, j):
        self.src_file = src_file
        self.arc = arc
        #self.index = index
        self.heights = None

        # mosaic coordinates
        self.i = i
        self.j = j

        self.shape = None
        if arc == 1:
            self.shape = (3601,3601)
        elif arc == 3:
            self.shape = (1201,1201)
        else:
            self.shape = (0,0)


    def read_bytes(self, bytes_to_read):
        # read binary file as unsigned char type
        # return 1D np.array

        raw_bytes = array.array('B')

        f = open(self.src_file, "rb")
        raw_bytes.fromfile(f,bytes_to_read)
        f.close()
        loaded_bytes = np.asarray(raw_bytes,np.int64)

        return loaded_bytes

    def decode_hgt(self, src_bytes, wrapped):

        # split array into high and low bytes
        low_b  = src_bytes[::2]
        high_b = src_bytes[1::2]
        heights = None

        if not wrapped:
            heights = np.left_shift(high_b,8) + low_b
        else:
            heights = low_b

        return heights


    def load_data(self, wrapped=False):

        samples_per_line, lines = self.shape
        bytes_per_sample = 2

        heights = self.decode_hgt(self.read_bytes(samples_per_line*bytes_per_sample*lines), wrapped)

        # special height values handling
        # TO DO
        # max_val = 8480
        # self.heights = np.clip( np.reshape(heights,(samples_per_line,lines)),0,max_val)

        self.heights = np.reshape(heights,(samples_per_line,lines))
