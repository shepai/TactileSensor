import machine
import time

# Define the control pins

SIG = machine.ADC(26)  # GP28

def gather(low_pass=True,high_pass=True,alpha=0.2):
    global a
    global b
    global UT
    array=0
    untouched=0

    value = SIG.read_u16()  # Read the analog value
    untouched=value
    if low_pass:
        value=(1-alpha)*a + (alpha*value) #low pass filter
    if high_pass:
        value=alpha*b + alpha*(value-a)
    array=value
    print(array)
    a=array
    b=array
    UT=untouched
    return array

a=gather(low_pass=False,high_pass=False)
b=gather(low_pass=False,high_pass=False)
UT=gather(low_pass=False,high_pass=False)