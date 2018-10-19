#!/usr/bin/env python
"""Provides 'Assigned Number' to 'Name' matching funcs, Pandas DataFrames holding the spec-defined Bluetooth GATT Characteristic, Services 'Assigned Numbers' as related info.
"""

import utils

__author__ = "Kasidit Yusuf"
__copyright__ = "bluez-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf."
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"

g_df_cache = {}

# Data from https://www.bluetooth.com/specifications/gatt/services
BT_GATT_SERVICE_ASSIGNED_NUMBERS_CSV = "bt_gatt_service_assigned_numbers.csv"

# Data from https://www.bluetooth.com/specifications/gatt/characteristics
BT_GATT_CHRC_ASSIGNED_NUMBERS_CSV = "bt_gatt_chrc_assigned_numbers.csv"


def get_assigned_numbers_df(csv_fn):
    global g_df_cache

    #print "get_assigned_numbers_df: csv_fn:", csv_fn
    if csv_fn not in g_df_cache:
        print "reading assigned_numbers_csv:", csv_fn
        df = utils.read_csv_in_module_path_as_df(csv_fn)        
        # convert "Assigned Number" from 'hex string' to int
        df["Assigned Number"] = df["Assigned Number"].apply(lambda x: int(x,16))
        g_df_cache[csv_fn] = df
    
    return g_df_cache[csv_fn]


def get_assigned_number_name(csv, assigned_number):
    #print "get_assigned_number_name csv:", csv
    df = get_assigned_numbers_df(csv)
    df = df[df["Assigned Number"] == assigned_number]
    if len(df) == 1:
        return df.iloc[0]["Name"]
    return None


def get_gatt_chrc_name_for_assigned_number(assigned_number):
    return get_assigned_number_name(BT_GATT_CHRC_ASSIGNED_NUMBERS_CSV, assigned_number)

    
def get_gatt_service_name_for_assigned_number(assigned_number):
    return get_assigned_number_name(BT_GATT_SERVICE_ASSIGNED_NUMBERS_CSV, assigned_number)


def check_service_assigned_number(service_assigned_number):
    if not isinstance(service_assigned_number, int):
        raise Exception("Invalid service_assigned_number specified - not a number")

    service_name = get_gatt_service_name_for_assigned_number(service_assigned_number)
    print "Check service_assigned_number 0x%x - got matching Name: %s" % (service_assigned_number, service_name)
    if service_name is None:
        raise Exception("Failed to find matching GATT Service for Assigned Number: 0x%x - please use a valid Assigned Number from: https://www.bluetooth.com/specifications/gatt/services" % service_assigned_number)


def check_chrc_assigned_number_list(characteristic_assigned_number_list):
    utils.check_int_list(characteristic_assigned_number_list)
    for chrc in characteristic_assigned_number_list:
        chrc_name = get_gatt_chrc_name_for_assigned_number(chrc)        
        print "Check chrc assigned_number: 0x%x - got matching Name: %s"  % (chrc, chrc_name)
        if chrc_name is None:
            raise Exception("Failed to find matching Characteristic Name for Assigned Number: 0x%x - please use a valid Assigned Number from: https://www.bluetooth.com/specifications/gatt/characteristics" % chrc)

