import board
import busio
import busio as io
import sdcardio
import storage
import os
import digitalio
import time
import pulseio
import neopixel
import analogio

spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
cs = board.GP15
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')

#define foot
LF=[digitalio.DigitalInOut(board.GP0),digitalio.DigitalInOut(board.GP1),digitalio.DigitalInOut(board.GP2),digitalio.DigitalInOut(board.GP3)]
for i in range(len(LF)): #set mode
    LF[i].direction = digitalio.Direction.OUTPUT
Lpin = analogio.AnalogIn(board.GP26)            
# Define the GPIO pins for the buttons
button_pins = [board.GP20, board.GP21, board.GP22]
led_pins = [board.GP6, board.GP7, board.GP8, board.GP9]  # Example LED pins, adjust as needed

# Initialize buttons as digital inputs with pull-down resistors
buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.DOWN
# Initialize LEDs as digital outputs
leds = [digitalio.DigitalInOut(pin) for pin in led_pins]
for led in leds:
    led.direction = digitalio.Direction.OUTPUT
    
    
def getFilename(name):
    # Specify the file path
    count=0
    name="file"
    file=name+"_"+str(count)+".csv"
    # Check if the file exists
    files=os.listdir("/sd/")

    while file in files:
        count+=1
        file=name+"_"+str(count)+".csv"
    return file

def selectLED(num):
    leds[0].value = 0
    leds[1].value = 0
    leds[2].value = 0
    leds[3].value = 0
    leds[num].value = True

def select_channel(channel,foot): #select a channel
    channel=f'{channel:04b}'
    foot[0].value=int(channel[3])
    foot[1].value=int(channel[2])
    foot[2].value=int(channel[1])
    foot[3].value=int(channel[0])

pixel_pin = board.GP28
num_pixels = 1
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)

pixels.fill((0,200,0))
pixels.show()

print(getFilename("file"))
surfaces=["rough","smooth","concrete","nothing"]
record=False
mode=0
filename=".."
# Main loop
timer=0
f=None
exit=0
while exit<2: 
    for i, button in enumerate(buttons):
        if not button.value:
            if i==0 and not record:

                filename=getFilename(surfaces[mode])
                f=open("/sd/"+filename,"w") #create unique file
                keys=["time"]+["s"+str(i) for i in range(16)]
                for j in range(len(keys)-1):
                    f.write(keys[j]+",")
                f.write(keys[-1]+"\n")
                timer=time.monotonic()
                pixels.fill((200,0,0))
                pixels.show()
                record=True
                exit=0
            if i==1:
                mode+=1
                time.sleep(0.2)
                if mode>=4:
                    mode=0
                selectLED(mode)
            if i==2: #click twice to leave
                f.close()
                record=False
                pixels.fill((0,200,0))
                pixels.show()
                exit+=1
                time.sleep(0.2)
    if record:
        f.write(str(time.monotonic()-timer)+",")
        s=""
        ar=[]
        for i in range(16):
            select_channel(i,LF)
            val=Lpin.value
            ar.append(val)
            s+=str(val)+","
        print(ar)
        f.write(s[:-1]+"\n")
        
    else:
        time.sleep(0.01)  # small delay to avoid busy-waiting and reduce CPU usage
