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
top=np.ones((5,5))+B.getSensor(type_="flat")
past=B.getSensor(type_="flat")
i=0
while True:
    image=B.getSensor(type_="flat")
    top = np.where(image < top, image,top)
    matrix=(image-top )/np.max(image) 
    #print(np.diff(np.array([past.flatten(),image.flatten()]),axis=0).shape)
    #matrix=1 * np.diff(np.array([past.flatten(),image.flatten()]),axis=0).reshape(5,5)
    matrix[matrix<0.2]=0
    #matrix[matrix>255]=255
    past=matrix.copy()
    plt.imshow(matrix)
    plt.axis('off')
    plt.pause(0.1)
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        break