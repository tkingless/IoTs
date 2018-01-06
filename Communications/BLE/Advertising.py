import sys
sys.path.append("/usr/lib/python2.7/dist-packages")

import dbus
import dbus.service

import Bluezutils
from Bluezutils import InvalidArgsException
from Bluezutils import NotSupportedException
from Bluezutils import NotPermittedException
from Bluezutils import InvalidValueLengthException
from Bluezutils import FailedException

SERVICE_NAME = Bluezutils.SERVICE_NAME
LE_ADVERTISING_MANAGER_IFACE = SERVICE_NAME + '.LEAdvertisingManager1'
DBUS_OM_IFACE = Bluezutils.DBUS_OM_IFACE
DBUS_PROP_IFACE = Bluezutils.DBUS_PROP_IFACE

LE_ADVERTISEMENT_IFACE = SERVICE_NAME + '.LEAdvertisement1'

class Advertisement(dbus.service.Object):
    PATH_BASE = '/org/bluez/example/advertisement'

    def __init__(self, bus, index, advertising_type):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        #TODO: by example, the input is 'peripheral', check further
        #self.ad_type = advertising_type
        self.ad_type = 'peripheral'
        self.service_uuids = None
        self.manufacturer_data = None
        self.solicit_uuids = None
        self.service_data = None
        self.local_name = None
        self.include_tx_power = None
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        properties = dict()
        properties['Type'] = self.ad_type
        if self.service_uuids is not None:
            properties['ServiceUUIDs'] = dbus.Array(self.service_uuids,
                                                    signature='s')
        if self.solicit_uuids is not None:
            properties['SolicitUUIDs'] = dbus.Array(self.solicit_uuids,
                                                    signature='s')
        if self.manufacturer_data is not None:
            properties['ManufacturerData'] = dbus.Dictionary(
                self.manufacturer_data, signature='qv')
        if self.service_data is not None:
            properties['ServiceData'] = dbus.Dictionary(self.service_data,
                                                        signature='sv')
        if self.local_name is not None:
            properties['LocalName'] = dbus.String(self.local_name)
        if self.include_tx_power is not None:
            properties['IncludeTxPower'] = dbus.Boolean(self.include_tx_power)
        return {LE_ADVERTISEMENT_IFACE: properties}

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service_uuid(self, uuid):
        if not self.service_uuids:
            self.service_uuids = []
        self.service_uuids.append(uuid)

    def add_solicit_uuid(self, uuid):
        if not self.solicit_uuids:
            self.solicit_uuids = []
        self.solicit_uuids.append(uuid)

    def add_manufacturer_data(self, manuf_code, data):
        if not self.manufacturer_data:
            self.manufacturer_data = dbus.Dictionary({}, signature='qv')
        self.manufacturer_data[manuf_code] = dbus.Array(data, signature='y')

    def add_service_data(self, uuid, data):
        if not self.service_data:
            self.service_data = dbus.Dictionary({}, signature='sv')
        self.service_data[uuid] = dbus.Array(data, signature='y')

    def add_local_name(self, name):
        if not self.local_name:
            self.local_name = ""
        self.local_name = dbus.String(name)

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        print 'GetAll'
        if interface != LE_ADVERTISEMENT_IFACE:
            raise InvalidArgsException()
        print 'returning props'
        return self.get_properties()[LE_ADVERTISEMENT_IFACE]

    @dbus.service.method(LE_ADVERTISEMENT_IFACE,
                         in_signature='',
                         out_signature='')
    def Release(self):
        print '%s: Released!' % self.path

def get_adapter_advertisingMng():
    adapter = Bluezutils.find_adapter(LE_ADVERTISING_MANAGER_IFACE)
    return adapter

def get_advertisingMng():
    adapter_advMng = get_adapter_advertisingMng()

    if not adapter_advMng:
        print('LEAdvertisingManager1 interface not found')
        return

    sysBus = dbus.SystemBus()
    adapter_props = dbus.Interface(sysBus.get_object(SERVICE_NAME, adapter_advMng),DBUS_PROP_IFACE)

    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    advMng = dbus.Interface(sysBus.get_object(SERVICE_NAME, adapter_advMng), LE_ADVERTISING_MANAGER_IFACE)

    return advMng
