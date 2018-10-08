#!/usr/bin/env python
"""Provides simple ways to define and start BLE advertisements.

Note: This file is not used right now as BlueZ already seems to maintain the advertisements based on defined services already.
"""

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
import functools
import adapters
import advertising
from advertising import Advertisement

__author__ = "Kasidit Yusuf"
__copyright__ = "mqtt-to-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf."
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"


class AdTemplate(Advertisement):
    def __init__(self, bus, index,
                 service_assigned_number_list,
                 manuf_code=0xffff,
                 manuf_data=[0x00, 0x01, 0x02, 0x03, 0x04],
                 service_assigned_number='9999',
                 service_data=[0x00, 0x01, 0x02, 0x03, 0x04],
                 include_tx_power=True
    ):

        Advertisement.__init__(self, bus, index, 'peripheral')
        if not isinstance(service_assigned_number_list, list):
            raise Exception("service_assigned_number_list must be a list - ABORT")
        if len(service_assigned_number_list) == 0:
            raise Exception("service_assigned_number_list must not be an empty list - ABORT")
        
        for service_assigned_number in service_assigned_number_list:
            print "adding service_assigned_number:", service_assigned_number
            self.add_service_assigned_number(service_assigned_number)
        self.add_manufacturer_data(manuf_code, manuf_data)
        self.add_service_data(service_assigned_number, service_data)
        self.include_tx_power = include_tx_power


def register_ad_cb():
    print('Advertisement registered')


def register_ad_error_cb(mainloop, error):
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()


def start_ad(mainloop, bus, adapter_name, service_assigned_number_list):
    adapter = adapters.find_adapter(bus, advertising.LE_ADVERTISING_MANAGER_IFACE, adapter_name)
    print('adapter: %s' % (adapter,))
    if not adapter:
        raise Exception('LEAdvertisingManager1 interface not found')

    adapter_props = dbus.Interface(bus.get_object(advertising.BLUEZ_SERVICE_NAME, adapter),
                                   "org.freedesktop.DBus.Properties")

    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    ad_manager = dbus.Interface(bus.get_object(advertising.BLUEZ_SERVICE_NAME, adapter),
                                advertising.LE_ADVERTISING_MANAGER_IFACE)

    ad = AdTemplate(bus, 0, service_assigned_number_list)

    ad_manager.RegisterAdvertisement(ad.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=functools.partial(register_ad_error_cb, mainloop))

