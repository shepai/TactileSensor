
import numpy as np
import serial

# Define the serial port (you might need to change this depending on your system)
#serial_port = "/dev/ttyUSB0"  # Linux
serial_port = "COM7"  # Windows (replace X with the actual COM port number)

# Create a serial connection
ser = serial.Serial(serial_port, 9600)
print("connected..")
try:
    while True:
        # Read data from the serial port
        if ser.inWaiting() > 0:
            data=ser.readline()
            #data = ser.readline().decode('utf-8').strip()
            # Print the received data
            print("Received:", data)

except KeyboardInterrupt:
    print("Serial communication terminated.")

finally:
    ser.close()  # Close the serial connection when done


"""
import usb_cdc
usb_cdc.enable(console=True, data=True)

"""