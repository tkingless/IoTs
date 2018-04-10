#!/usr/bin/env python
from enum import Enum

class EventType(Enum):
    NORMAL='N'
    HAPPY='H'
    SAD='S'
    ANGRY='A'
    COUNT='C'

#TODO: not implemented yet
class ResponseType(Enum):
    OK='O'
    BAD='B'

import time
import sys
import os
import signal
import random
from collections import deque
from Utilities.daemon import Daemon
from Communications import Protocols
from Communications.Protocols import UARTadapter
from Communications.BLE.Objects import RobotdBLE
from Motor import Servo, ServoCtlr
from Buzzer import BuzzerObj,AngryMelody,HappyMelody,NormalMelody,SadMelody,BeepCountNote,BeepBeepNote
from RobotCounter import RobotCounter

class Robotd(Daemon):

    def __init__(self,pidFile):
        super(Robotd, self).__init__(pidFile,stdout='/tmp/Robot/stdout',
                                     stderr='/tmp/Robot/stderr',ospath='/tmp/Robot')
        signal.signal(signal.SIGUSR1,self.Terminate)
        signal.siginterrupt(signal.SIGUSR1, False)
        #Don't know why, it is the process get killed with this signal, the motor signal reset
        #if not getting signal through process kill, it behave okay, process kill is for dev only
        signal.signal(signal.SIGUSR2,self.ShuffleState)
        signal.siginterrupt(signal.SIGUSR2, False)
        """This robot daemon initialization cannot put here, not belong to the daemon
        #self.LmicroBit = UARTadapter(23,24)
        #Lservo = Servo(4)
        #self.Leyebrow = ServoCtlr(Lservo)
        """
        #This illustrated that the following still belong to the parent process, only at run() of the daemon,
        #it is starting something belong to the daemon
        #fo = open("/tmp/Robot/init.txt","w")
        #fo.write("here is called 22\n")
        #fo.close()
        return

    def robotInit(self):
        print 'Robot Init....'
        #UARTadapter(TX,RX)
        self.LmicroBit = UARTadapter(23,24)
        self.RmicroBit = UARTadapter(18,25)
        Lservo = Servo(4)
        Rservo = Servo(12)
        #The calibration is empirical
        #Lservo.Calibrate(1425,575,2500)
        self.Leyebrow = ServoCtlr(Lservo)
        self.Reyebrow = ServoCtlr(Rservo)
        self.Buzzer = BuzzerObj(26)
        self.Counter = RobotCounter(self)
        self.alive = True

        self.stateQ = deque([])
        self.BLEadapter = RobotdBLE()
        self.BLEadapter.Enable()
        self.BLEadapter.AddEmotionWriteCallback(self.BLEemotionCB)
        self.BLEadapter.AddMinuteWriteCallback(self.BLEminuteCB)
        self.BLEadapter.AddSecondWriteCallback(self.BLEsecondCB)

        self.SetState(EventType.NORMAL)

        return
   
    def run(self):
        
        self.robotInit()
        
        while self.alive:
            #self.Leyebrow.Animate()
            #print('Robot running... ',os.getpid())
            time.sleep(0.02)
            if self.IsBusyToAppendState() != True:
                self.CheckBLEState()
            pass
            
        return

    #The signal callback must match the parameters
    def Terminate(self,signum,frame):
        print('Robot Terminating... ',os.getpid())
        self.alive = False
        self.Leyebrow.Terminate()
        self.Reyebrow.Terminate()
        self.LmicroBit.Terminate()
        self.RmicroBit.Terminate()
        self.BLEadapter.Disable()
        return
    
    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process       
        try:
            while 1:
                os.kill(pid, signal.SIGUSR1)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)

    #Deprecated
    def ShuffleState(self,signum,frame):
#        li = ['N', 'H', 'S', 'A']
#        dataEvt = self.curEvt
#        
#        while self.curEvt is dataEvt:
#            dataEvt = EventType(random.choice(li))
#  
#        self.SetState(dataEvt)
        return

    def BLEemotionCB(self,writeVal):
        #self.BLEemotionValue = writeVal
        if len(self.stateQ) < 5:
            print('stateQ append state: {0}'.format(writeVal))
            self.stateQ.append(writeVal)

    def BLEminuteCB(self,writeVal):
        self.counterMin = writeVal

    def BLEsecondCB(self,writeVal):
        self.counterSec = writeVal

    def CheckBLEState(self):
        try:
            if len(self.stateQ) > 0:
                self.BLEemotionValue = self.stateQ.popleft()
                self.curEvt = EventType(self.BLEemotionValue)
                self.SetState(self.curEvt)
                print('CheckState() from BLE, SetState() ',self.BLEemotionValue)
        except:
            pass

    def IsBusyToAppendState(self):
        if self.Leyebrow.isAnimating or self.Reyebrow.isAnimating or \
        (self.Counter.IsCounting() is True):
            return True
        return False

    def SetState(self,eventEnum):

        self.curEvt = eventEnum
        data = eventEnum.value
        self.LmicroBit.WriteBytes(data)
        self.RmicroBit.WriteBytes(data)

        tp = None
        rp = None
        rrp = None
        #About Motor:
        if eventEnum is EventType.NORMAL:
            tp = [0,250,2000]
            rp = [1500,1500,1500]
            rrp = [1500,1500,1500]
        elif eventEnum is EventType.HAPPY:
            tp = [0,200,1100,1500,2000,2200,3200]
            rp = [1500,2000,1600,2300,1600,2300,1600]
            rrp = [1500,1000,1400,700,1400,700,1400]
        elif eventEnum is EventType.SAD:
            tp = [0,1000,2500]
            rp = [1500,1200,1200]
            rrp = [1500,1800,1800]

        elif eventEnum is EventType.ANGRY:
            tp = [0,500,2000]
            rp = [1500,2200,2200]
            rrp = [1500,800,800]

        if tp is not None and \
        rp is not None and \
        rrp is not None:
            self.Leyebrow.Animate(tp,rp)
            self.Reyebrow.Animate(tp,rrp)

        if eventEnum is EventType.COUNT:
            self.Counter.StartCountDown(self.counterMin,self.counterSec)
        
        if eventEnum is EventType.NORMAL:
            self.PlayMelodyNonBlocking(NormalMelody)
        elif eventEnum is EventType.HAPPY:
            self.PlayMelodyNonBlocking(HappyMelody)
        elif eventEnum is EventType.SAD:
            self.PlayMelodyNonBlocking(SadMelody)
        elif eventEnum is EventType.ANGRY:
            self.PlayMelodyNonBlocking(AngryMelody)

        return

    def SwipeEyesOnCounting(self):
        if self.Leyebrow.isAnimating or self.Reyebrow.isAnimating:
            return

        tp = [0,50,400]
        rp = [1500,2300,1500]
        rrp = [1500,700,1500]

        self.Leyebrow.Animate(tp,rp)
        self.Reyebrow.Animate(tp,rrp)

    def PlayMelodyNonBlocking(self, melody):
        #non-blockingly play sound
        import threading
        soundThread = None
        buzzer = self.Buzzer

        soundThread = threading.Thread(target=buzzer.PlayMelody,args=(melody,))

        if soundThread is not None:
            soundThread.start()

        return

if __name__ == "__main__":

    print('pid: ',os.getpid())
    daemon = Robotd('/tmp/robotDaemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print 'Robotd start'
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        print 'Robotd parent process to detach'
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
