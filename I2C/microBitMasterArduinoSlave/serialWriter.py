from microbit import *

# Write your code here :-)
while True:
    if button_a.is_pressed():
        i2c.write(0x08,b'Kathy')
