import controller
import sys
import numpy as np
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/TactileSensor/Code/')
import TactileSensor as ts
import time

B=controller.Sensor()
#get serial boards and connect to first one
B.autoConnect()

#input("Press enter once you have added your rig device")

exp=controller.experiment(B)
exp.moveZ(0.1,-1)
CM=1
ST=0.1
samples=100
data=np.zeros((samples,len(np.arange(0, CM, ST)),1))
t1=time.time()
for i in range(samples):
    print("Complete:",round((i/samples)*100,1),"%","Time taken:",round((time.time()-t1)/60,1),"minutes")
    sensor=exp.pressures(CM,ST)
    data[i]=sensor
    exp.moveZ(1,1)

    np.save("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/pressures/vibePressVals_1",data)
    #np.save("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/pressures/pressureWeights_3",weights)

print("Exiting...")
exp.moveZ(2,1)