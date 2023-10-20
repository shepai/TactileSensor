"""
CircuitPython variant of gonk
"""

import board
import busio
import busio as io
import sdcardio
import storage
import adafruit_mpu6050
import adafruit_ht16k33.matrix
import digitalio
import analogio
from audiomp3 import MP3Decoder
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!
import pwmio
from adafruit_motor import servo
import time
import ulab.numpy as np

class gonk:
    def __init__(self):
        self.DELAY=0.0001
        self.i2c = io.I2C(board.GP9, board.GP8)
        #setup sd card
        spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
        cs = board.GP15
        sd = sdcardio.SDCard(spi, cs)
        vfs = storage.VfsFat(sd)
        self.sd=1
        try:
            storage.mount(vfs, '/sd')
            with open("/sd/test.csv", "w") as f:
                f.write("test")
        except:
            print("No Sd card")
            self.sd=0
        self.audio = AudioOut(board.GP18)
        #setup eye
        self.timer=time.time()
        self.eye=[
                [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
                [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0]
            ]
        self.eyes=1
        self.display=None
        try:
            self.display = adafruit_ht16k33.matrix.Matrix16x8(self.i2c)
            self.display.brightness=0.4
        except:
            print("No eyes detected")
            self.eyes=0.0
        #setup MPU sensor
            self.temp=0
        self.mpu=1
        try:
            self.mpu_ = adafruit_mpu6050.MPU6050(self.i2c)
        except:
            print("No mpu6050 detected")
            self.mpu=0
        #setup servos
        pins=[board.GP17,board.GP20,board.GP21,board.GP22]
        self.servos=[servo.Servo(pwmio.PWMOut(pins[i], frequency=50),min_pulse=750, max_pulse=2250) for i in range(len(pins))]
        #setup feet
        self.S0 = digitalio.DigitalInOut(board.GP0)
        self.S0.direction = digitalio.Direction.OUTPUT
        self.S1 = digitalio.DigitalInOut(board.GP1)
        self.S1.direction = digitalio.Direction.OUTPUT
        self.S2 = digitalio.DigitalInOut(board.GP3)
        self.S2.direction = digitalio.Direction.OUTPUT
        self.S3 = digitalio.DigitalInOut(board.GP4)
        self.S3.direction = digitalio.Direction.OUTPUT
        self.pin = analogio.AnalogIn(board.GP26)
        #bandpass filter
        self.LP=self.getFeet()
        self.HP=self.getFeet()
    def getFeet(self):
        def select_channel(channel):
            channel=f'{channel:04b}'
            self.S0.value=int(channel[3])
            self.S1.value=int(channel[2])
            self.S2.value=int(channel[1])
            self.S3.value=int(channel[0])
        a=[]
        for i in range(10):
            select_channel(i)
            a.append(self.pin.value)
        return np.array(a)
    def filter(self,array,alpha=0.2):
        low_pass=(1-alpha)*self.LP +(alpha*array)
        highpass=alpha*self.HP + alpha*(low_pass-self.LP)
        self.LP=low_pass.copy()
        self.HP=highpass.copy()
        return highpass
    def move(self,servo,angle):
        assert servo>=0 and servo<len(self.servos),"Incorrect index"
        self.servos[servo].angle=angle
    def display_face(self,motion):
        #display the eye
        if self.eyes:
            for i in range(8):
                for j in range(16):
                    self.display[j, i] = motion[i][j]
                    self.display.show()

                    time.sleep(self.DELAY)
    def writeData(self,name,gyro,pressure):
        if self.mpu and self.sd:
            with open("/sd/"+str(name), "a") as f:
                f.write(str(gyro[0])+","+str(gyro[1])+","+str(gyro[2])+","+pressure+"\n")
        else: print("Cannot save as sensor or storage device missing")
    def blink(self):
        #blink the eye
        test=self.eye.copy()
        if self.eyes:
            for k in range(3):
                for i in range(len(test)):
                    for j in range(len(test[0])):
                        self.display[j, i] = test[i][j]
                self.display.show()
                test.pop(k+1)
                test.pop(len(test)-k-1)
                test.insert(k,[0 for i in range(16)])
                test.insert(len(test)-k,[0 for i in range(16)])
            for i in range(8):
                for j in range(16):
                    self.display[j, i] = 0
                    self.display[j,3]=1
                    self.display[j,4]=1
            time.sleep(0.1)
            self.display_face(self.eye)
    def getGyro(self):
        if self.mpu:
            gyro=self.mpu_.gyro
            acc=self.mpu_.acceleration
            self.temp=self.mpu_.temperature
            return gyro
    def playSound(self):
        mp3 = open("gonk-droid-sound.mp3", "rb")
        decoder = MP3Decoder(mp3)
        decoder.file = open("gonk-droid-sound.mp3", "rb")
        self.audio.play(decoder)
        t = time.monotonic()
        while time.monotonic() - t < 3:
            pass
droid=gonk()
for i in range(10):
    print(droid.filter(droid.getFeet()))
droid.display_face(droid.eye)
droid.blink()
droid.playSound()
print(droid.getGyro())
print("Temperature:",droid.temp)
droid.writeData("test.csv",droid.getGyro(),"example")
