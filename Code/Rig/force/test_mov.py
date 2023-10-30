import controller
import time

B=controller.Board()
B.autoConnect()
B.runFile("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/Rig/boardSide.py")

B.moveZ(10)
B.moveZ(-10)

B.moveX(10)
B.moveX(-10)

