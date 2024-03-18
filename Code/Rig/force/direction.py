import controller
import sys
import numpy as np
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/TactileSensor/Code/')
import TactileSensor as ts
import time

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()

#input("Press enter once you have added your rig device")

exp=controller.experiment(B)
#exp.moveZ(1,-1)
trials=3
steps=4
samples=100
data=np.zeros((samples,trials,2,steps,10))
t1=time.time()
try:
    for i in range(samples):
        print("Complete:",round((i/samples)*100,1),"%","Time taken:",round((time.time()-t1)/60,1),"minutes")
        sensor=exp.direction(trials,steps)
        data[i]=sensor
        np.save("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/pressures/directionWithVibe",data)
except KeyboardInterrupt:
    pass

print("Exiting...")
exp.control.unclick()