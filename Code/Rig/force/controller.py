
from mpremote import pyboard
import serial, time
import sys
import glob
import numpy as np
import pickle 


class Board:
    def __init__(self):
        self.COM=None
        self.VALID_CHANNELS=[i for i in range(10)]
    def connect(self,com):
        """
        Connect to a com given
        @param com of serial port
        @param fileToRun is the file that executes on board to allow hardware interfacing
        """
        self.COM=pyboard.Pyboard(com) #connect to board
        self.COM.enter_raw_repl() #open for commands
        print("Successfully connected")
    def runFile(self,fileToRun='mOTRO CONTROL.py'):
        """
        runFile allows the user to send a local file to the device and run it
        @param fileToRun is the file that will be locally installed
        """
        if self.COM==None:
            raise OSError("Connect to device before running file")
        self.COM.execfile(fileToRun) #run the file controlling the sensors
    def serial_ports(self):
        """
        Read the all ports that are open for serial communication
        @returns array of COMS avaliable
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform') #if the OS is not one of the main

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    def autoConnect(self,file="C:/Users/dexte/Documents/GitHub/TactileSensor/Code/TactileSensor/boardSide.py"):
            COM=""
            while COM=="":
                try:
                    res=self.serial_ports()
                    print("ports:",res)
                    self.connect(res[0])
                    self.runFile(file) #C:/Users/dexte/OneDrive/Documents/GitHub/TactileSensor/Code/TactileSensor/boardSide.py
                    COM=res[0]
                except IndexError:
                    time.sleep(1)
    def moveX(self,num):
        self.COM.exec_raw_no_follow('b.moveX('+str(num)+')')#.decode("utf-8").replace("/r/n","")
    def moveZ(self,num,override=False):
        self.COM.exec_raw_no_follow('b.moveZ('+str(num)+',overide='+str(override)+')')#.decode("utf-8").replace("/r/n","")
    def setSpeed(self,speed):
        self.COM.exec_raw_no_follow('b.speed='+str(speed))#.decode("utf-8").replace("/r/n","")
    def close(self):
        self.COM.close()
    def getWeight(self):
        return float(self.COM.exec('get_pressure()').decode("utf-8").replace("\r\n",""))
    def unclick(self):
        self.COM.exec_raw_no_follow('b.unclick()')#.decode("utf-8").replace("/r/n","")
    def calib(self):
        self.COM.exec_raw_no_follow('b.moveTillCorner()')
class experiment:
    def __init__(self,sensor):
        self.sensor=sensor
        path=""
        if sys.platform.startswith('win'):
            path="C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Rig/boardSide.py"
        else:
            path="/its/home/drs25/Documents/GitHub/TactileSensor/Code/Rig/boardSide.py"
        self.control=Board()
        self.control.autoConnect(path) #autoconnect and run file

    def moveTillTouch(self,threshold=300):
        touched=False
        #get moving
        for i in range(100):
            s=self.sensor.getSensor(type_="round")
        t1=time.time()
        while not touched:
            s=self.sensor.getSensor(type_="round")
            self.control.moveZ(1)
            if time.time()-t1>5: touched=True #np.average(s)>=threshold or
        #print("Override")
        self.control.moveZ(5,override=True) 
        print("Touching surface")
    def moveZ(self,cm,dir): #dir must be 1 or -1
        assert dir==1 or dir==-1, "Incorrect direction, must be 1 or -1"
        cm=cm*17 #17 steps per cm
        for i in range(0,round(cm)):
            self.control.moveZ(1*dir) #move up
    def moveX(self,cm,dir): #dir must be 1 or -1
        assert dir==1 or dir==-1, "Incorrect direction, must be 1 or -1"
        cm=cm*26 #26 steps per cm
        for i in range(0,round(cm)):
            self.control.moveX(1*dir) #move up
    def pressures(self,cm_samples=2,step=0.5):
        a=[]
        d=[]
        self.moveTillTouch() #be touching the platform
        for i in np.arange(0, cm_samples, step):
            #print("depth:",i)
            mag=self.sensor.getSensor(type_="round")
            time.sleep(1)
            self.moveZ(i,1) #move down
            time.sleep(1)
            data=self.sensor.getSensor(type_="round")
            a.append(data)
            d.append(self.control.getWeight())
            self.moveZ(i,-1) #move back
        self.moveZ(1,1) #move back
        return np.array(a),np.array(d)
    def direction(self,trials,steps):
        a=[]
        #self.moveZ(0.5,-1) #move back
        self.control.unclick()
        print("calib")
        self.control.calib()
        for i in range(0, trials):
            #print("depth:",i)
            a_prime=[]
            self.moveTillTouch()
            a_=[]
            for j in range(steps):
                mag=self.sensor.getSensor(type_="round")
                self.moveX(1,-1)
                a_.append(mag)
            a_prime.append(a_)
            a_=[]
            for j in range(steps):
                mag=self.sensor.getSensor(type_="round")
                self.moveX(1,1)
                a_.append(mag)
            a_prime.append(a_)
            a.append(a_prime)
            self.control.unclick()
            self.control.calib()
        return np.array(a)
    