import sys
sys.path.append("/usr/lib/python2.7/dist-packages")

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

try:
    from gi.repository import GLib
except ImportError:
    import gobject as GLib

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

OPATH = "/tmp/Test/object/path"
IFACE = "temp.Test.iface"
BUS_NAME = "temp.Test.busName"

class MyService(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        #bus = dbus.SystemBus() #is not allowed by configuration file
        bus.request_name(BUS_NAME, dbus.bus.NAME_FLAG_REPLACE_EXISTING)
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, OPATH)
    
    @dbus.service.method(dbus_interface=IFACE, in_signature="s")
    def Echo(self, message):
        return "received: " + message

if __name__ == "__main__":
    my_service = MyService()
    loop = GLib.MainLoop()
    loop.run()
