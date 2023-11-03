import PicoRobotics
import utime
from machine import freq, Pin, ADC

class Move:
    def __init__(self,speed=40):
        self.board=PicoRobotics.KitronikPicoRobotics()
        self.speed=speed
        self.board.motorOff(1)
        self.pushX=Pin(26 , Pin.IN, Pin.PULL_UP)
        self.pushY=Pin(27 , Pin.IN, Pin.PULL_UP)
    def moveZ(self,num,overide=False,speed=40):
        direction="f"
        if num<0:
            direction="r"
        for step in range(abs(num)):
            if self.pushX.value() or overide or direction=="r":
                self.board.step(1,direction,speed)
    def moveX(self,num,speed=40):
        direction="f"
        if num<0:
            direction="r"
        for step in range(abs(num)):
            if self.pushY.value() or direction=="f":
                self.board.step(2,direction,speed)
            elif not self.pushY.value(): #if touches side move backwards
                while not self.pushY.value():
                    self.board.step(2,"f",self.speed)
    def unclick(self):
        while not self.pushX.value():
            self.board.step(1,"r",100)
        #self.board.step(1,"r",100)
        while not self.pushY.value():
            self.board.step(2,"f",100)
        #self.board.step(2,"f",100)
    def moveX_dc(self,num,stopFunc=None):
        direction="f"
        if num<0:
            direction="r"
        step=0
        stop=False
        if self.pushX.value() or direction=="f": #not touching edge
            self.board.motorOn(1, direction, self.speed)
            while step < abs(num) and not stop:
                utime.sleep(0.3)
                if stopFunc!=None: stop=stopFunc
                if not self.pushX.value():
                    break
                step+=1
            
        self.board.motorOff(1)


pot = ADC(Pin(28))

def get_pressure():
    a=[]
    alpha = 0.1
    filtered_value = pot.read_u16()
    for i in range(50):
        raw_value = pot.read_u16()
        filtered_value = alpha * raw_value + (1 - alpha) * filtered_value
        a.append(raw_value)
        utime.sleep(0.005)
    print(sum(a)//50)

b=Move()
"""b.moveZ(-5)
utime.sleep(3)
b.moveZ(5)

b.moveX(-5)
utime.sleep(3)
b.moveX(5)"""