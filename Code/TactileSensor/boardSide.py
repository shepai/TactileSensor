import time
import board
import busio
import digitalio


# Create a UART object
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

while True:
    # Define the array to be sent
    data_array = [1, 2, 3, 4, 5]
    transmit=bytes(str(data_array)+"\n",'utf-8')
    # Send the data over UART
    uart.write(transmit)
    led.value = True  # Turn the LED on
    time.sleep(1)  # Wait for 1 second before sending again
    led.value = False  # Turn the LED off
    time.sleep(0.5)  # Wait for 0.5 seconds
