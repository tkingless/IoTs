import threading
from Networks import networking
import time

class UARTadapter(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.HaveReceivedValue = False
        self.uart = networking.UARTobj(23,24)
        return

    def run(self):
        while self.HaveReceivedValue is False:
            (cnt,readBytes) = self.uart.ReadBytes()
            time.sleep(float(0.02))
            if cnt > 0:
                self.HaveReceivedValue = True

        self.uart.Delete()
        return
    
def worker():
    print "Worker init"

    UARTadpt = UARTadapter()
    UARTadpt.start()

    while UARTadpt.isAlive():
        pass
    
    return

t = threading.Thread(target=worker)
t.start()
t.join()

print 'Main() finished'


            

    
    
