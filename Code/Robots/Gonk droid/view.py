from gonkController import *

droid=gonk()
droid.display_face(droid.eye)
print(droid.getGyro())
print("Temperature:",droid.temp)
print("Recording")
droid.reset()
droid.createFile("movementLeftFoot.csv",["x","y","z","s1","s2","s3","s4","s5","s6"])
epochs=10000

for i in range(epochs):
    d=droid.filter(droid.getFeet())
    print(d)

print("Finished")

