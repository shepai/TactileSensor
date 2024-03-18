import TactileSensor as ts
import time
import numpy as np
import keyboard  # using module keyboard
import cv2

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()
x=[]
y=[]
def calibrate(num=100):
    image=B.getSensor(type_="foot")
    reduction_matrix=np.zeros_like(image)
    for i in range(num):
        reduction_matrix+=B.getSensor(type_="foot")
    return reduction_matrix/num

rm=calibrate()
print("Begin")
i=0
scale_factor=100
while True:
    image=B.getSensor(type_="foot")
    matrix=image.copy()-rm
    matrix[matrix<0]=0
    matrix=(matrix-np.min(matrix))/(np.max(matrix)-np.min(matrix))
    #matrix=(matrix-np.mean(matrix))/(np.std(matrix))
    #matrix[matrix<np.mean(matrix)-np.std(matrix)]=0
    #print(np.mean(matrix))
    #matrix[matrix>0.2]=matrix[matrix>0.2]*255
    #plt.imshow(matrix,cmap='coolwarm')
    #plt.axis('off')
    #plt.pause(0.01)
    height, width = matrix.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Resize the image using linear interpolation
    resized_img = cv2.resize(matrix, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    resized_img2 = cv2.resize(matrix, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    cv2.imshow('interpolated', resized_img)
    cv2.imshow('sensor', resized_img2)
    q=cv2.waitKey(1) 
    if q & 0xFF == ord('q'):
        break
    if keyboard.is_pressed('n'):  # if key 'q' is pressed qqqqq q
        print("north label")
        x.append(matrix)
        y.append([1,1,0,0])
    if keyboard.is_pressed('e'):  # if key 'q' is pressed qqqqq q
        print("east label")
        x.append(matrix)
        y.append([0,1,1,0])
    if keyboard.is_pressed('x'):  # if key 'q' is pressed qqqqq q
        print("south label")
        x.append(matrix)
        y.append([0,0,1,1])
    if keyboard.is_pressed('w'):  # if key 'q' is pressed qqqqq q
        print("west label")
        x.append(matrix)
        y.append([1,0,0,1])
    if keyboard.is_pressed('1'):  # if key 'q' is pressed qqqqq q
        print("north-east label")
        x.append(matrix)
        y.append([1,1,1,0])
    if keyboard.is_pressed('2'):  # if key 'q' is pressed qqqqq q
        print("south-east label")
        x.append(matrix)
        y.append([0,1,1,1])
    if keyboard.is_pressed('3'):  # if key 'q' is pressed qqqqq q
        print("south-west label")
        x.append(matrix)
        y.append([1,0,1,1])
    if keyboard.is_pressed('4'):  # if key 'q' is pressed qqqqq q
        print("north-west label")
        x.append(matrix)
        y.append([1,1,0,1])
    
x=np.array(x)
y=np.array(y)

filepath="C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/edges/"

np.save(filepath+"xdata_soft1",x)
np.save(filepath+"ydata_soft1",y)