import strmlib as st

data = '/home/cm/git/strmlib/data/everest/'

# create object
d = st.Strm(data)
d.mem()
print('PID: {0}'.format(d.get_pid()))

#read src folder
d.read_dir()

# validate existance of expected set
d.build_bil_set()
d.mosaic_print_structure()
d.load_blocks()
# load blocks to memory
d.mem()

