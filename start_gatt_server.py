import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
import array
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import argparse

import server_template
import ad_template
import gatt_server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--adapter-name', type=str, help='Adapter name', default='')
    args = parser.parse_args()
    adapter_name = args.adapter_name

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    service_uuid_list = ['180F']  # battery service - https://www.bluetooth.com/specifications/gatt/services
    ad_template.start_ad(mainloop, bus, adapter_name, service_uuid_list)
    #gatt_server.gatt_server_main(mainloop, bus, adapter_name)
    server_template.start_server(mainloop, bus, adapter_name)
    mainloop.run()

    

if __name__ == '__main__':
    main()
