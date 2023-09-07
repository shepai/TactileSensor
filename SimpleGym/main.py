import numpy as np
import skin
import matplotlib.pyplot as plt

s=skin.sensor()
s.changeEnv(skin.env.genObs(200))

for i in range(50):
    im=s.getImage()
    plt.imshow(im)
    plt.title(np.average(im))
    plt.pause(0.1)
    s.move([5,5])
plt.show()