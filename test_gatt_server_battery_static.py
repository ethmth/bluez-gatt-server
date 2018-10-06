import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import argparse
import server_template


def test():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--adapter-name', type=str, help='Adapter name', default='')
    args = parser.parse_args()
    adapter_name = args.adapter_name

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    #### define our services
    my_batt_service = Service(bus, 0, ble_service_uuid_list.Battery_Service, True)
    my_batt_chrc = ReadNotifyCharacteristic(bus, 0, my_batt_service, ble_characteristic_uuid_list.Battery_Level, 19)
    my_batt_service.add_characteristic(my_batt_chrc)
    ####
    
    server_template.start_server(mainloop, bus, adapter_name, [my_batt_service])
    mainloop.run()

    

if __name__ == '__main__':
    test()
