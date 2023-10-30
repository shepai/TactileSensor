import controller
import sys
import numpy as np
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/TactileSensor/Code/')
#import TactileSensor as ts
import time
from pynput import keyboard


B=controller.Board()
#get serial boards and connect to first one
B.autoConnect()
B.runFile("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Rig/boardSide.py")

def on_press(key):
    if key == keyboard.Key.right:
        # Stop listener
        print("move")
        B.moveX(1)
    elif key == keyboard.Key.left:
        # Stop listener
        B.moveX(-1)
    elif key == keyboard.Key.up:
        # Stop listener
        B.moveZ(1)
    elif key == keyboard.Key.down:
        # Stop listener
        B.moveZ(-1)

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
)


