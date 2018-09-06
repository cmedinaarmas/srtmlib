import block as bl

data = 'data/everest/n27_e085_1arc_v3.bil'
b = bl.Block(data,1,0)
# b.load_data()
data=b.read_bytes(3601*3601*2)
heights= b.decode_hgt(data,False)
heights_w= b.decode_hgt(data,True)
#
# h = b.heights
# print(b.src_file)
# print(h.shape)
# print(b.decoded[0])
print(data[:2])
print(heights[0])
print(heights_w[0])
