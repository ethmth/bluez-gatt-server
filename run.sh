#!/bin/bash

# VERSION=$1
VERSION="3"

python$VERSION bluez-gatt-server.py --service_assigned_number "Scooter Service" --characteristics_table_csv "my_chrc.csv"
