import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
import functools
import gatt_server
import adapters


class AppTemplate(gatt_server.Application):
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

    
def register_app_cb():
    print('GATT application registered')


def register_app_error_cb(mainloop, error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()


def start_server(mainloop, bus, adapter_name):
    adapter = adapters.find_adapter(bus, gatt_server.GATT_MANAGER_IFACE, adapter_name)
    if not adapter:
        raise Exception('GattManager1 interface not found')

    service_manager = dbus.Interface(
            bus.get_object(gatt_server.BLUEZ_SERVICE_NAME, adapter),
            gatt_server.GATT_MANAGER_IFACE)

    service_list = [gatt_server.BatteryService(bus, 1)]
    app = AppTemplate(bus, service_list)

    print('Registering GATT application...')

    service_manager.RegisterApplication(app.get_path(), {},
                                    reply_handler=register_app_cb,
                                    error_handler=functools.partial(register_app_error_cb, mainloop))
