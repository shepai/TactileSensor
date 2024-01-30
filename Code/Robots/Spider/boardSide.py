from machine import Pin
import machine
import utime

S0 = machine.Pin(0,machine.Pin.OUT)  # GP0
S1 = machine.Pin(1,machine.Pin.OUT)  # GP1
S2 = machine.Pin(2,machine.Pin.OUT)  # GP2
S3 = machine.Pin(3,machine.Pin.OUT)  # GP3
SIG = machine.ADC(26)  # GP28

SE = machine.Pin(4,machine.Pin.OUT)  # GP3
SE.value(0)
a=[]
b=[]


class servoBot:
    def __init__(self,I2CAddress=108,sda=8,scl=9):
        self.CHIP_ADDRESS = 108
        sda=machine.Pin(sda)
        scl=machine.Pin(scl)
        self.i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)
        self.initPCA()
        self.servos=[-1 for i in range(8)]
    #Class variables - these should be the same for all instances of the class.
    # If you wanted to write some code that stepped through
    # the servos or motors then this is the Base and size to do that
    SRV_REG_BASE = 0x08
    MOT_REG_BASE = 0x28
    REG_OFFSET = 4

    #to perform a software reset on the PCA chip.
    #Separate from the init function so we can reset at any point if required - useful for development...
    def swReset(self):
        self.i2c.writeto(0,"\x06")

    #setup the PCA chip for 50Hz and zero out registers.
    def initPCA(self):
        self.swReset() #make sure we are in a known position
        #setup the prescale to have 20mS pulse repetition - this is dictated by the servos.
        self.i2c.writeto_mem(108,0xfe,"\x78")
        #block write outputs to off
        self.i2c.writeto_mem(108,0xfa,"\x00")
        self.i2c.writeto_mem(108,0xfb,"\x00")
        self.i2c.writeto_mem(108,0xfc,"\x00")
        self.i2c.writeto_mem(108,0xfd,"\x00")
        #come out of sleep
        self.i2c.writeto_mem(108,0x00,"\x01")

    def setPrescaleReg(self):
        self.i2c.writeto_mem(108,0xfe,"\x78")

    def servoWrite(self,servo, degrees):
        #check the degrees is a reasonable number. we expect 0-180, so cap at those values.
        if(degrees>180):
            degrees = 180
        elif (degrees<0):
            degrees = 0
        #check the servo number
        if((servo<1) or (servo>8)):
            raise Exception("INVALID SERVO NUMBER") #harsh, but at least you'll know
        calcServo = self.SRV_REG_BASE + ((servo - 1) * self.REG_OFFSET)
        PWMVal = int((degrees*2.2755)+102) # see comment above for maths
        lowByte = PWMVal & 0xFF
        highByte = (PWMVal>>8)&0x01 #cap high byte at 1 - shoud never be more than 2.5mS.
        self.i2c.writeto_mem(self.CHIP_ADDRESS, calcServo,bytes([lowByte]))
        self.i2c.writeto_mem(self.CHIP_ADDRESS, calcServo+1,bytes([highByte]))
        self.servos[servo-1]=degrees
    def getServo(self,servo):
        if((servo<1) or (servo>8)):
            raise Exception("INVALID SERVO NUMBER") #harsh, but at least you'll know
        print(self.servos[servo-1])

# Function to select a channel on the multiplexer
def select_channel(channel):
    channel=f'{channel:04b}'
    S0.value(int(channel[3]))
    S1.value(int(channel[2]))
    S2.value(int(channel[1]))
    S3.value(int(channel[0]))


def gather(low_pass=True,high_pass=True,alpha=0.2):
    global a
    global b
    global UT
    array=[]
    untouched=[]
    for i in range(16):
        select_channel(i)
        value = SIG.read_u16()  # Read the analog value
        untouched.append(value)
        if low_pass:
            value=(1-alpha)*a[i] + (alpha*value) #low pass filter
        if high_pass:
            value=alpha*b[i] + alpha*(value-a[i])
        array.append(value)
    print([float('{:f}'.format(untouched[i])) for i in range(len(array))])
    a=array.copy()
    b=array.copy()
    UT=untouched.copy()
    return array

a=gather(low_pass=False,high_pass=False)
b=gather(low_pass=False,high_pass=False)
UT=gather(low_pass=False,high_pass=False)
        
sb=servoBot()
sb.servoWrite(8,150)
sb.servoWrite(7,0)
sb.servoWrite(6,55)
