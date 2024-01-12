from gonkController import *

droid=gonk()
droid.display_face(droid.eye)
print(droid.getGyro())
print("Temperature:",droid.temp)
print("Recording")
droid.reset()
name="accmovementLeftFootDay6.csv"
droid.createFile(name,["time_step","x","y","z"]+["s_1_"+str(i) for i in range(16)]+["s_2_"+str(i) for i in range(16)])
epochs=100
t=time.time()
droid.move(0,15)
for i in range(epochs):
    print(i,time.time()-t)
    t=time.time()
    for j in range(25,80):
        d=droid.filter(droid.getFeet())
        droid.move(3,j)
        droid.writeData(name)
        #print(d)
    for j in reversed(range(25,80)):
        d=droid.filter(droid.getFeet())
        droid.move(3,j)
        droid.writeData(name)
        #print(d)
#"""
"""
inverse
"""
name="accmovementRightFootDay5.csv"
droid.createFile(name,["time_step","x","y","z"]+["s_1_"+str(i) for i in range(16)]+["s_2_"+str(i) for i in range(16)])

droid.move(3,130)
for i in range(epochs):
    print(i,time.time()-t)
    t=time.time()
    for j in range(60,100):
        d=droid.filter(droid.getFeet())
        droid.move(0,j)
        droid.writeData(name)
        #print(d)
    for j in reversed(range(60,100)):
        d=droid.filter(droid.getFeet())
        droid.move(0,j)
        droid.writeData(name)
        #print(d)
#"""
print("Finished")

