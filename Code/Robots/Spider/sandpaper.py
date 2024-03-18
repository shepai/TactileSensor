from control import Board
import numpy as np
import time

b=Board() #create connection to controller
winpath="C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Robots/Spider/boardSide.py"
linpath="/its/home/drs25/Documents/GitHub/TactileSensor/Code/Robots/Spider/boardSide.py"
b.autoConnect(winpath) #run servo controller



def calibrate(num=100):
    image=b.getSensor(type_="round")
    reduction_matrix=np.zeros_like(image)
    for i in range(num):
        reduction_matrix+=b.getSensor(type_="round")
    return reduction_matrix/num

#rm=calibrate()
print("Begin")

data={"run":[],"timestep":[],"servo1":[],"servo2":[],"servo3":[],"p1":[],"p2":[],"p3":[],"p4":[],"p5":[],"p6":[],"p7":[],"p8":[],"p9":[],"p10":[],"p11":[],"p12":[],"p13":[],"p14":[],"p15":[],"p16":[]}

filename="carpet_1.csv" #sandpaper_C180_3
path_l="/its/home/drs25/Documents/GitHub/TactileSensor/Code/Data collection/robot/spiderData/"
path_w="C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/robot/spiderData/"
path=path_w
def run(j=0,dt=0.01): #move through making recordings
    #future will need a move till placed
    data=[]
    t=time.time()
    for i in range(35,145):
        b.moveServo(7,i)
        time.sleep(dt)
        passed=time.time()-t
        data.append([j,passed,b.getServo(8),b.getServo(7),b.getServo(6)]+list(b.getSensor(type_="round")))
    b.moveServo(6,105)
    time.sleep(1)
    return data

def resetTrial(): #reset to initial position
    b.moveServo(8,175)
    b.moveServo(7,35)
    time.sleep(1)
    b.moveServo(6,80)


num_trials=30
dt=0.001
file=open(path+filename,'w')
header=""
for name in list(data.keys()):
    header+=name+","
file.write(header[:-1]+"\n")
for i in range(num_trials): #loop through 
    print("Trial",i+1)
    d=run(i,dt) #move through time
    resetTrial() #reset to start position
    #write data in csv format
    for j in range(len(d)):
        str_=""
        for k in range(len(d[j])):
            str_+=str(d[j][k])+","
        file.write(str_[:-2]+"\n") #write in csv format


file.close()