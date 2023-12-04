import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import torch
import torch.nn as nn
import torch.optim as optim


path="/its/home/drs25/TactileSensor/Code/Data collection/robot/"

torch.cuda.empty_cache() 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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
    X_train, X_test, Y_train, Y_test = train_test_split(X_.astype(np.float32)[0:100], y_.astype(np.float32)[0:100], test_size=0.2, random_state=42)
    X_train=torch.tensor(X_train).to(device)
    X_test=torch.tensor(X_test).to(device)
    Y_train=torch.tensor(Y_train).to(device)
    Y_test=torch.tensor(Y_test).to(device)
    return X_train, X_test, Y_train, Y_test
    
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # Forward propagation
        out, _ = self.lstm(x, (h0, c0))

        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out
    
#prep data
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
#split
X_train, X_test, Y_train, Y_test = getAugmentedData(X,y,50)
X_train=torch.tensor(X_train).to(device)
X_test=torch.tensor(X_test).to(device)
Y_train=torch.tensor(Y_train).to(device)
Y_test=torch.tensor(Y_test).to(device)

def train(X_train,Y_train,X_test,Y_test,num_epochs = 100,learning_rate = 0.001):
    # Split your dataset into training and validation sets
    # train_data, val_data = ...
    lstm_model=LSTMModel(X_train.shape[2],50,2,Y_train.shape[1]).to(device)
    # Create data loaders for training and validation

    # Initialize the optimizer
    optimizer = optim.SGD(lstm_model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()
    history_train=[]
    history_test=[]
    # Training loop
    for epoch in range(num_epochs):
        lstm_model.train()

        optimizer.zero_grad()
        # Forward pass
        outputs = lstm_model(X_train)

        # Calculate the loss
        loss = criterion(outputs, Y_train)

        # Backpropagation
        loss.backward()
        optimizer.step()

        total_loss = loss.item()
        history_train.append(total_loss)
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss:.4f}")

        # Validation
        lstm_model.eval()
        with torch.no_grad():
            total_val_loss = 0

            outputs = lstm_model(X_test)
            val_loss = criterion(outputs, Y_test)
            total_val_loss = val_loss.item()

            print(f"Validation Loss: {total_val_loss:.4f}")
            history_test.append(total_val_loss)
    # Save the trained model
    torch.save(lstm_model.state_dict(), path+"GPUCluster/data/"+"lstm_model.pth")
    return np.array(history_train), np.array(history_test)

lossTrain,lossTest=train(X_train,Y_train,X_test,Y_test,num_epochs = 10000,learning_rate = 0.001)

np.save(path+"GPUCluster/data/train_loss",lossTrain)
np.save(path+"GPUCluster/data/test_loss",lossTest)
