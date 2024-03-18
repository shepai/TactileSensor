"""
Foot as an object for micropython
"""
import machine
import time

class Foot:
    def __init__(self,pins,analog,out,alpha=0.2):
        # Define the control pins
        assert len(pins)!=4, "Incorrec number of pins"
        self.s=[]
        for pin in pins:
            self.s.append(machine.Pin(pin,machine.Pin.OUT))  # GPIO
        self.SIG = machine.ADC(analog)  # GP26
        machine.Pin(out,machine.Pin.OUT)  # GP3
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
            value = self.SIG.read_u16()  # Read the analog value
            ar.append(value)
            value=(1-self.alpha)*self.a[i] + (self.alpha*value) #low pass filter
            self.a[i]=value
            value=self.alpha*self.b[i] + self.alpha*(value-self.a[i])
            self.b[i]=value
        return ar