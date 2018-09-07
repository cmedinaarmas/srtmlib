import time
import srtmlib as st
#dell
data  ='/home/cm/Documents/cm/srtm/data/everest/'
#data = '/home/cm/git/srtmlib/data/guadaloupe/'

# create object
d = st.Srtm(data)

d.mem(msg=True)
print('PID: {0}'.format(d.get_pid()))

#read src folder
d.read_dir()

# validate existance of expected set
d.build_bil_set()
d.mosaic_print_structure()

t1 = time.time()
#d.load_blocks_mp()
d.load_blocks()
t2 = time.time()

print('{0}'.format(t2-t1))
#d.load_blocks()

d.mem(msg=True)
