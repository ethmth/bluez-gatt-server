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


def test():

    ################ define options/args
    parser = argparse.ArgumentParser(
        description="mqtt_gatt_server",
        usage="Use mqtt_gatt_server to define and start a Bluetooth Low Energy (BLE) service where its characteristics' values would be updated from the specified 'MQTT server and topic'. Only characteristic Read and Notify operations are supported.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-a', '--adapter-name', type=str, help='Adapter name', default='')

    parser.add_argument('--mqtt_host', type=str, help='MQTT Host URL', default='localhost')

    parser.add_argument('--service_uuid', type=str, help='BLE service UUID in hex starting with 0x - e.g., "Battery Service" would be: 0x180F', required=True)

    parser.add_argument('--characteristic_uuid_list', type=str, help='Python-sytaxed list of Bluetooth service UUID in hex starting with 0x - e.g., A list containing one characteristic of "Battery Level" would be: [0x2A19]', required=True)
    
    args = parser.parse_args()
    args_dict = vars(args)
        
    characteristic_uuid_list = None

    try:
        characteristic_uuid_list = eval(args_dict['characteristic_uuid_list'])
        if not isinstance(characteristic_uuid_list, list):
            raise Exception("not a python list")
        if len(characteristic_uuid_list) == 0:
            raise Exception("list must have at least on characteristic uuid")
        for chrc_uuid in characteristic_uuid_list:
            if not isinstance(chrc_uuid, int):
                raise Exception("characteristic uuid not a number: "+str(chrc_uuid))
    except Exception as e:
        print "Invalid --characteristic_uuid_list specified - error:", e
        exit(-1)    
    #################

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    #### define our battery service with 3 percent ramaining battery level characteristic
    service = service_template.create_read_notify_service(
        bus,
        0,
        ble_service_uuids.Battery_Service,
        True,
        [ble_characteristic_uuids.Battery_Level],
        [3]
    )
    ####

    # TODO: try run another thread that gets a ptr to the chrc and randomly changes its battery value - test with notify from phone...
    
    service_template.start_services(mainloop, bus, adapter_name, [test_batt_service])
    mainloop.run()

    

if __name__ == '__main__':
    test()
