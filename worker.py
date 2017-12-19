import threading
from Communications import Protocols
import time

class UARTadapter(threading.Thread):

    def __init__(self,TX,RX):
        threading.Thread.__init__(self)
        self.uart = Protocols.UARTobj(TX,RX)
        self.userCB = None
        return

    def run(self):
        while self.userCB is not None:
            (cnt,readBytes) = self.uart.ReadBytes()
            time.sleep(float(0.02))
            if cnt > 0:
                self.WhenBytesRead(readBytes)

        return

    def WriteBytes(self,data):
        self.uart.WriteBytes(data)
        return

    def SetReadCB(self,cb):
        self.userCB = cb
        self.start()
        return

    def WhenBytesRead(self,data):
        self.userCB(data)
        return

    def Terminate(self):
        self.uart.Delete()
        self.userCB = None

            

    
    
