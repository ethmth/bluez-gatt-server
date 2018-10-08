mqtt-to-gatt-server
===================

*Still under dev. NOT working yet.*


About
-----

Host Bluetooth GATT Services with Read/Notify Characteristics from a one line bash/terminal command. Update the characteristic from another command to a local MQTT (mosquitto) server 'topic', or even stream it from a remote MQTT server (that might even be from another BLE or non-BLE sensor/data-source).

This project is a fork of 'python-gatt-server' (https://github.com/Jumperr-labs/python-gatt-server.git) originally by Jumper Labs which in turn is based on 'BlueZ' (http://www.bluez.org/) example code. Credit goes to respective authors and see copyright notices of respective projects for further details.

*Python source Header format of most added files are from: http://web.archive.org/web/20111010053227/http://jaynes.colorado.edu/PythonGuidelines.html#module_formatting (linked from https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files).*

Setup
-----

- Download, compile, install BlueZ 5.50 (./configure, make, sudo make install, sudo service bluetooth restart). Right now, we are currently using Bluez 5.50 with good success so far and no need to enable 'experimental' features. Make sure it is working (try bluetoothctl commands).
- Make sure python 'pandas' is installed. (sudo pip install pandas)
- Make sure python 'paho-mqtt' library is installed. (sudo pip install paho-mqtt)
- Make sure you've install a MQTT server (sudo apt-get install mosquitto), and a MQTT client to test (sudo apt-get install mosquitto-clients). If you never tried this, please go through the great examples at https://www.vultr.com/docs/how-to-install-mosquitto-mqtt-broker-server-on-ubuntu-16-04 - only until the 'Publish a message to topic "test"' topic is fine. (We'll use this to test updating our BLE Characteristics).
- For actual testing the BLE Services - we use, recommend and really want to thank Nordic semi for providing their great free Android app named 'nRF Connect'.


Instructions
------------

- Let's try start a local BLE 'Battery Service' withen one 'Battery Level' characteristic. Firstly, let's try run the --help to see how to do this:
<pre>python mqtt-to-gatt-server.py --help</pre>
We'd get something like:
<pre>
...
optional arguments:
  -h, --help            show this help message and exit
  -a ADAPTER_NAME, --adapter-name ADAPTER_NAME
                        Adapter name
  --mqtt_host MQTT_HOST
                        MQTT Host URL
  --service_assigned_number SERVICE_ASSIGNED_NUMBER
                        BLE service ASSIGNED_NUMBER in hex starting with 0x - see
                        https://www.bluetooth.com/specifications/gatt/services for the full list - e.g., "Battery Service" would
                        be: 0x180F
  --characteristic_assigned_number_list CHARACTERISTIC_ASSIGNED_NUMBER_LIST
                        Python-sytaxed list of Bluetooth service ASSIGNED_NUMBER in hex starting with 0x - see
                        https://www.bluetooth.com/specifications/gatt/characteristics for the full list - e.g., A list containing
                        one characteristic of "Battery Level" would be: [0x2A19]
</pre>

- So we can consult the official bluetooth.com links in the help above to get the assigned numbers for our "Battery Service" service our "Battery Level" characteristic - below is our command:

<pre>
python mqtt-to-gatt-server.py --service_assigned_number 0x180F --characteristic_assigned_number_list [0x2A19]
</pre>

If all is well, it would show 'GATT application registered' as in below example output:

<pre>
Checking arguments...
reading assigned_numbers_csv: bt_gatt_service_assigned_numbers.csv
Check service_assigned_number 0x180f - got matching Name: Battery Service
reading assigned_numbers_csv: bt_gatt_chrc_assigned_numbers.csv
Check chrc assigned_number: 0x2a19 - got matching Name: Battery Level
Preparing dbus...
Creating BLE service...
- service assigned_number: 0x180f (Battery Service)
- characteristic_assigned_number_list: 
  - 0x2a19 (Battery Level)
checking adapter /org/bluez/hci0, keys: [dbus.String(u'org.bluez.GattManager1'), dbus.String(u'org.bluez.Media1'), dbus.String(u'org.freedesktop.DBus.Introspectable'), dbus.String(u'org.bluez.NetworkServer1'), dbus.String(u'org.bluez.LEAdvertisingManager1'), dbus.String(u'org.bluez.Adapter1'), dbus.String(u'org.freedesktop.DBus.Properties')]
found adapter /org/bluez/hci0
returning adapter /org/bluez/hci0
adding service: <gatt_server.Service at /org/bluez/example/service0 at 0x7f5130f7c7d0>
Registering GATT application...
GetManagedObjects
GATT application registered
</pre>


LICENSE
-------

mqtt-to-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf.

Released under the GNU GPL v2 License - see COPYING file (from BlueZ project) for details. This project is a fork of 'python-gatt-server' (https://github.com/Jumperr-labs/python-gatt-server.git) originally by Jumper Labs which is based on 'BlueZ' (http://www.bluez.org/) example code. Credit goes to respective authors and see copyright notices of respective projects for further details.

