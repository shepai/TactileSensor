from gonkController import *

droid=gonk()
droid.display_face(droid.eye)
print(droid.getGyro())
print("Temperature:",droid.temp)
print("Recording")
droid.reset()
droid.createFile("movementLeftFoot.csv",["x","y","z","s1","s2","s3","s4","s5","s6"])
epochs=1000

for i in range(epochs):
    for j in range(30,130):
        d=droid.filter(droid.getFeet())
        droid.move(3,j)
        droid.writeData("movementLeftFoot.csv")
        print(d)
    for j in reversed(range(30,130)):
        d=droid.filter(droid.getFeet())
        droid.move(3,j)
        droid.writeData("movementLeftFoot.csv")
        print(d)

print("Finished")
