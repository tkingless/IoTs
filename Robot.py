#!/usr/bin/env python
from enum import Enum

class EventType(Enum):
    NORMAL='N'
    HAPPY='H'
    SAD='S'
    ANGRY='A'

class ResponseType(Enum):
    OK='O'
    BAD='B'

import time
import sys
import os
from Utilities.daemon import Daemon
from Communications import Protocols
from Communications.Protocols import UARTadapter
from Motor import Servo, ServoCtlr

class Robotd(Daemon):

    def __init__(self,pidFile):
        super(Robotd, self).__init__(pidFile,stdout='/tmp/Robot/stdout',
                                     stderr='/tmp/Robot/stderr',ospath='/tmp/Robot')
        
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
        self.LmicroBit = UARTadapter(23,24)
        Lservo = Servo(4)
        self.Leyebrow = ServoCtlr(Lservo)
        return

    def run(self):
        
        self.robotInit()
        cnt = 1
        
        while cnt <= 2:
            self.Leyebrow.Animate()
            cnt += 1
            time.sleep(3)

        self.Leyebrow.Terminate()
        self.LmicroBit.Terminate()
        return

if __name__ == "__main__":
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
