import TactileSensor as ts
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

B=ts.Board()
#get serial boards and connect to first one
COM=""
while COM=="":
    try:
        res=B.serial_ports()
        print("ports:",res)
        B.connect(res[0])
        B.runFile("/its/home/drs25/Documents/GitHub/TactileSensor/Code/TactileSensor/boardSide.py") #C:/Users/dexte/OneDrive/Documents/GitHub/TactileSensor/Code/TactileSensor/boardSide.py
        COM=res[0]
    except IndexError:
        time.sleep(1)

round=np.zeros((100,10))
for i in range(100):
    round[i]=B.getSensor(type_="round")
    time.sleep(0.1)

for i in range(len(round[0])):
    round[:,i]=(round[:,i]-np.min(round[:,i]))/(np.max(round[:,i])-np.min(round[:,i]))#"""

for i in range(len(round[0])):
    plt.plot([j/5 for j in range(len(round))],round[:,i],label="sensor "+str(i+1))
#plt.plot([i/10 for i in range(len(unfiltered))],unfiltered,label="Un-filtered")
plt.legend(loc="lower right")
plt.title("Filtered round sensor")
plt.xlabel("Time (seconds)")
plt.ylabel("Analogue value")
plt.show()