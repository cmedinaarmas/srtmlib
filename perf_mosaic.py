import time
import mosaic as m
# dell
#data  ='/home/cm/Documents/cm/srtm/data/everest/'

# cx
data = '/home/cm/git/srtmlib/data/everest/'

# create object
d = m.Mosaic(data)

d.mem(msg=True)
print('PID: {0}'.format(d.get_pid()))

#read src folder
d.read_dir()

# validate existance of expected set
d.build_bil_set()
d.mosaic_print_structure()

t1 = time.time()
d.load_tiles_mp()
#d.load_tiles_()
t2 = time.time()

print('{0}'.format(t2-t1))


d.mem(msg=True)
# pc
# 13.7890s
