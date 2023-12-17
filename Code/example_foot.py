import TactileSensor as ts
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import keyboard  # using module keyboard

matplotlib.use('TkAgg')

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()

i=0
while True:
    image=B.getSensor(type_="foot")
    matrix=image.copy()
    matrix=(matrix-np.min(matrix))/(np.max(matrix)-np.min(matrix))
    plt.imshow(matrix)
    plt.axis('off')
    plt.pause(0.1)
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        break