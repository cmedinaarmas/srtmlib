# benchmark performance of tile class
# -------------------------------------
# dell
# read_bytes 0.08397531509399414s
# decode_hgt 4.739003419876099s
# load_data  4.788928031921387s
# latency    -0.034050703048706055s

# pc
# read_bytes 0.09253764152526855s
# decode_hgt 4.923607587814331s
# load_data  5.001503944396973s
# latency    -0.014641284942626953s
# np array dtype int64


import time
import core

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

if __name__ == '__main__':
    data = 'data/everest/n27_e085_1arc_v3.bil'
    src_file = data
    perf_tile(src_file)
