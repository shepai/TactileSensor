import controller
import sys
import numpy as np
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/TactileSensor/Code/')
import TactileSensor as ts
import time

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()

input("Press enter once you have added your rig device")

exp=controller.experiment(B)
exp.moveX(10,1)
trials=50
steps=2
samples=1
data=np.zeros((samples,trials,steps))
t1=time.time()
for i in range(samples):
    print("Complete:",round((i/samples)*100,1),"%","Time taken:",round((time.time()-t1)/60,1),"minutes")
    sensor=exp.direction(trials,steps)
    data[i]=sensor
    np.save("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/pressures/directionVals_2",data)

print("Exiting...")
exp.moveZ(2,1)