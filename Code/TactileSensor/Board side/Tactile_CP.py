"""
Foot as an object for circuitpython
"""
from adafruit_mcp230xx.mcp23017 import MCP23017
import busio
import board
import digitalio
from analogio import AnalogIn
import time
import board
import adafruit_ads7830.ads7830 as ADC
from adafruit_ads7830.analog_in import AnalogIn


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
    def __init__(self,pins,analog,alpha=0.2):
        # Define the control pins
        assert len(pins)==4, "Incorrec number of pins"
        self.s=[]
        for pin in pins:
            self.s.append(pin)  # GPIO
        self.SIG = AnalogIn(analog)# GP26
        self.low_pass=[0 for i in range(16)]
        self.band_pass=[0 for i in range(16)]
        self.alpha=alpha
        self.prev=None
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
            value=(1-self.alpha)*self.low_pass[i] + (self.alpha*value) #low pass filter
            self.low_pass[i]=value
            value=self.alpha*self.band_pass[i] + self.alpha*(value-self.low_pass[i]) #bandpass filter
            self.band_pass[i]=value
        return ar
    def grads(self,dat):
        if type(self.prev)==type(None):#if not real
            self.prev=dat.copy()
        grads=[]
        for j in range(len(dat)):
            grads.append((dat[j]-self.prev[j])/2)
        #self.prev=dat.copy()
        return grads
    
class I2C_Tactile:
    def __init__(self,i2c=None,alpha=0.4):
        if type(i2c)==type(None):
            i2c = board.I2C()
        self.adc1=ADC.ADS7830(i2c,address=0x49)
        self.adc2=ADC.ADS7830(i2c,address=0x48)
        self.low_pass=[0 for i in range(16)]
        self.band_pass=[0 for i in range(16)]
        self.alpha=alpha
    def readGyro(self):
        self.x = AnalogIn(self.adc1, 1).value
        self.y = AnalogIn(self.adc1, 2).value
        self.z = AnalogIn(self.adc1, 3).value
        return self.x,self.y,self.z
    def read(self):
        ar=[]
        for i in range(8):
            ar.append(AnalogIn(self.adc2, i).value)
            value=(1-self.alpha)*self.low_pass[i] + (self.alpha*value) #low pass filter
            self.low_pass[i]=value
            value=self.alpha*self.band_pass[i] + self.alpha*(value-self.low_pass[i]) #bandpass filter
            self.band_pass[i]=value
        for i in range(8):
            ar.append(AnalogIn(self.adc1, i).value)
            value=(1-self.alpha)*self.low_pass[8+i] + (self.alpha*value) #low pass filter
            self.low_pass[8+i]=value
            value=self.alpha*self.band_pass[8+i] + self.alpha*(value-self.low_pass[8+i]) #bandpass filter
            self.band_pass[8+i]=value
        return ar
    def read_sig(self): #return basic signal
        self.read()
        return self.s
    def read_LP(self): #return low passed signal
        self.read()
        return self.low_pass
    def read_BP(self): #return band passed signal
        self.read()
        return self.band_pass

class Plate(I2C_master):
    def __init__(self,analog,i2c=None,address=0x21,sda=None,scl=None,alpha=0.1):
        super().__init__(analog,i2c=None,address=0x21,sda=None,scl=None)
        self.s=[[self.mcp.get_pin(i+j) for i in range(4)] for j in range(6)] #needs exact values
        self.SIG = AnalogIn(analog)# GP26
        self.low_pass=[0 for i in range(16*6)]
        self.band_pass=[0 for i in range(16*6)]
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
            value=(1-self.alpha)*self.low_pass[i] + (self.alpha*value) #low pass filter
            self.low_pass[i]=value
            value=self.alpha*self.band_pass[i] + self.alpha*(value-self.low_pass[i]) #bandpass filter
            self.band_pass[i]=value
    def read_sig(self):
        self.read()
        return self.s
    def read_LP(self):
        self.read()
        return self.low_pass
    def read_BP(self):
        self.read()
        return self.band_pass