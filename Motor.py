from Communications import Protocols
import time

PIobj = Protocols.PIobj

class Servo(object):

    def __init__(self,servoPin):
        """
        servoPin: = GPIO
        """
        self.pin = servoPin
        return

    def WritePos(self,pos):
        """
        pos: = 0(off), 500 (most anti-clockwise) - 2500 (most clockwise)
            remember to set off if not using
        """
        PIobj.set_servo_pulsewidth(self.pin,pos)
        return

    def Calibrate(self,zero,clk,antiClk):
        self.zero = zero
        self.clk = clk
        self.antiClk = antiClk
        return

##    def Combo(self):
##        interval = 0.25
##        self.WritePos(1500)
##        time.sleep(float(interval))
##        self.WritePos(2200)
##        time.sleep(float(interval))
##        self.WritePos(1500)
##        time.sleep(float(interval))
##        self.WritePos(2200)
##        time.sleep(float(interval))
##        self.WritePos(1500)
##        time.sleep(float(interval))
##        self.WritePos(0)
##
##    def AutoZero(self):

    def Delete(self):
        self.WritePos(0)
        return

import threading
import numpy as np
from numpy import interp as Interpolate

class ServoCtlr(threading.Thread):

    cooldownInterval = 50
    aniSampleTime = 50

    def __init__(self,servo):
        threading.Thread.__init__(self)
        self.servo = servo
        self.isAlive = True
        
        #Animation Params
        self.isAnimating = False
        self.xp = None #checkout numpy interp from SciPy.org 
        self.fp = None
        self.aniStartOffStamp = 0
        self.aniLastUpdate = 0
        self.lastSetTP = 0
        
        self.start()
        return

    def run(self):
        while self.isAlive:

            current_milli = ServoCtlr.GetMillis()
            if self.isAnimating:
                if(current_milli >= self.aniStartOffStamp):
                    if(current_milli - self.aniLastUpdate >= ServoCtlr.aniSampleTime):
                        self.aniLastUpdate = current_milli

                        tmp = current_milli - self.aniStartOffStamp
                        
                        if(tmp >= self.xp[-1]):
                            self.isAnimating = False
                            
                        self.servo.WritePos(Interpolate(int(tmp),self.xp.tolist(),self.fp.tolist(),right=1500))
                        self.lastSetTP = current_milli
            else:
                #Not Animating:
                if(current_milli - self.lastSetTP >= ServoCtlr.cooldownInterval and
                   self.lastSetTP > 0):
                    #auto Zero positioning
                    self.servo.WritePos(0)
                    self.lastSetTP = -1
                    print('finish ani')
        return

    def Animate(self):
        self.isAnimating = True
        self.xp = np.array([0,250,500,750,1000])
        self.aniStartOffStamp = ServoCtlr.GetMillis()
        self.fp = np.array([1500,2300,1600,2300,1600])
        return

    def Terminate(self):
        #This object must Terminate() before release
        self.isAlive = False
        return

    #TODO put into Utility
    @staticmethod
    def GetMillis():
        return int(round(time.time() * 1000))
