import block as bl

data = 'data/everest/n27_e085_1arc_v3.bil'
b = bl.Block(data,1,0)
b.load_data()
h = b.heights
print(b.src_file)
print(h.shape)
