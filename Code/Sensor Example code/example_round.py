import TactileSensor as ts
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import keyboard
matplotlib.use('TkAgg')

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()
num_=16

round=np.zeros((100,num_))
i=0
while True:
    if i>=len(round):
        round=np.roll(round, -1,axis=0)
        round[-1]=B.getSensor(type_="round",num=num_)
    else:
        round[i]=B.getSensor(type_="round",num=num_)
    i+=1
    plt.cla()
    window_size=5
    for j in range(len(round[0])):
        num=round[:,j].copy()
        #num=(num-np.min(num))/(np.max(num)-np.min(num))
        #num=(num-np.mean(round,axis=1))/np.std(round,axis=1)
        #num = np.convolve(num, np.ones(window_size) / window_size, mode='same')
        #plt.plot([k/5 for k in range(len(round))],num,label="sensor "+str(j+1))
        #plt.plot([k/5 for k in range(len(round))],np.average(round,axis=1),"--")
    plt.plot(round[:,-1],label="Vibration")
    #plt.plot(np.max(round,axis=1),label="sensor_max")
    plt.legend(loc="lower left")
    plt.title("Filtered round sensor")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Analogue value")
    plt.title(str(np.average(round[-1])))
    #plt.ylim([20000,25000])
    plt.pause(0.01)
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        break
