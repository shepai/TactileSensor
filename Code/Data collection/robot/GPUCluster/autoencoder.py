import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import torch
import torch.nn as nn
import torch.optim as optim
import time
import sys

path="/its/home/drs25/Documents/GitHub/TactileSensor/Code/Data collection/robot/"
if sys.platform.startswith('win'):
    path="C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Data collection/robot/"

torch.cuda.empty_cache() 
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device=torch.device("cpu")
print(torch.version.cuda)
print("GPU:",torch.cuda.is_available())
def sort_data(name,vibration=True,dir="all"):
    df = pd.read_csv(path+name)
    df=pd.DataFrame(df).fillna(0)
    if vibration:
        x=np.array([df['s1'],df['s2'],df['s3'],df['s4'],df['s5'],df['s6']])
    else:
        x=np.array([df['s1'],df['s2'],df['s5'],df['s6']])
    if dir=="left":
        x=np.array([df['s1'],df['s2'],df['s3']])
    elif dir=="right":
        x=np.array([df['s4'],df['s5'],df['s6']])
    x=x.T #transpose to have layers
    y=np.array([df['x'],df['y'],df['z']])
    y=y.T
    nan_indices = np.where(np.isnan(y))
    y[nan_indices]=0
    print("X data:",x.shape,"/ny data:",y.shape)
    return x,y


def gen_temporal_data_2(X_,y_,T):
    X=X_.copy()
    temp_x=np.zeros((X.shape[0]-T,T,X.shape[1]))
    temp_y=np.zeros((X.shape[0]-T,y_.shape[1]))
    for j in range(len(y_)-T): #loop through classes
        ar=[X[j+k] for k in range(T)]
        temp_x[j]=np.array(ar)
        temp_y[j]=y_[j]
    x=temp_x
    y=temp_y
    return x, y


def augmented_pattern(x,y):
    isMod=False
    while not isMod:
        chunk_size=np.random.randint(5,100)
        if len(x[0])%chunk_size==0:
            isMod=True
    repetitions=np.random.randint(3,5)
    print(chunk_size)
    randomized_x = []
    randomized_y = []
    
    for idx, pattern in enumerate(x):
        pattern_length = len(pattern)
        num_chunks = pattern_length // chunk_size
        
        # Split pattern into chunks of size chunk_size
        chunks = [pattern[i * chunk_size: (i + 1) * chunk_size] for i in range(num_chunks)]
        
        for _ in range(repetitions):
            # Shuffle the chunks randomly
            np.random.shuffle(chunks)
            # Concatenate the shuffled chunks to create a new pattern
            randomized_pattern = np.concatenate(chunks)
            
            # Store the randomized pattern and corresponding label
            randomized_x.append(randomized_pattern)
            randomized_y.append(y[idx])
    
    return np.array(randomized_x), np.array(randomized_y)
def augmented_noise(X_):
    X=X_.copy()
    return X+np.random.normal(np.average(X),np.std(X)+1,X.shape)

def getAugmentedData(X,y,T):
    x,y=gen_temporal_data_2(X,y,T)
    x1=augmented_noise(x)
    x2,y1=augmented_pattern(x,y)
    x=np.concatenate([x,x1,x2])
    y=np.concatenate([y,y,y1])
    #reduction
    X_=(x-np.average(x))/np.std(x)
    y_=(y-np.average(y))/np.std(y)
    #split
    X_train, X_test, Y_train, Y_test = train_test_split(X_.astype(np.float32), y_.astype(np.float32), test_size=0.2, random_state=42)
    X_train=torch.tensor(X_train).to(device)
    X_test=torch.tensor(X_test).to(device)
    Y_train=torch.tensor(Y_train).to(device)
    Y_test=torch.tensor(Y_test).to(device)
    return X_train, X_test, Y_train, Y_test

def getData(X,y,T):
    X_,y_=gen_temporal_data_2(X,y,T)
    #reduction
    X_=(X_-np.average(X_))/np.std(X_)
    y=(y-np.average(y))/np.std(y)
    #split
    X_train, X_test, Y_train, Y_test = train_test_split(X_.astype(np.float32), y_.astype(np.float32), test_size=0.2, random_state=42)
    X_train=torch.tensor(X_train)
    X_test=torch.tensor(X_test)
    Y_train=torch.tensor(Y_train)
    Y_test=torch.tensor(Y_test)
    return X_train, X_test, Y_train, Y_test
# Define your Autoencoder class
class Autoencoder(nn.Module):
    def __init__(self, input_size, latent_size):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, latent_size),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_size, input_size),
            nn.ReLU(),
            nn.Linear(input_size, input_size)  # Output size is 3
        )
        #self.endlayer = nn.linear(input_size,output_size)

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded



X,y=sort_data("accmovementLeftFoot.csv")
X1,y1=sort_data("accmovementRightFoot.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementRightFootCarpet.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementLeftFootCarpet.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementRightFootConrete.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementLeftFootConrete.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementRightFootOutdoor.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementLeftFootOutdoor.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementLeftFootCarpetDay2.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementRightFootCarpetDay2.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementLeftFootCarpetDay3.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementRightFootCarpetDay3.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementLeftFootDay4.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)
X1,y1=sort_data("accmovementRightFootDay4.csv")
X=np.concatenate((X,X1),axis=0)
y=np.concatenate((y,y1),axis=0)

X_train, X_test, Y_train, Y_test=getAugmentedData(X,y,50)
# Initialize the autoencoder
input_size = 50 * 6
latent_size = 64  # Choose an appropriate size for the latent space
autoencoder = Autoencoder(input_size, latent_size).to(device)

# Reshape data for the autoencoder
x = X_train.view(-1, input_size)

# Define your optimizer and loss function
optimizer = torch.optim.SGD(autoencoder.parameters(), lr=0.001)
criterion = nn.MSELoss()

batch_size=32

# Training loop
num_epochs = 5000
history=[]
try:
    for epoch in range(num_epochs):
        # Forward pass
        for i in range(0, len(X_train), batch_size):
            inputs = x[i:i + batch_size]
            targets = Y_train[i:i + batch_size]

            output = autoencoder(inputs)

            # Calculate the loss
            #loss_x = criterion(output, x)
            loss = criterion(output, inputs)  # Use only the first 3 elements for Y
            #loss = loss_x + loss_y  # Combine both losses
            # Backpropagation and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            history.append(loss.item())
            # Print progress
        if epoch%100==0:
                print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}")
except KeyboardInterrupt:
    pass
      

torch.save(autoencoder.state_dict(), path+"GPUCluster/data/"+"autoencoder_model.pth")

np.save(path+"GPUCluster/data/train_loss",np.array(history))