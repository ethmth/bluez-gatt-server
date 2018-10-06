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
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--adapter-name', type=str, help='Adapter name', default='')
    args = parser.parse_args()
    adapter_name = args.adapter_name

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    #### define our battery service with 3 percent ramaining battery level characteristic
    test_batt_service = service_template.create_read_notify_service(
        bus,
        0,
        ble_service_uuids.Battery_Service,
        True,
        {
            ble_characteristic_uuids.Battery_Level: 3
        }
    )
    ####

    # TODO: try run another thread that gets a ptr to the chrc and randomly changes its battery value - test with notify from phone...
    
    service_template.start_services(mainloop, bus, adapter_name, [test_batt_service])
    mainloop.run()

    

if __name__ == '__main__':
    test()
