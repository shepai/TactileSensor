import TactileSensor as ts
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#import keyboard
matplotlib.use('TkAgg')
import pickle
# Specify the filename to save the model
model_filename = 'C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/pressures/regression_model.pkl'

with open(model_filename, 'rb') as model_file:
    loaded_model = pickle.load(model_file)

B=ts.Board()
#get serial boards and connect to first one
B.autoConnect()

round=np.zeros((10,10))
i=0
for i in range(10):
    round[i]=B.getSensor(type_="round")
while True:
    round=np.roll(round, -1,axis=0)
    round[-1]=B.getSensor(type_="round")
    coords=loaded_model.predict(round.reshape((1,100)))
    coords=np.round(coords,0)[0].reshape((2,2))
    plt.cla()
    plt.imshow(coords)
    plt.title("Prediction")
    plt.pause(0.1)

