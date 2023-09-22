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
minimums=np.ones((10,))+B.getSensor(type_="round")
round=np.zeros((100,10))
past=B.getSensor(type_="flat")
i=0
while True:
    image=B.getSensor(type_="flat")
    data=B.getSensor(type_="round")
    top = np.where(image < top, image,top)
    minimums=np.where(data < minimums, data,minimums)
    matrix=(image-top )/np.max(image) 
    matrix[matrix<0.2]=0
    plt.subplot(1, 2, 1)
    if i>=len(round):
        round=np.roll(round, -1,axis=0)
        round[-1]=data-minimums
    else:
        round[i]=data-minimums
    i+=1
    plt.cla()
    for j in range(len(round[0])):
        num=round[:,j].copy()
        #num=(num-np.min(num))/(np.max(num)-np.min(num))
        #np.gradient(num)
        plt.plot([k/5 for k in range(len(round))],num,label="sensor "+str(j+1))
    plt.title('Plot')

    plt.subplot(1, 2, 2)
    plt.imshow(matrix)
    plt.axis('off')
    plt.title('Image representation')
    past=image.copy()
    # Adjust the spacing between subplots for better visualization
    plt.tight_layout()
    plt.pause(0.1)
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        break