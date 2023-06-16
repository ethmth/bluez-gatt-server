#!/bin/bash

VERSION=$1

python$VERSION bluez-gatt-server.py --service_assigned_number "Battery Service" --characteristics_table_csv "example_batt_chrc.csv"
