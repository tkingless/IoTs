from Communications import Protocols
import time
import numpy as np

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
        try:
            calpos = self.CalibratedYMXC(pos)
            PIobj.set_servo_pulsewidth(self.pin,calpos)
        except:
            PIobj.set_servo_pulsewidth(self.pin,pos)
            
        return

    def Calibrate(self,zero,clk,antiClk):
        self.zero = zero
        #small number
        self.clk = clk
        #large number
        self.antiClk = antiClk

        x = np.array([500,1500,2500])
        y = np.array([self.clk,self.zero,self.antiClk])
        A = np.vstack([x,np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A,y)[0]
        self.m = m
        self.c = c
        return

    def CalibratedYMXC(self,x):
        if x == 0:
            return 0
        y = int(self.m * x + self.c)
        y = max(min(y,self.antiClk),self.clk)
        return y
    
    def Delete(self):
        self.WritePos(0)
        return

import threading
from numpy import interp as Interpolate

class ServoCtlr(threading.Thread):

    cooldownInterval = 50
    aniSampleTime = 50

    def __init__(self,servo):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.servo = servo
        self.isAlive = True
        
        #Animation Params
        self.isAnimating = False
        self.tp = None #checkout numpy interp from SciPy.org 
        self.rp = None
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
                        
                        if(tmp >= self.tp[-1]):
                            self.isAnimating = False
                            
                        self.servo.WritePos(
                            Interpolate(int(tmp),self.tp.tolist(),
                                        self.rp.tolist(),right=1500))
                        self.lastSetTP = current_milli
            else:
                #Not Animating:
                if(current_milli - self.lastSetTP >= ServoCtlr.cooldownInterval and
                   self.lastSetTP > 0):
                    #auto Zero positioning
                    self.servo.WritePos(0)
                    self.lastSetTP = -1

            time.sleep(0.02)
        return

    def SetPos(self,pos):
        self.servo.WritePos(pos)
        return

    def Animate(self,tp,rp):
        """
        tp: time point array, rp: rotation point array
        """
        self.isAnimating = True
        self.aniStartOffStamp = ServoCtlr.GetMillis()
        self.tp = np.array(tp)
        self.rp = np.array(rp)
        return

    def TestAnimate1(self):
        tp = [0,250,500,750,1000]
        #note rp 1500 is supposed the current pos of motor
        rp = [1500,2300,1600,2300,1600]
        self.Animate(tp,rp)
        return

    def Terminate(self):
        #This object must Terminate() before release
        self.lock.acquire()
        try:
            #Ensure the ServoCtl main loop stop after this func
            self.isAlive = False
        finally:
            self.lock.release()
        self.servo.Delete()
        return

    #TODO put into Utility
    @staticmethod
    def GetMillis():
        return int(round(time.time() * 1000))
