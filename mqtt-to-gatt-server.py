#!/usr/bin/env python
"""Main mqtt-to-gatt-server program that provides functionality as described in the 'README.md' file.
"""

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import argparse
import ble_service_uuids
import ble_characteristic_uuids
import service_template
import mqtt_to_gatt_utils

__author__ = "Kasidit Yusuf"
__copyright__ = "mqtt-to-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf."
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"


def main():

    
    ### define options/args

    parser = argparse.ArgumentParser(
        description="mqtt-to-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf.\nReleased under the GNU GPL v2 License - see COPYING file (from BlueZ project) for details. This project is a fork of 'python-gatt-server' (https://github.com/Jumperr-labs/python-gatt-server.git) originally by Jumper Labs which is based on 'BlueZ' (http://www.bluez.org/) example code. Credit goes to respective authors and see copyright notices of respective projects for further details.",
        usage="Use mqtt_gatt_server to define and start a Bluetooth Low Energy (BLE) service where its characteristics' values would be updated from the specified 'MQTT server and topic'. Only characteristic Read and Notify operations are supported.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-a', '--adapter-name', type=str, help='Adapter name', default='')

    parser.add_argument('--mqtt_host', type=str, help='MQTT Host URL', default='localhost')

    parser.add_argument('--service_uuid', type=str, help='BLE service UUID in hex starting with 0x - e.g., "Battery Service" would be: 0x180F', required=True)

    parser.add_argument('--characteristic_uuid_list', type=str, help='Python-sytaxed list of Bluetooth service UUID in hex starting with 0x - e.g., A list containing one characteristic of "Battery Level" would be: [0x2A19]', required=True)
    

    ### parse/check arguments

    print "Checking arguments..."
    args = parser.parse_args()
    args_dict = vars(args)

    service_uuid = eval(args_dict['service_uuid'])
    if not isinstance(service_uuid, int):
        print "Invalid service_uuid specified - not a number"
        exit(1)
        
    characteristic_uuid_list = None
    try:
        characteristic_uuid_list = eval(args_dict['characteristic_uuid_list'])
        mqtt_to_gatt_utils.check_int_list(characteristic_uuid_list)
    except Exception as e:
        print "Invalid --characteristic_uuid_list specified - exception:", e
        exit(2)

    try:
        characteristic_uuid_list = eval(args_dict['characteristic_uuid_list'])
        mqtt_to_gatt_utils.check_int_list(characteristic_uuid_list)
    except Exception as e:
        print "Invalid --characteristic_uuid_list specified - exception:", e
        exit(2)        
    
    
    ### prepare dbus stuff

    print "Preparing dbus..."
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    
    ### create BLE service

    print "Creating BLE service..."
    print "- service uuid: 0x%x" % service_uuid
    print "- characteristic_uuid_list: "

    characteristic_default_value_list = []
    for chrc_uuid in characteristic_uuid_list:
        print "  - 0x%x" % chrc_uuid
        chrc_name_for_uuid = spec_gatt_chrc_list
        print ""
        characteristic_default_value_list.append(0)

    service = service_template.create_read_notify_service(
        bus,
        0,
        service_uuid,
        True,
        characteristic_uuid_list,
        characteristic_default_value_list
    )

    ### start BLE service
   
    service_template.start_services(mainloop, bus, args_dict['adapter_name'], [service])
    mainloop.run()

    # TODO: run another thread that reads from the mqtt server and updates the chrc on changes

    

if __name__ == '__main__':
    main()
