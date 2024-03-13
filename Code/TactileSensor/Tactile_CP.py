"""
Foot as an object for circuitpython
"""
from adafruit_mcp230xx.mcp23017 import MCP23017
import busio
import board
import digitalio
from analogio import AnalogIn

class I2C_master:
    def __init__(self,analog,i2c=None,address=0x21,sda=None,scl=None):
        if type(i2c)!=type(None):
            self.mcp = MCP23017(i2c, address=address)  # MCP23017 w/ A0 set
        else:
            i2c = busio.I2C(scl, sda)
            self.mcp = MCP23017(i2c, address=address)
    def setPin(self,pin,value): #set the pin value
        self.mcp.get_pin(pin).value=value
        
class Foot:
    def __init__(self,pins,analog,out,alpha=0.2):
        # Define the control pins
        assert len(pins)!=4, "Incorrec number of pins"
        self.s=[]
        for pin in pins:
            self.s.append(pin)  # GPIO
        self.SIG = AnalogIn(analog)# GP26
        digitalio.DigitalInOut(out)
        self.low_pass=[0 for i in range(16)]
        self.band_pass=[0 for i in range(16)]
        self.alpha=alpha
    def select_channel(self,channel):
        channel=f'{channel:04b}'
        for i in range(len(self.s)):
            self.s[i].value=int(channel[len(self.s)-i-1])
    def read(self): #read all the values
        ar=[]
        for i in range(16):
            self.select_channel(i)
            value = self.SIG.value # Read the analog value
            ar.append(value)
            value=(1-self.alpha)*self.a[i] + (self.alpha*value) #low pass filter
            self.a[i]=value
            value=self.alpha*self.b[i] + self.alpha*(value-self.a[i]) #bandpass filter
            self.b[i]=value
        return ar
    
class Foot_i2c(I2C_master):
    def __init__(self,analog,i2c=None,address=0x21,sda=None,scl=None,alpha=0.1):
        super().__init__(analog,i2c=None,address=0x21,sda=None,scl=None)
        self.SIG = AnalogIn(analog)# GP26
        self.s=[self.mcp.get_pin(i) for i in range(4)]
        self.low_pass=[0 for i in range(16)]
        self.band_pass=[0 for i in range(16)]
        self.alpha=alpha
    def select_channel(self,channel):
        channel=f'{channel:04b}'
        for i in range(len(self.s)):
            self.s[i].value=int(channel[len(self.s)-i-1])
    def read(self):
        #read the foot and return an array of values
        ar=[]
        for i in range(16):
            self.select_channel(i)
            value=self.SIG.value
            ar.append(value)
            value=(1-self.alpha)*self.a[i] + (self.alpha*value) #low pass filter
            self.a[i]=value
            value=self.alpha*self.b[i] + self.alpha*(value-self.a[i]) #bandpass filter
            self.b[i]=value

class Plate(I2C_master):
    def __init__(self,analog,i2c=None,address=0x21,sda=None,scl=None,alpha=0.1):
        super().__init__(analog,i2c=None,address=0x21,sda=None,scl=None)
        self.s=[[self.mcp.get_pin(i+j) for i in range(4)] for j in range(6)] #needs exact values
        self.SIG = AnalogIn(analog)# GP26
        self.low_pass=[0 for i in range(16)]
        self.band_pass=[0 for i in range(16)]
        self.alpha=alpha
    def select_channel(self,boardID,channel):
        channel=f'{channel:04b}'
        for i in range(len(self.s)):
            self.s[boardID][i].value=int(channel[len(self.s)-i-1])
    def read(self):
        #read the foot and return an array of values
        ar=[]
        for i in range(16):
            self.select_channel(i)
            value=self.SIG.value
            ar.append(value)
            value=(1-self.alpha)*self.a[i] + (self.alpha*value) #low pass filter
            self.a[i]=value
            value=self.alpha*self.b[i] + self.alpha*(value-self.a[i]) #bandpass filter
            self.b[i]=value