
from mpremote import pyboard
import serial, time
import sys
import glob
import numpy as np

"""
Setup control with micropython device
"""

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
    def runFile(self,fileToRun='boardSide.py'):
        """
        runFile allows the user to send a local file to the device and run it
        @param fileToRun is the file that will be locally installed
        """
        if self.COM==None:
            raise OSError("Connect to device before running file")
        self.COM.execfile(fileToRun) #run the file controlling the sensors
    def autoConnect(self,file=""):
        COM=""
        if file=="": #defaut files for my PC
            if sys.platform.startswith('win'):
                file="C:/Users/dexte/OneDrive/Documents/GitHub/TactileSensor/Code/TactileSensor/boardSide.py"
            else:
                file="/its/home/drs25/Documents/GitHub/TactileSensor/Code/TactileSensor/boardSide.py"
        while COM=="":
            try:
                res=self.serial_ports()
                print("ports:",res)
                self.connect(res[0])
                self.runFile(file) #C:/Users/dexte/OneDrive/Documents/GitHub/TactileSensor/Code/TactileSensor/boardSide.py
                COM=res[0]
            except IndexError:
                time.sleep(1)
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
    def getSensor(self,type_="flat",x=5,y=5,alpha=0.1):
        data=self.COM.exec('gather(alpha='+str(alpha)+')').decode("utf-8").replace("\r\n","").replace("[","").replace("]","").replace(" ","")
        grid=None
        if type_=="flat":
            data=data.split(",")
            grid=np.zeros((x,y))
            for i in range(x):
                grid[i]=float(data[i])
            for i in range(y):
                grid[:,i]+=float(data[x+i])
        elif type_=="round": #if round type return data
            data=self.COM.exec('gather()').decode("utf-8").replace("\r\n","").replace("[","").replace("]","").replace(" ","")
            data=data.split(",")
            grid=np.array(data).astype(float)
        return grid
    
    
