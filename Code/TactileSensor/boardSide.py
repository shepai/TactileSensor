import machine
import time
from Tactile_MP import *

foot=Foot([0,1,2,3],26,4)
# Define the control pins
def gather(low_pass=True,high_pass=True,alpha=0.2):
    foot.alpha=alpha
    data=foot.read()
    if low_pass:
        data=foot.low_pass
    elif low_pass:
        data=foot.high_pass
    print([float('{:f}'.format(data[i])) for i in range(len(data))])
    return data
