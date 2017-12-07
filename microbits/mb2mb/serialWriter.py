from microbit import *

# Write your code here :-)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin0, rx=pin1)
while True:
    if button_a.is_pressed():
        uart.write('a')
