import threading
from Networks import networking
import time

class UARTadapter(threading.Thread):

    def __init__(self,TX,RX):
        threading.Thread.__init__(self)
        self.HaveReceivedValue = False
        self.uart = networking.UARTobj(TX,RX)
        self.callback = None
        return

    def run(self):
        while self.HaveReceivedValue is False:
            (cnt,readBytes) = self.uart.ReadBytes()
            time.sleep(float(0.02))
            if cnt > 0:
                #self.HaveReceivedValue = True
                WhenBytesRead(readBytes)

        #self.uart.Delete()
        return

    def WriteBytes(self,data):
        self.uart.WriteBytes(data)
        return

    def RegReadCB(self,cb):
        self.callback = cb
        return

    def WhenBytesRead(self,data):
        self.callback(data)
        return

    def Terminate(self):
        self.uart.Delete()
        self.HaveReceivedValue = True
"""    
def worker():
    print "Worker init"

    UARTadpt = UARTadapter(23,24)
    UARTadpt.start()

    while UARTadpt.isAlive():
        pass
    
    return

t = threading.Thread(target=worker)
t.start()
t.join()


print 'Main() finished'
"""

"""
Event Callback pattern test
"""

class Pub(object):

    def __init__(self,cb):
        self.callback = cb
        return

    def Raise(self,arg):
        self.callback(arg)
        return

class Sub(object):

    def __init__(self):
        return

    def CB (self,arg):
        print ("Hello {}".format(arg))

            

    
    
