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
import signal
from Utilities.daemon import Daemon
from Communications import Protocols
from Communications.Protocols import UARTadapter
from Motor import Servo, ServoCtlr

class Robotd(Daemon):

    def __init__(self,pidFile):
        super(Robotd, self).__init__(pidFile,stdout='/tmp/Robot/stdout',
                                     stderr='/tmp/Robot/stderr',ospath='/tmp/Robot')
        signal.signal(signal.SIGUSR1,self.Terminate)
        signal.siginterrupt(signal.SIGUSR1, False)
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
        self.alive = True
        return

    def run(self):
        
        self.robotInit()
        
        while self.alive:
            self.Leyebrow.Animate()
            print('Robot running... ',os.getpid())
            time.sleep(3)
            
        return

    #The signal callback must match the parameters
    def Terminate(self,signum,frame):
        print('Robot Terminating... ',os.getpid())
        self.alive = False
        self.Leyebrow.Terminate()
        self.LmicroBit.Terminate()
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
