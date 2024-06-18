"""
Foot as an object for micropython
"""
import machine
from machine import Pin, I2C
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

class ADS7830:
    """Adafruit ADS7830 ADC driver"""

    # Single channel selection list
    _CHANNEL_SELECTION = [
        0x08,  # SINGLE_CH0
        0x0C,  # SINGLE_CH1
        0x09,  # SINGLE_CH2
        0x0D,  # SINGLE_CH3
        0x0A,  # SINGLE_CH4
        0x0E,  # SINGLE_CH5
        0x0B,  # SINGLE_CH6
        0x0F,  # SINGLE_CH7
    ]
    # Differential channel selection list
    _DIFF_CHANNEL_SELECTION = [
        0x00,  # DIFF_CH0_CH1
        0x04,  # DIFF_CH1_CH0
        0x01,  # DIFF_CH2_CH3
        0x05,  # DIFF_CH3_CH2
        0x02,  # DIFF_CH4_CH5
        0x06,  # DIFF_CH5_CH4
        0x03,  # DIFF_CH6_CH7
        0x07,  # DIFF_CH7_CH6
    ]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        i2c: I2C,
        address: int = 0x48,
        differential_mode: bool = False,
        int_ref_power_down: bool = False,
        adc_power_down: bool = False) -> None:
        """Initialization over I2C

        :param int address: I2C address (default 0x48)
        :param bool differential_mode: Select differential vs. single mode
        :param bool int_ref_power_down: Power down internal reference after sampling
        :param bool adc_power_down: Power down ADC after sampling
        """
        self.i2c_device = i2c
        _pd = 0
        if not int_ref_power_down:
            _pd |= 2
        if not adc_power_down:
            _pd |= 1
        self.power_down = _pd
        self.differential_mode = differential_mode
        self.address=address
    def read(self, channel: int) -> int:
        """ADC value
        Scales the 8-bit ADC value to a 16-bit value

        :param int channel: Channel (0-7)
        :return: Scaled ADC value or raise an exception if read failed
        :rtype: int
        """
        if channel > 7:
            raise ValueError("Invalid channel: must be 0-7")
        if self.differential_mode:
            command_byte = self._DIFF_CHANNEL_SELECTION[channel // 2]
        else:
            command_byte = self._CHANNEL_SELECTION[channel]
        command_byte <<= 4
        command_byte |= self.power_down << 2

        try:
            # Buffer to store the read ADC value
            adc_value = bytearray(1)
            self.i2c_device.writeto(self.address,bytearray([command_byte]))
            adc_value=self.i2c_device.readfrom(self.address,1)
            # Scale the 8-bit value to 16-bit
            return adc_value[0] << 8
        except Exception as error:
            raise RuntimeError(f"Failed to read value: {error}") from error
        
class I2C_Tactile:
    def __init__(self,i2c=None,alpha=0.4):
        if type(i2c)==type(None):
            i2c = I2C(0,scl=Pin(1), sda=Pin(0),freq=400000)
        self.adc1=ADS7830(i2c,address=0x49)
        self.adc2=ADS7830(i2c,address=0x48)
        self.low_pass=[0 for i in range(16)]
        self.band_pass=[0 for i in range(16)]
        self.alpha=alpha
    def readGyro(self):
        self.x = self.adc1.read(1)
        self.y = self.adc1.read(2)
        self.z = self.adc1.read(3)
        return self.x,self.y,self.z
    def read(self):
        ar=[]
        for i in range(8):
            value=self.adc2.read(i).value
            ar.append(value)
            value=int((1-self.alpha)*self.low_pass[i] + (self.alpha*value)) #low pass filter
            if value<=0: value=0
            self.low_pass[i]=value
            #value=self.alpha*self.band_pass[i] + self.alpha*(value-self.low_pass[i]) #bandpass filter
            #self.band_pass[i]=value
        for i in range(8):
            value=self.adc1.read(i).value
            ar.append(value)
            value=int((1-self.alpha)*self.low_pass[8+i] + (self.alpha*value)) #low pass filter
            if value<=0: value=0
            self.low_pass[8+i]=value
            #value=self.alpha*self.band_pass[8+i] + self.alpha*(value-self.low_pass[8+i]) #bandpass filter
            #self.band_pass[8+i]=value
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