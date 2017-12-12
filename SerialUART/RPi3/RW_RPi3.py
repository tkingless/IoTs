#!/usr/bin/python
import wiringpi as wp
import time
wp.wiringPiSetup()
#RPi3 has changed things around a bit: ttyAMA0 now refers to the serial
#port that is connected to the bluetooth. The old serial port is now called ttyS0
serial = wp.serialOpen('/dev/serial0',9600)
wp.serialPuts(serial,'h')

time.sleep(4)

if (wp.serialDataAvail(serial) > 0):
    print( chr(wp.serialGetchar(serial)) )

wp.serialClose(serial)
