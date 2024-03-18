#code to move leg across a surface and gather data


from mpremote import pyboard
import serial, time
import sys
import glob
import numpy as np


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
    def autoConnect(self,file=""):
        COM=""
        if file=="": #defaut files for my PC
            if sys.platform.startswith('win'):
                file="C:/Users/dexte/Documents/GitHub/TactileSensor/Code/TactileSensor/boardSide.py"
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
    def moveServo(self,num,angle):
        self.COM.exec_raw_no_follow('sb.servoWrite('+str(num)+','+str(angle)+')')
    def getServo(self,servo):
        data=self.COM.exec('sb.getServo('+str(servo)+')').decode("utf-8").replace("\r\n","").replace("[","").replace("]","").replace(" ","")
        return data
    def getSensor(self,type_="flat",x=5,y=5,alpha=0.6,num=16):
        data=self.COM.exec('gather(alpha='+str(alpha)+')').decode("utf-8").replace("\r\n","").replace("[","").replace("]","").replace(" ","")
        grid=np.array(data.split(",")).astype(float)
        #self.zero()
        #difference=self.middle-grid
        processed=grid.copy()
        window_size=2
        #processed = np.convolve(processed, np.ones(window_size) / window_size, mode='same')
        #if type(self.past_data)!=type(None): #work out change
        #    processed=np.abs((self.past_data-processed)/np.max(self.past_data))
        self.past_data=grid.copy()
        grid=processed.copy()
        if type_=="flat":
            processed=processed[:10]
            grid=np.zeros((x,y))
            for i in range(x):
                grid[i]=processed[i]
            for i in range(y):
                grid[:,i]+=processed[x+i]
        elif type_=="round": #if round type return data
            grid=grid
        elif type_=="foot":
            grid=np.zeros((3,5))
            grid[2][4]=processed[0]
            grid[2][3]=processed[1]
            grid[2][2]=processed[2]
            grid[2][1]=processed[3]
            grid[2][0]=processed[4]

            grid[1][3]=processed[8]
            grid[1][2]=processed[9]
            grid[1][1]=processed[6]
            grid[1][0]=processed[5]

            grid[0][4]=processed[10]
            grid[0][3]=processed[11]
            grid[0][2]=processed[12]
            grid[0][1]=processed[13]
            grid[0][0]=processed[14]
        return grid