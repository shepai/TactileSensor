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
top=np.ones((5,5))
round=np.zeros((5,5))
i=0
while True:
    image=B.getSensor(type_="flat")
    #top= np.where(image > top, image, top)
    scaled_image=np.abs((image-np.mean(image))/(np.std(image)))*100  #(image-np.min(image))/(np.max(image)-np.min(image)) 
    scaled_image[scaled_image<100]=0
    plt.imshow(scaled_image)
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        break
    plt.pause(0.1)