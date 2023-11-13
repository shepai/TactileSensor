import controller
import sys
import numpy as np

import time

B=controller.Sensor()
#get serial boards and connect to first one
B.autoConnect()

#input("Press enter once you have added your rig device")

exp=controller.experiment(B)
#exp.moveZ(1,-1)
steps=4
samples=100
data=np.zeros((samples,2,steps))
t1=time.time()
print(data.shape)
try:
    for i in range(samples):
        print("Complete:",round((i/samples)*100,1),"%","Time taken:",round((time.time()-t1)/60,1),"minutes")
        sensor=exp.direction(steps)
        data[i]=sensor
        np.save("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/pressures/speeds",data)
except KeyboardInterrupt:
    pass

print("Exiting...")
exp.control.unclick()