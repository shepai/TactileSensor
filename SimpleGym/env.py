import numpy as np
import noise
import math

def sigmoid(x):
    return 1/(1+math.e**(-x))

def generateWorld(SIZE):
    shape = (SIZE,SIZE)
    scale = 100.0
    octaves = 10 #rnd.randint(2,20)
    persistence = 0.7
    lacunarity = 2

    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.pnoise2(i/scale, 
                                        j/scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        repeatx=1024, 
                                        repeaty=1024, 
                                        base=42)
    world=world.astype(float)
    #print("Octaves:",octaves)
    return sigmoid(np.array(world))+1


def genFlat(SIZE):
    return np.ones((SIZE,SIZE))+np.random.normal(0,0.5,(SIZE,SIZE))

def genObs(SIZE):
    x=np.ones((SIZE,SIZE))+np.random.normal(0,0.1,(SIZE,SIZE))
    x[50:100,0:100]+=2
    return x