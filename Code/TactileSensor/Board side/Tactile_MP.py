"""
Foot as an object for micropython
"""
import machine
import time

class Foot:
    def __init__(self,pins,analog,alpha=0.2):
        # Define the control pins
        assert len(pins)==4, "Incorrect number of pins"
        self.s=[]
        for pin in pins:
            self.s.append(machine.Pin(pin,machine.Pin.OUT))  # GPIO
        self.SIG = machine.ADC(analog)  # GP26
        self.low_pass=[0 for i in range(16)]
        self.band_pass=[0 for i in range(16)]
        self.alpha=alpha
        self.prev=None
    def select_channel(self,channel):
        channel=f'{channel:04b}'
        for i in range(len(self.s)):
            self.s[i].value(int(channel[len(self.s)-i-1]))
    def read(self): #read all the values
        ar=[]
        for i in range(16):
            self.select_channel(i)
            time.sleep(0.001)
            value = self.SIG.read_u16()  # Read the analog value
            ar.append(value)
            value=(1-self.alpha)*self.low_pass[i] + (self.alpha*value) #low pass filter
            self.low_pass[i]=value
            value=self.alpha*self.band_pass[i] + self.alpha*(value-self.low_pass[i])
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

