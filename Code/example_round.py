import TactileSensor as ts
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()

round=np.zeros((100,10))
i=0
while True:
    if i>=len(round):
        round=np.roll(round, -1,axis=0)
        round[-1]=B.getSensor(type_="round")
    else:
        round[i]=B.getSensor(type_="round")
    i+=1
    plt.cla()
    for j in range(len(round[0])):
        num=round[:,j].copy()
        #num=(num-np.min(num))/(np.max(num)-np.min(num))
        num=(num-np.mean(round,axis=1))/np.std(round,axis=1)
        plt.plot([k/5 for k in range(len(round))],num,label="sensor "+str(j+1))
    plt.legend(loc="lower left")
    plt.title("Filtered round sensor")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Analogue value")
    plt.pause(0.1)