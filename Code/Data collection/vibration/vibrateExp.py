import board
import busio
import digitalio
import sdcardio
import storage
import time
import neopixel
import analogio
import ulab.numpy as np

S0 = digitalio.DigitalInOut(board.D5 if "D5" in dir(board) else boad.GP3)
S0.direction = digitalio.Direction.OUTPUT
S1 = digitalio.DigitalInOut(board.D4 if "D4" in dir(board) else boad.GP2)
S1.direction = digitalio.Direction.OUTPUT
S2 = digitalio.DigitalInOut(board.D3 if "D3" in dir(board) else boad.GP1)
S2.direction = digitalio.Direction.OUTPUT
S3 = digitalio.DigitalInOut(board.D2 if "D2" in dir(board) else boad.GP30)
S3.direction = digitalio.Direction.OUTPUT
pinA = analogio.AnalogIn(board.A0 if "A0" in dir(board) else boad.GP28)

# Define the parameters for your LED ring
num_pixels = 12*5  # Number of LEDs in your ring
pin = board.D8 if "D8" in dir(board) else board.GP8   # Define the pin connected to the LED ring

# Create a NeoPixel object with the specified parameters
pixels = neopixel.NeoPixel(pin, num_pixels, brightness=0.1, auto_write=False)

# Create SPI bus
spi = busio.SPI(board.SD_SCK, MOSI=board.SD_MOSI, MISO=board.SD_MISO)  # SCK, MOSI, MISO

# Create digital input/output object for SD card's CS pin
sd=False
try:
    cs=board.SD_CS if "D17" in dir(board) else board.GP17
    sdcard = sdcardio.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    with open("/sd/vibration.csv", "w") as file:  # Change the file path/name as needed
        file.write("Rotation,LED_no,s1,s2,s3,s4,t\n")
    sd=True
except OSError as e:
    print("No SD card",e)

def select_channel(channel):
    channel=f'{channel:04b}'
    S0.value=int(channel[3])
    S1.value=int(channel[2])
    S2.value=int(channel[1])
    S3.value=int(channel[0])

past=np.array([0,0,0,0])
alpha=0.2
rotation=0
trials=10
for k in range(trials):
    for i in range(num_pixels):
        #show user pixel
        pixels[i]=(255,0,255)
        pixels.show()
        time.sleep(0.1)
        #gather data
        for t in range(100):
            a=[]
            for j in range(4):
                select_channel(j)
                a.append(pinA.value)
            a=np.array(a)
            filtered=(1-alpha)*past + alpha*a #low pass
            past=a.copy()
            print(filtered)
            if sd:
                with open("/sd/vibration.csv", "a") as file:  # Change the file path/name as needed
                    s=""
                    for dat in a:
                        s+=str(dat)+","
                    s=str(rotation)+","+str(i)+","+s+str(t)+"\n"
                    file.write(s)
        #remove pixel
        pixels[i]=(0,0,0)
        pixels.show()
        if i==num_pixels-1:
            rotation+=1
    

if sd:
    storage.mount(vfs, "/sd")
    sdcard.unmount()  # Unmount SD card when done

