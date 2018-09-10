import psutil
import os

#get current memory usage
def mem(msg=False):
    pid = os.getpid()
    process = psutil.Process(pid)
    mem = process.memory_info()[0]/float(2**20)
    if msg:
        print('Mem usage: {0} MB'.format(mem))
    return mem

if __name__=='__main__':
    mem(msg=True)
