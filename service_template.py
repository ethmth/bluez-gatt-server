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
import sys
import traceback
import urlparse
import threading

import paho.mqtt.client as mqtt
import gatt_server
import adapters
from gatt_server import Application
from gatt_server import Service
from gatt_server import Characteristic
import bt_assigned_numbers

__author__ = "Kasidit Yusuf"
__copyright__ = "bluez-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf."
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
    
    def __init__(self, bus, index, service, chrc_assigned_number, initial_value):

        Characteristic.__init__(
            self, bus, index,
            chrc_assigned_number,            
            ['read', 'notify'],
            service)
        self.notifying = False

        if initial_value is not None:
            self.value_buffer = buffer_to_dbus_byte_list(hex_str_decode_to_buffer(initial_value))
        else:
            self.value_buffer = None

    # value: hex string that can be .decode('hex') via python - example: "10" (for a one-byte value of 16)
        
    def update_value(self, new_value):

        print "update_value:", new_value
        try:            
            self.value_buffer = buffer_to_dbus_byte_list(hex_str_decode_to_buffer(new_value))
            print "update_value calling PropertiesChanged - new self.value_buffer hex dump:", self.value_buffer
            
            if not self.notifying:
                print "update_value but not notifying so ignore this call"
                return
            
            self.PropertiesChanged(
                gatt_server.GATT_CHRC_IFACE,
                {
                    'Value': self.value_buffer
                },
                []
            )

        except:
            type_, value_, traceback_ = sys.exc_info()
            exstr = str(traceback.format_exception(type_, value_, traceback_))        
            print "WARNING: update_value - exception:", exstr

    
    def ReadValue(self, options):
        print "ReadValue: enter"
        if self.value_buffer is None:
            print "WARNING: ReadValue called when self.value_buffer is None"
            return None

        return self.value_buffer

    
    def StartNotify(self):
        print "StartNotify: enter"
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True

        
    def StopNotify(self):
        print "StopNotify: enter"
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False


class MqttSrcReadNotifyCharacteristic(ReadNotifyCharacteristic):

    def __init__(self, bus, index, service, chrc_assigned_number, initial_value, mqtt_topic_url):

        self.mqtt_connected = False
        
        ReadNotifyCharacteristic.__init__(
            self, bus, index,
            service,
            chrc_assigned_number,            
            initial_value
        )

        if mqtt_topic_url is None:
            print "WARNING: MqttSrcReadNotifyCharacteristic: mqtt_topic_url is None for chrc_assigned_number 0x%x - omit value updates from mqtt" % (chrc_assigned_number)
        else:
            url = urlparse.urlparse(mqtt_topic_url)

            topic = url.path[1:]
            if not topic:
                raise Exception("invalid mqtt_server_url - no topic (path) specified: {}".format(mqtt_topic_url))

            mqttc = mqtt.Client()
            self.mqttc = mqttc
            # Assign event callbacks
            mqttc.on_message = self.on_message
            mqttc.on_connect = self.on_connect
            mqttc.on_publish = self.on_publish
            mqttc.on_subscribe = self.on_subscribe
            mqttc.on_log = self.on_log

            mqttc.username_pw_set(url.username, url.password)
            
            print "order mqtt_client connect to:", url            
            mqttc.connect(url.hostname, url.port)
            mqttc.subscribe(topic, 0)

            mqtt_thread = threading.Thread(target=self.mqtt_loop, args=())
            mqtt_thread.daemon = True
            mqtt_thread.start()

        
    def mqtt_loop(self):
        if self.mqttc is None:
            return
        # Continue the network loop, exit when an error occurs
        rc = 0
        while rc == 0:
            rc = self.mqttc.loop()
            print("rc: " + str(rc))
            
    # Define mqtt event callbacks
    def on_connect(self, client, userdata, flags, rc):
        self.mqtt_connected = True
        print("on_connect: " + str(rc))

    def on_message(self, client, obj, msg):
        print("on_message: topic: {} qos: {} payload_to_update_chrc_value: {}".format(msg.topic, msg.qos, msg.payload))
        self.update_value(msg.payload)

    def on_publish(self, client, obj, mid):
        print("on_publish: " + str(mid))

    def on_subscribe(self, client, obj, mid, granted_qos):
        print("on_subscribe: " + str(mid) + " " + str(granted_qos))

    def on_log(self, client, obj, level, string):
        print("on_log:", string)
        
    
def register_app_cb():
    print('GATT application registered')


def register_app_error_cb(mainloop, error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()

    
def hex_str_decode_to_buffer(value):
    if not isinstance(value, str):
        raise Exception("hex_str_decode_to_buffer: invalid value is not 'str' - value type:", type(value))
    
    value = value.strip()
    value = value.replace(' ','')
    value = value.replace('0x','')

    retstr = value.decode('hex')
    return retstr

    
def buffer_to_dbus_byte_list(bufferstr):
    # generate dbus_byte_list
    dbus_byte_list = []
    for char in bufferstr:
        dbus_byte_list.append(dbus.Byte(char))

    return dbus_byte_list
        
    


def create_read_notify_service(bus, index, service_assigned_number, is_primary, chrc_to_mqtt_topic_tuple_list):

    if isinstance(service_assigned_number, str):
        print "provided service_assigned_number is a string - trying to match known services for the assigned_number..."
        service_assigned_number = bt_assigned_numbers.get_gatt_service_assigned_number_for_name(service_assigned_number)
        print "provided service_assigned_number is a string - got match: 0x%x" % service_assigned_number

    # check chrc_to_mqtt_topic_tuple_list - each must be either be an int for static chrc or tuple(int, str) for mqtt_topic triggered chrc
    chrc_assigned_number_list = []
    mqtt_topic_url_list = []
    for entry in chrc_to_mqtt_topic_tuple_list:
        if isinstance(entry, tuple):
            if len(entry) != 2:
                raise Exception("invalid chrc to mqtt_topic_url tuple len: "+str(entry))
            else:
                
                if isinstance(entry[0], str):
                    print "provided chrc_assigned_number: '%s' is a string - trying to match known chrc for the assigned_number..." % entry[0]
                    chrc_assigned_number = bt_assigned_numbers.get_gatt_chrc_assigned_number_for_name(entry[0])
                    print "provided chrc_assigned_number is a string - got match: 0x%x" % chrc_assigned_number
                    entry = (chrc_assigned_number, entry[1])  # create updated entry
                    
                if isinstance(entry[0], int) and isinstance(entry[1], str):
                    chrc_assigned_number_list.append(entry[0])
                    mqtt_topic_url_list.append(entry[1])
                else:
                    raise Exception("invalid chrc to mqtt_topic_url tuple - first must be int, second must be str: "+str(entry))
        else:
            raise Exception("invalid chrc to mqtt_topic_url entry: {} - must be tuple but got type: {}".format(entry, type(entry)))

    try:
        bt_assigned_numbers.check_service_assigned_number(service_assigned_number)
    except:
        type_, value_, traceback_ = sys.exc_info()
        exstr = str(traceback.format_exception(type_, value_, traceback_))        
        print "WARNING: failed to match a known service from specified 'assigned number' - exception:", exstr


    try:
        bt_assigned_numbers.check_chrc_assigned_number_list(chrc_assigned_number_list)
    except:
        type_, value_, traceback_ = sys.exc_info()
        exstr = str(traceback.format_exception(type_, value_, traceback_))        
        print "WARNING: failed to match a known characteristic from specified 'assigned number' - exception:", exstr
        

    service = Service(bus, index, service_assigned_number, is_primary)

    chrc_index = 0
    for i in range(len(chrc_assigned_number_list)):

        chrc_assigned_number = chrc_assigned_number_list[i]
        mqtt_topic_url = mqtt_topic_url_list[i]
                
        chrc = MqttSrcReadNotifyCharacteristic(bus, chrc_index, service, chrc_assigned_number, "00", mqtt_topic_url)
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


