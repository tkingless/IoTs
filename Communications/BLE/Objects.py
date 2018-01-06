import sys
sys.path.append("/usr/lib/python2.7/dist-packages")

import Advertising
import GATT
import array

class RobotdAdvertisement(Advertising.Advertisement):

    def __init__(self, bus, index):
        Advertising.Advertisement.__init__(self, bus, index, 'peripheral')
        #self.add_service_uuid('180D')
        #self.add_service_uuid('180F')
        #self.add_manufacturer_data(0xffff, [0x00, 0x01, 0x02, 0x03, 0x04])
        #self.add_service_data('9999', [0x00, 0x01, 0x02, 0x03, 0x04])
        self.add_local_name('Robotd')
        self.include_tx_power = True

class RobotdService(GATT.Service):
    _UUID = "fa09f5e9-e97c-4bba-af12-3f23590311e1"

    def __init__(self, bus, index):
        GATT.Service.__init__(self, bus, index, self._UUID, True)
        self.add_characteristic(RobotdEmotionCharc(bus, 0, self))

class RobotdEmotionCharc(GATT.Characteristic):
    """
    This charc for emotion read/write
    """
    _UUID = '8c95a57f-6f82-4d0d-8aba-2de700ce7ad1'

    def __init__(self, bus, index, service):
        GATT.Characteristic.__init__(self, bus, index,
            self._UUID,['write'],service)
        self.add_descriptor(RobotdEmotionDesc(bus, 0, self))

    def WriteValue(self, value, options):
        print('WriteValue() called')

        if len(value) != 1:
            raise InvalidValueLengthException()

        byte = value[0]
        #print('Written value: ' + repr(byte))
        print('Written value: ' + repr(byte))
        return

class RobotdEmotionDesc(GATT.Descriptor):
    """
    Characteristic descriptor for RbotodEmotion, use Nordic's RF Connect to test
    """
    _UUID = '8c95a57f-6f82-4d0d-8aba-2de700ce7ad2'

    def __init__(self, bus, index, characteristic):
        GATT.Descriptor.__init__(self, bus, index, self._UUID,
            ['read'], characteristic)

    def ReadValue(self, options):
        return array.array('B', b'Rotbod Emotion Writing')
    
#Testing code only
import dbus
import dbus.service
import dbus.mainloop.glib
import gobject

def register_ad_cb():
    print 'Advertisement registered'

def register_ad_error_cb(error):
    print 'Failed to register advertisement: ' + str(error)
    mainloop.quit()
    
mainloop = None

#Advertisment impl
##def main():
##    global mainloop
##
##    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
##
##    ad_manager = Advertising.get_advertisingMng()
##
##    bus = dbus.SystemBus()
##    test_advertisement = TestAdvertisement(bus, 0)
##
##    mainloop = gobject.MainLoop()
##
##    try:
##        ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
##                                         reply_handler=register_ad_cb,
##                                         error_handler=register_ad_error_cb)
##    except:
##        print(ad_manager)
##
##    mainloop.run()

#GATT service impl
try:
  from gi.repository import GLib
except ImportError:
  import gobject as GLib

def register_app_cb():
    print('GATT application registered')

def register_app_error_cb(error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()
 
def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    gatt_service_manager = GATT.get_GATTmng()

    bus = dbus.SystemBus()
    app = GATT.GATTrootApp(bus)
    app.add_service(RobotdService(bus,0))

    mainloop = GLib.MainLoop()

    print('Registering GATT application...')

    #this is not registering the Application dbus service object on systembus,
    #it is enrolled into bluez's, tutorial way to register a dbus service,
    #see the Expt/dbusTest.py, need dbus.Bus.request_name()
    gatt_service_manager.RegisterApplication(app.get_path(), {},
                                    reply_handler=register_app_cb,
                                    error_handler=register_app_error_cb)

    mainloop.run()
