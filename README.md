bluez-gatt-server
===================

About
-----

Create a Bluetooth Low Energy GATT Service on BlueZ from a single terminal/bash command. Update its values from a single 'mosquitto_pub' (MQTT publish) command. It just works - no extra programming required.

Easy to use
-----------

Host a BLE GATT Service with Read/Notify Characteristics from a one line bash/terminal command:
<pre>
python bluez-gatt-server.py --service_assigned_number "Battery Service" --characteristic_assigned_number_list "[('Battery Level', 'mqtt://localhost:1883/my_battery_level')]"
</pre>

Update (initialize) the characteristics using a hex string from another (MQTT) mosquitto_pub command - let's try update the battery percent to 17% - this is a one-byte hex string of '11':
<pre>
mosquitto_pub -t "my_battery_level" -m "11"
</pre>

(You can use 'bc' to calculate the 1-byte hex value of 17% too like: <pre>"obase=16; 17" | bc</pre> instead of calculating '11'.)

Now, use 'nRF Connect' BLE app (or similar) to read this 'battery level' characteristic from phone! Yes, it would show 17%.
Then, press the 'subscribe notifications' button, and update the value to 16 on computer:
<pre>mosquitto_pub -t "my_battery_level" -m "10"</pre>

You'd see the value update to 16% in the phone app instantly!

Done - in a similar manner - you can now easily script to create and update your BLE service!

Obviously, as the commands above hints, you can also specify remote MQTT servers/topics which might stream from remote sensors/notifications and you might also use various MQTT APIs to update the MQTT topic as alternatives to the 'mosquitto_pub' command too.

Easy to script, easy to use - [just like in the good old days where commands like 'hciconfig', 'sdptool' and 'rfcomm' roamed the earth](https://github.com/ykasidit/bluez-compassion). They don't make them like that any more:

![They don't make them like that any more.](http://www.clearevo.com/300D/300D_small.jpg "They don't make them like that any more.")

This project is a fork of 'python-gatt-server' (https://github.com/Jumperr-labs/python-gatt-server.git) originally by Jumper Labs which in turn is based on 'BlueZ' (http://www.bluez.org/) example code. Credit goes to respective authors and see copyright notices of respective projects for further details.

Special thanks to the BlueZ project for providing Bluetooth support to GNU/Linux as well as their easy to program D-Bus APIs - especially from Python - much simpler than the C API in the old days.

Setup
-----

- Download, compile, install BlueZ 5.50 (./configure, make, sudo make install, sudo service bluetooth restart). Right now, we are currently using Bluez 5.50 with good success so far and no need to enable 'experimental' features. Make sure it is working (try bluetoothctl commands).
- Make sure python 'pandas' is installed. (sudo pip install pandas)
- Make sure python 'paho-mqtt' library is installed. (sudo pip install paho-mqtt)
- Make sure you've install a MQTT server (sudo apt-get install mosquitto), and a MQTT client to test (sudo apt-get install mosquitto-clients). *If you never tried this, please go through the examples at https://www.vultr.com/docs/how-to-install-mosquitto-mqtt-broker-server-on-ubuntu-16-04 - only until the 'Publish a message to topic "test"' topic is fine. (We'll use this to test updating our BLE Characteristics).*
- Make sure python 'pytest' testing library is installed. (sudo pip install pytest)
- Run 'pytest' command in this directory - make sure all tests have passed.
- For actual testing the BLE Services - we use, recommend and really want to thank Nordic semi for providing their great free Android app named 'nRF Connect'.


Updating the Bluetooth GATT Service/Characteristics Assigned Numbers
--------------------------------------------------------------------

Using a browser, you can copy the 'table' list from https://www.bluetooth.com/specifications/gatt/services and https://www.bluetooth.com/specifications/gatt/characteristics and paste into the files bt_gatt_service_assigned_numbers.csv and bt_gatt_chrc_assigned_numbers.csv respectively. Make sure you run 'pytest' again to test that the csv files are in the correct format.

Use cases
----------

- Easily host and update local BLE GATT Services from bash scripts or other software.

- Stream data frome remote notificaions to local BLE GATT Services. For example, if some low-power BLE devices that don't have internet access need to know some data/flag/command from a remote server - they can read that data/flag/command from a BLE Service/Characteristic on this GNU/Linux computer/board instead.

- Mirror/Duplicate remote BLE devices which were already setup to publish to a MQTT server - stream their BLE GATT Service/Characteristic reads/notifications to update the same on this GNU/Linux computer/board running this project. Therefore, mobile apps connect/read/display data from the remote BLE device through this computer/board.

LICENSE
-------

bluez-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf.

Released under the GNU GPL v2 License - see COPYING file (from BlueZ project) for details. This project is a fork of 'python-gatt-server' (https://github.com/Jumperr-labs/python-gatt-server.git) originally by Jumper Labs which is based on 'BlueZ' (http://www.bluez.org/) example code. Credit goes to respective authors and see copyright notices of respective projects for further details.

