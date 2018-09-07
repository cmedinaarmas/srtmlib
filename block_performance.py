# benchmark performance of block class



import time
import block as bl

data = 'data/everest/n27_e085_1arc_v3.bil'
b = bl.Block(data,1,0)

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

# dell
# read_bytes 0.08397531509399414s
# decode_hgt 4.739003419876099s
# load_data  4.788928031921387s
# latency    -0.034050703048706055s

