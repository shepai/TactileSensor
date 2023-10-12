import TactileSensor as ts
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


matplotlib.use('TkAgg')

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()

round=np.zeros((100,))
i=0
while True:
    t1=time.time()
    if i>=len(round):
        round=np.roll(round, -1,axis=0)
        round[-1]=B.ReadAnalog()
    else:
        round[i]=B.ReadAnalog()
    i+=1
    plt.cla()
    plt.plot([k/5 for k in range(len(round))],round,label="sensor ")
    plt.legend(loc="lower left")
    plt.title("Filtered round sensor")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Analogue value")
    #plt.ylim([20000,25000])
    plt.pause(0.1)
    #if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        #break