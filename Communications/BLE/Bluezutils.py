import sys
sys.path.append("/usr/lib/python2.7/dist-packages")

import dbus
import dbus.exceptions

SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"

DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'

def get_managed_objects():
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/"),DBUS_OM_IFACE)
    return manager.GetManagedObjects()

def find_adapter(pattern=None):
    return find_adapter_in_objects(get_managed_objects(), pattern)

##def find_adapter_in_objects(objects, pattern=None):
##	bus = dbus.SystemBus()
##	for path, ifaces in objects.iteritems():
##		adapter = ifaces.get(ADAPTER_INTERFACE)
##		if adapter is None:
##			continue
##		if not pattern or pattern == adapter["Address"] or \
##							path.endswith(pattern):
##			obj = bus.get_object(SERVICE_NAME, path)
##			return dbus.Interface(obj, ADAPTER_INTERFACE)
##	raise Exception("Bluetooth adapter not found")

def find_adapter_in_objects(objects, pattern=None):
    bus = dbus.SystemBus()
    for path, props in objects.items():
	if pattern in props:
            return path
    raise Exception("Bluetooth adapter not found")

def find_device(device_address, adapter_pattern=None):
    return find_device_in_objects(get_managed_objects(), device_address, adapter_pattern)

def find_device_in_objects(objects, device_address, adapter_pattern=None):
    bus = dbus.SystemBus()
    path_prefix = ""
    if adapter_pattern:
	adapter = find_adapter_in_objects(objects, adapter_pattern)
	path_prefix = adapter.object_path
    for path, ifaces in objects.iteritems():
	device = ifaces.get(DEVICE_INTERFACE)
	if device is None:
	    continue
	if (device["Address"] == device_address and path.startswith(path_prefix)):
            obj = bus.get_object(SERVICE_NAME, path)
            return dbus.Interface(obj, DEVICE_INTERFACE)

    raise Exception("Bluetooth device not found")

#TODO: excpetions should be put into a file
class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.freedesktop.DBus.Error.InvalidArgs'


class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotSupported'


class NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotPermitted'


class InvalidValueLengthException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.InvalidValueLength'


class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.Failed'
