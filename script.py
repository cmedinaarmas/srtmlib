import strmlib as st
#data  ='/home/cm/Documents/strmlib/data/everest'
data = '/home/cm/git/strmlib/data/guadaloupe/'

# create object
d = st.Strm(data)

d.mem(msg=True)
print('PID: {0}'.format(d.get_pid()))

#read src folder
d.read_dir()

# validate existance of expected set
d.build_bil_set()
d.mosaic_print_structure()
d.load_blocks_mp()

#d.load_blocks()

d.mem(msg=True)

