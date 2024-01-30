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

def run(dt=0.01):
    #future will need a move till placed
    data=[]
    t=time.time()
    for i in range(0,180):
        b.moveServo(7,i)
        time.sleep(dt)
        passed=time.time()
        data.append([passed,b.getServo(8),b.getServo(7),b.getServo(6)]+list(b.getSensor(type_="round")))
    return np.array(data)

def resetTrial():
    b.moveServo(8,150)
    b.moveServo(7,0)
    b.moveServo(6,55)


run()
resetTrial()