import machine
import time

# Define the control pins
S0 = machine.Pin(0,machine.Pin.OUT)  # GP0
S1 = machine.Pin(1,machine.Pin.OUT)  # GP1
S2 = machine.Pin(2,machine.Pin.OUT)  # GP2
S3 = machine.Pin(3,machine.Pin.OUT)  # GP3
SIG = machine.ADC(28)  # GP28

# Function to select a channel on the multiplexer
def select_channel(channel):
    channel=f'{channel:04b}'
    S0.value(int(channel[3]))
    S1.value(int(channel[2]))
    S2.value(int(channel[1]))
    S3.value(int(channel[0]))

while True:
    for channel in range(4):
        select_channel(channel)
        value = SIG.read_u16()  # Read the analog value
        print(f"Channel {channel}: {value}")
        print(S0.value(),S1.value(),S2.value(),S3.value())
        time.sleep(1)  # Adjust the delay as needed
