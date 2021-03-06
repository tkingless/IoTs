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
        self.add_local_name('Robotd_EdUHK')
        self.include_tx_power = True

class RobotdService(GATT.Service):
    _UUID = "fa09f5e9-e97c-4bba-af12-3f23590311e1"

    def __init__(self, bus, index):
        GATT.Service.__init__(self, bus, index, self._UUID, True)
        self.add_characteristic(RobotdEmotionCharc(bus, 0, self))
        self.add_characteristic(RobotdCounterMinCharc(bus, 1, self))
        self.add_characteristic(RobotdCounterSecCharc(bus, 2, self))

class RobotdEmotionCharc(GATT.Characteristic):
    """
    This charc for emotion read/write
    """
    _UUID = '8c95a57f-6f82-4d0d-8aba-2de700ce7ad1'

    def __init__(self, bus, index, service):
        GATT.Characteristic.__init__(self, bus, index,
            self._UUID,['write'],service)
        self.add_descriptor(RobotdEmotionDesc(bus, 2, self))
        self.writeStrDelegate = None

    def SubscribeDele(self,cb):
        self.writeStrDelegate = cb

    def WriteValue(self, value, options):

        if len(value) != 1:
            raise InvalidValueLengthException()

        byte = value[0]
        print('Emotion charc, written value: ' + repr(byte))
        if self.writeStrDelegate is not None:
            self.writeStrDelegate(chr(byte))
            
        return

class RobotdEmotionDesc(GATT.Descriptor):
    """
    Characteristic descriptor for RbotodEmotion, use Nordic's RF Connect to test
    """
    _UUID = '2901'

    def __init__(self, bus, index, characteristic):
        self.value = array.array('B', b'Robotd Emotion Write')
        self.value = self.value.tolist()
        GATT.Descriptor.__init__(self, bus, index, self._UUID,
            ['read'], characteristic)

    def ReadValue(self, options):
        return self.value

class RobotdCounterMinCharc(GATT.Characteristic):
    """
    This charc for counter's minutes read/write/notify
    Impletation logic: When central writing a value on the char and also the second charc,
        central also write 'C' to start count down, changing the robotd's state
        the central also subscribe to these charcs, get notified
    """
    _UUID = '6758ffd3-9458-4b13-95a2-df1093cc818d'

    def __init__(self, bus, index, service):
        GATT.Characteristic.__init__(self, bus, index,
            self._UUID,['write','notify'],service)
        self.add_descriptor(RobotdCounterMinDesc(bus, 2, self))
        self.writeIntDelegate = None

        self.notifying = False
        self.minuteVal = 1

    def SubscribeDele(self,cb):
        self.writeIntDelegate = cb

    def WriteValue(self, value, options):

        if len(value) != 1:
            raise InvalidValueLengthException()

        byte = value[0]
        print('Min charc, written value: ' + repr(byte))
        if self.writeIntDelegate is not None:
            self.writeIntDelegate(int(byte))
            
        return

    def StartNotify(self):
        self.notifying = True

    def StopNotify(self):
        self.notifying = False

    def notify_minute_value(self):
        if not self.notifying:
            return

        self.PropertiesChanged(
                GATT.GATT_CHRC_IFACE,
                { 'Value': [dbus.Byte(self.minuteVal)] }, [])


class RobotdCounterMinDesc(GATT.Descriptor):
    """
    Characteristic descriptor for Robotd's counter min, use Nordic's RF Connect to test
    """
    _UUID = '2902'

    def __init__(self, bus, index, characteristic):
        self.value = array.array('B', b'Robotd Minute RWN')
        self.value = self.value.tolist()
        GATT.Descriptor.__init__(self, bus, index, self._UUID,
            ['read'], characteristic)

    def ReadValue(self, options):
        return self.value

class RobotdCounterSecCharc(GATT.Characteristic):

    _UUID = '705b7354-a93e-4257-9e77-a371c15479b4'

    def __init__(self, bus, index, service):
        GATT.Characteristic.__init__(self, bus, index,
            self._UUID,['write','notify'],service)
        self.add_descriptor(RobotdCounterSecDesc(bus, 2, self))
        self.writeIntDelegate = None

        self.notifying = False
        self.secondVal = 1

    def SubscribeDele(self,cb):
        self.writeIntDelegate = cb

    def WriteValue(self, value, options):

        if len(value) != 1:
            raise InvalidValueLengthException()

        byte = value[0]
        print('Sec charc, written value: ' + repr(byte))
        if self.writeIntDelegate is not None:
            self.writeIntDelegate(int(byte))
            
        return

    def StartNotify(self):
        self.notifying = True

    def StopNotify(self):
        self.notifying = False

    def notify_second_value(self):
        if not self.notifying:
            return

        self.PropertiesChanged(
                GATT.GATT_CHRC_IFACE,
                { 'Value': [dbus.Byte(self.secondVal)] }, [])


class RobotdCounterSecDesc(GATT.Descriptor):

    _UUID = '2903'

    def __init__(self, bus, index, characteristic):
        self.value = array.array('B', b'Robotd Second RWN')
        self.value = self.value.tolist()
        GATT.Descriptor.__init__(self, bus, index, self._UUID,
            ['read'], characteristic)

    def ReadValue(self, options):
        return self.value
   
#Implementation of BLE GATT advertising service
import threading
import dbus
import dbus.service
import dbus.mainloop.glib

try:
  from gi.repository import GLib
except ImportError:
  import gobject as GLib

class RobotdBLE(threading.Thread):

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.mainloop = None

        #Getting Bluez's interface for advertising and GATT
        ad_manager = Advertising.get_advertisingMng()
        gatt_service_manager = GATT.get_GATTmng()

        bus = dbus.SystemBus()

        #dbus service objects to be registered on Bluez's bus
        rbtd_advertisement = RobotdAdvertisement(bus, 0)
        GATTapp = GATT.GATTrootApp(bus)
        GATTapp.add_service(RobotdService(bus,0))

        self.mainloop = GLib.MainLoop()

        #AdvertiseManager interface has UnregisterAdvertisement(rbtd_advertisement.get_path())
        #this works to deregister the advertisement, to re-register, however need to
        #deregister the rbtd_advertisement's object path, rbtd_advertisement.remove_from_connection(0
        ad_manager.RegisterAdvertisement(rbtd_advertisement.get_path(), {},
            reply_handler=self.register_ad_cb,
            error_handler=self.register_ad_error_cb)

        #this is not registering the Application dbus service object on systembus,
        #it is enrolled into bluez's, tutorial way to register a dbus service,
        #see the Expt/dbusTest.py, need dbus.Bus.request_name()
        gatt_service_manager.RegisterApplication(GATTapp.get_path(), {},
            reply_handler=self.register_app_cb,
            error_handler=self.register_app_error_cb)


        #class members:
        self.ad_manager = ad_manager
        self.gatt_service_manager = gatt_service_manager
        self.rbtd_advertisement = rbtd_advertisement
        self.GATTapp = GATTapp

        threading.Thread.__init__(self)
        #TODO: Is this needed?
        self.setDaemon(True)

    def run(self):
        self.mainloop.run()

    def Enable(self):
        self.start()

    def Disable(self):
        self.ad_manager.UnregisterAdvertisement(self.rbtd_advertisement.get_path())
        self.rbtd_advertisement.remove_from_connection()
        self.gatt_service_manager.UnregisterApplication(self.GATTapp.get_path())
        self.GATTapp.ReleaseFromBluez()
##        self.GATTapp.remove_from_connection()
##        self.GATTapp.services[0].remove_from_connection()
##        self.GATTapp.services[0].characteristics[0].remove_from_connection()
##        self.GATTapp.services[0].characteristics[0].descriptors[0].remove_from_connection()
        self.mainloop.quit()
        return

    def AddEmotionWriteCallback(self,cb):
        self.GATTapp.services[0].characteristics[0].SubscribeDele(cb)

    def AddMinuteWriteCallback(self,cb):
        self.GATTapp.services[0].characteristics[1].SubscribeDele(cb)

    def AddSecondWriteCallback(self,cb):
        self.GATTapp.services[0].characteristics[2].SubscribeDele(cb)

    def GetMinuteCharc(self):
        return self.GATTapp.services[0].characteristics[1]

    def GetSecondCharc(self):
        return self.GATTapp.services[0].characteristics[2]

    def register_ad_cb(self):
        print 'Advertisement registered'

    def register_ad_error_cb(self,error):
        print 'Failed to register advertisement: ' + str(error)
        self.mainloop.quit()

    def register_app_cb(self):
        print('GATT application registered')

    def register_app_error_cb(self,error):
        print('Failed to register application: ' + str(error))
        self.mainloop.quit()
