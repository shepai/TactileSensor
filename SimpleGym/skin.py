import numpy as np
import env
import cv2


class sensor:
    """
    Sensor class that also holds the environment. The sensor can move around the bounds of the environment
    """
    def __init__(self,numSensorAxis=5):
        self.env = env.generateWorld(200)
        self.sensorGrid=np.zeros((numSensorAxis*5,numSensorAxis*5))
        self.axis=self.sensorGrid.shape
        self.x=0
        self.y=0
        self.num=numSensorAxis
    def getImage(self):
        #gather the cut out image from the area
        cutOut=self.env[self.y:self.axis[0]+self.y,self.x:self.axis[1]+self.x]
        im=cv2.resize(cutOut,(self.num,self.num),interpolation=cv2.INTER_AREA) #resize to robot view
        y=np.sum(im,axis=0)
        x=np.sum(im,axis=1)
        grid=np.zeros((self.num,self.num)).astype(float)
        for i in range(self.num):
            grid[i]=float(x[i])
        for i in range(self.num):
            grid[:,i]+=float(y[i])
        z=env.sigmoid(grid)
        return z
    def move(self,vector):
        #move the sensor by the vector, but not out of bounds of environment
        if self.x+vector[1]<len(self.env) and self.x+vector[1]>0: 
            self.x+=vector[1]
        if self.y+vector[0]<len(self.env) and self.y+vector[0]>0: 
            self.y+=vector[0]
    def changeEnv(self,newEnv):
        self.env=newEnv



