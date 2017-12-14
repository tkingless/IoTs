#Define communication objs
import pigpio as pigpio

baudRate = 9600
bits = 8
PIobj = pigpio.pi()

class UARTobj(object):

	def __init__(self,TX,RX):

		self.TX = TX
		self.RX = RX
		self.wid = None

		PIobj.set_mode(TX,pigpio.OUTPUT)
		PIobj.set_mode(RX,pigpio.INPUT)

        def WriteBytes(self,data):
            self.configureWave(data)
            #wid is created
            PIobj.wave_send_once(self.wid)

        def configureWave(self,data):
            PIobj.wave_clear()
            PIobj.wave_add_serial(self.TX,baudRate,data)
            self.wid = PIobj.wave_create()

        def Delete(self):
            PIobj.wave_delete(self.wid)
            PIobj.bb_serial_read_close(self.RX)
	#def run(self):
		#needed to be in main loop for serial reading
	#def WriteAbyte(self, val):
	#def ReadAbyte(self, aInput):
		#return None
