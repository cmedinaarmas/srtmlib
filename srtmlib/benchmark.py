import time
import core
import sys


def perf_mosaic(data):

    d = core.Mosaic(data)
    d.read_dir()
    d.build_bil_set()
    d.mosaic_print_structure()

    t1 = time.time()
    d.load_tiles_mp()
    t2 = time.time()
    print('{0}'.format(t2-t1))

    return None

def perf_tile(src_file):

    b = core.Tile(src_file,1,0)

    t1=time.time()
    data=b.read_bytes(3601*3601*2)
    t2 = time.time()
    heights= b.decode_hgt(data,False)
    t3 = time.time()
    b.load_data()
    t4 = time.time()

    read_t = t2-t1
    decode_t = t3-t2
    load_data_t = t4-t3

    latency_t = load_data_t - (read_t+decode_t)

    print('read_bytes {0}s'.format(read_t))
    print('decode_hgt {0}s'.format(decode_t))
    print('load_data  {0}s'.format(load_data_t))
    print('latency    {0}s'.format(latency_t))
    print('np array dtype {0}'.format(data.dtype))


if(__name__=='__main__'):

    help_msg = """
SRTMLIB benchmark tool

SYNOPSIS
    benchmark.py [option] [src_path | src_file]

DESCRIPTION
    t  Tile performance test
    m  Mosaic performance test
"""

    if len(sys.argv) == 2:
        option = sys.argv[1]
        if option == 'h':
            print(help_msg)
        else:
            print('Unkown option: {0}'.format(option))

    elif len(sys.argv) == 3:
        option = sys.argv[1]
        src = sys.argv[2]

        if option == 'm':
            #src_path='/home/cm/Documents/cm/srtm/srtmlib/data/everest/' #dell
            #src = '/home/cm/git/srtmlib/data/everest/' #cx
            perf_mosaic(src)

        elif option == 't':
            #data = 'data/everest/n27_e085_1arc_v3.bil'
            perf_tile(src)

        else:
            print('Unkown option: {0}'.format(option))
    else:
        print('Not enough parameters')
# pc
# 13.7890s
