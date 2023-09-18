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
round=np.zeros((100,10))
i=0
while True:
    image=B.getSensor(type_="flat")
    #top= np.where(image > top, image, top)
    scaled_image=np.abs((image-np.mean(image))/(np.std(image)))*100  #(image-np.min(image))/(np.max(image)-np.min(image)) 
    scaled_image[scaled_image<100]=0
    plt.subplot(1, 2, 1)
    if i>=len(round):
        round=np.roll(round, -1,axis=0)
        round[-1]=B.getSensor(type_="round")
    else:
        round[i]=B.getSensor(type_="round")
    i+=1
    plt.cla()
    for j in range(len(round[0])):
        num=round[:,j].copy()
        #num=(num-np.min(num))/(np.max(num)-np.min(num))
        num=np.abs((num-np.mean(round,axis=1))/np.std(round,axis=1))
        plt.plot([k/5 for k in range(len(round))],num,label="sensor "+str(j+1))
    plt.title('Plot')

    plt.subplot(1, 2, 2)
    plt.imshow(image)
    plt.title('Image representation')

    # Adjust the spacing between subplots for better visualization
    plt.tight_layout()

    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        break
    plt.pause(0.1)