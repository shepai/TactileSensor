import controller
import sys
import numpy as np
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/TactileSensor/Code/')
import TactileSensor as ts

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()

input("Press enter once you have added your rig device")

exp=controller.experiment(B)
#exp.moveZ(1,1)
CM=1
ST=0.2
samples=10
data=np.zeros((samples,len(np.arange(0, CM, ST)),10))
weights=np.zeros((samples,len(np.arange(0, CM, ST))))

for i in range(samples):
    sensor,weight=exp.pressures(CM,ST)
    print(sensor.shape,weight.shape)
    data[i]=sensor
    weights[i]=weight
    exp.moveZ(1,1)

np.save("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/pressures/pressureVals")


print("Exiting...")
exp.moveZ(2,1)