#!/bin/bash

VERSION=$1

python$VERSION bluez-gatt-server.py --service_assigned_number "Automation IO" --characteristics_table_csv "my_chrc.csv"
