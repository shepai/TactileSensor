from control import Board
import numpy as np
import time

b=Board() #create connection to controller
b.autoConnect("/its/home/drs25/Documents/GitHub/TactileSensor/Code/Robots/Spider/boardSide.py") #run servo controller



def calibrate(num=100):
    image=b.getSensor(type_="round")
    reduction_matrix=np.zeros_like(image)
    for i in range(num):
        reduction_matrix+=b.getSensor(type_="round")
    return reduction_matrix/num

#rm=calibrate()
print("Begin")

data={"timestep":[],"servo1":[],"servo2":[],"servo3":[],"p1":[],"p2":[],"p3":[],"p4":[],"p5":[],"p6":[],"p7":[],"p8":[],"p9":[],"p10":[],"p11":[],"p12":[],"p13":[],"p14":[],"p15":[],"p16":[],"vibration":[]}

filename="test.csv"
path="/its/home/drs25/Documents/GitHub/TactileSensor/Code/Data collection/robot/spiderData/"

def run(dt=0.01): #move through making recordings
    #future will need a move till placed
    data=[]
    t=time.time()
    for i in range(10,170):
        b.moveServo(7,i)
        time.sleep(dt)
        passed=time.time()-t
        data.append([passed,b.getServo(8),b.getServo(7),b.getServo(6)]+list(b.getSensor(type_="round")))
    b.moveServo(6,105)
    time.sleep(1)
    return data

def resetTrial(): #reset to initial position
    b.moveServo(8,150)
    b.moveServo(7,10)
    time.sleep(1)
    b.moveServo(6,55)


num_trials=2
dt=0.001
file=open(path+filename,'w')
header=""
for name in list(data.keys()):
    header+=name+","
file.write(header[:-2]+"\n")
for i in range(num_trials): #loop through 
    print("Trial",i+1)
    d=run(dt) #move through time
    resetTrial() #reset to start position
    #write data in csv format
    for j in range(len(d)):
        str_=""
        for k in range(len(d[j])):
            print(d[j][k])
            str_+=str(d[j][k])+","
        file.write(str_[:-2]+"\n") #write in csv format


