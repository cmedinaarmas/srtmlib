import time
import block as bl

data = 'data/everest/n27_e085_1arc_v3.bil'
b = bl.Block(data,1,0)

# b.load_data()
t1=time.time()
data=b.read_bytes(3601*3601*2)
t2 = time.time()
heights= b.decode_hgt(data,False)
t3 = time.time()
print('read', t2-t1)
print('decode', t3-t2)

print(data[:2])
print('dtype',data.dtype)
print(heights[0])
