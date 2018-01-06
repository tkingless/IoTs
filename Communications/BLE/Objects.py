import sys
sys.path.append("/usr/lib/python2.7/dist-packages")

import Advertising
import GATT

class TestAdvertisement(Advertising.Advertisement):

    def __init__(self, bus, index):
        Advertising.Advertisement.__init__(self, bus, index, 'peripheral')
        #self.add_service_uuid('180D')
        #self.add_service_uuid('180F')
        #self.add_manufacturer_data(0xffff, [0x00, 0x01, 0x02, 0x03, 0x04])
        #self.add_service_data('9999', [0x00, 0x01, 0x02, 0x03, 0x04])
        self.add_local_name('TestAdvertisement')
        self.include_tx_power = True

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
def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    ad_manager = Advertising.get_advertisingMng()

    bus = dbus.SystemBus()
    test_advertisement = TestAdvertisement(bus, 0)

    mainloop = gobject.MainLoop()

    try:
        ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                         reply_handler=register_ad_cb,
                                         error_handler=register_ad_error_cb)
    except:
        print(ad_manager)

    mainloop.run()
