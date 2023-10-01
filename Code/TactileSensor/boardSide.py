import machine
import time

# Define the control pins
S0 = machine.Pin(0,machine.Pin.OUT)  # GP0
S1 = machine.Pin(1,machine.Pin.OUT)  # GP1
S2 = machine.Pin(2,machine.Pin.OUT)  # GP2
S3 = machine.Pin(3,machine.Pin.OUT)  # GP3
SIG = machine.ADC(26)  # GP28

a=[]
b=[]

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
    for i in range(10):
        select_channel(i)
        value = SIG.read_u16()  # Read the analog value
        untouched.append(value)
        if low_pass:
            value=(1-alpha)*a[i] + (alpha*value) #low pass filter
        if high_pass:
            value=alpha*b[i] + alpha*(value-a[i])
        array.append(value)
    print(array)
    a=array.copy()
    b=array.copy()
    UT=untouched.copy()
    return array

a=gather(low_pass=False,high_pass=False)
b=gather(low_pass=False,high_pass=False)
UT=gather(low_pass=False,high_pass=False)