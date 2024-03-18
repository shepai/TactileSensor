import TactileSensor as ts
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()

max_time=10
dt=0.03
t1=time.time()
array=[]
T=0
print("Recording")
while T<max_time:
    T+=dt
    array.append(B.getSensor(type_="round"))

array=np.array(array)
np.save("C:/Users/dexte/Documents/GitHub/TactileSensor/Assets/Recorded_data/north-west",array)
print(time.time()-t1,"Seconds")