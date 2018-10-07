#!/usr/bin/env python
"""Provides simple ways to define and start BLE services.

- use create_read_notify_service() to define a BLE Service and Read+Notify Characteristics in one call.
- use start_services() to start the created servives
"""

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
import functools
import gatt_server
import adapters
from gatt_server import Application
from gatt_server import Service
from gatt_server import Characteristic
import sys
import traceback
import ble_service_uuid_list
import ble_characteristic_uuid_list
import mqtt_to_gatt_utils

__author__ = "Kasidit Yusuf"
__copyright__ = "mqtt-to-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf."
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"


class AppTemplate(Application):
    """
    org.bluez.GattApplication1 interface implementation
    """
    def __init__(self, bus, service_list):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)

        if not isinstance(service_list, list):
            raise Exception("service_list must be a list - ABORT")
        if len(service_list) == 0:
            raise Exception("service_list must not be an empty list - ABORT")

        for service in service_list:
            print "adding service:", service
            self.add_service(service)

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(gatt_server.DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()

        return response


class ReadNotifyCharacteristic(Characteristic):

    ######### Below functions would be used by the app developer (us)
    
    def __init__(self, bus, index, service, chrc_uuid, initial_value):

        Characteristic.__init__(
            self, bus, index,
            chrc_uuid,            
            ['read', 'notify'],
            service)
        self.notifying = False
        self.value = initial_value

        
    def update_value(self, value):
        self.value = value
        if not self.notifying:
            return
        self.PropertiesChanged(
                gatt_server.GATT_CHRC_IFACE,
                {'Value': [dbus.Byte(self.value)] }, [])


    ########### Below funcs would be used/called by the framework
    
    def ReadValue(self, options):
        try:
            if self.value is None:
                print "WARNING: ReadValue called when self.value is None"
            return [dbus.Byte(self.value)]
        except:
            type_, value_, traceback_ = sys.exc_info()
            exstr = str(traceback.format_exception(type_, value_, traceback_))        
            print "WARNING: ReadValue - exception:", exstr
        return None

    
    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True

        
    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False

        
    
def register_app_cb():
    print('GATT application registered')


def register_app_error_cb(mainloop, error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()


def create_read_notify_service(bus, index, service_uuid, is_primary, chrc_uuid_list, chrc_default_val_list):

    mqtt_to_gatt_utils.check_int_list(chrc_uuid_list)
    mqtt_to_gatt_utils.check_int_list(chrc_default_val_list)

    if len(chrc_uuid_list) != len(chrc_default_val_list):
        raise Exception("The specified chrc_uuid_list doesnt have the same length as the specified chrc_default_val_list.")
        
    service = Service(bus, index, service_uuid, is_primary)

    chrc_index = 0
    for i in range(len(chrc_uuid_list)):
        chrc_uuid = chrc_uuid_list[i]
        default_val = chrc_default_val_list[i]
        chrc = ReadNotifyCharacteristic(bus, chrc_index, service, chrc_uuid, default_val)
        service.add_characteristic(chrc)
        chrc_index += 1
        
    return service


def start_services(mainloop, bus, adapter_name, service_list):
    adapter = adapters.find_adapter(bus, gatt_server.GATT_MANAGER_IFACE, adapter_name)
    if not adapter:
        raise Exception('GattManager1 interface not found')

    service_manager = dbus.Interface(
            bus.get_object(gatt_server.BLUEZ_SERVICE_NAME, adapter),
            gatt_server.GATT_MANAGER_IFACE)
    
    app = AppTemplate(bus, service_list)

    print('Registering GATT application...')

    service_manager.RegisterApplication(app.get_path(), {},
                                    reply_handler=register_app_cb,
                                    error_handler=functools.partial(register_app_error_cb, mainloop))
