#Define communication objs
import pigpio as pigpio
import time

baudRate = 115200
bits = 8
ten_char_time = 100.0/float(baudRate)
PIobj = pigpio.pi()

class UARTobj(object):

	def __init__(self,TX,RX):

	    self.TX = TX
	    self.RX = RX
	    self.wid = None

	    PIobj.set_mode(TX,pigpio.OUTPUT)
	    PIobj.set_mode(RX,pigpio.INPUT)

	    try:
                PIobj.bb_serial_read_close(self.RX)
            except:
                pass

	    PIobj.bb_serial_read_open(self.RX,baudRate,bits)

        def WriteBytes(self,data):
            self.configureWave(data)
            #wid is created
            PIobj.wave_send_once(self.wid)

        def ReadBytes(self):
            """
            str(data.decode()) to get string
            """
            #count = 1
            #bytess = bytearray()
            #while count:
                #(count,data) = PIobj.bb_serial_read(self.RX)  
                #if count:
                    #bytess.append(data)
                #time.sleep(ten_char_time)

            (count,data) = PIobj.bb_serial_read(self.RX)
            #print "count: {0} data: {1}".format(count,data)
                
            return count, data
            
        def configureWave(self,data):
            PIobj.wave_clear()
            PIobj.wave_add_serial(self.TX,baudRate,data)
            while PIobj.wave_tx_busy():
                pass
            self.wid = PIobj.wave_create()

        def Delete(self):
            if self.wid is not None:
                PIobj.wave_delete(self.wid)
            PIobj.bb_serial_read_close(self.RX)
            return

import threading
import time

class UARTadapter(threading.Thread):

    def __init__(self,TX,RX):
        threading.Thread.__init__(self)
        self.uart = UARTobj(TX,RX)
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
