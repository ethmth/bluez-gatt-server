#!/usr/bin/env python
"""Provides a Pandas DataFrame holding the spec-defined Bluetooth GATT Characteristic info (including UUIDs).

Data from https://www.bluetooth.com/specifications/gatt/characteristics - saved to spec_gatt_characteristics.csv"""

import mqtt_to_gatt_utils

__author__ = "Kasidit Yusuf"
__copyright__ = "mqtt-to-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf."
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"

g_spec_gatt_chrc_df = None


def get_spec_gatt_chrc_df():
    global g_spec_gatt_chrc_df

    if g_spec_gatt_chrc_df is None:
        print "reading g_spec_gatt_chrc_df..."
        g_spec_gatt_chrc_df = mqtt_to_gatt_utils.read_csv_in_module_path_as_df("spec_gatt_characteristics.csv")
        print "g_spec_gatt_chrc_df cols:", g_spec_gatt_chrc_df.columns
        # convert "Assigned Number" from 'hex string' to int
        g_spec_gatt_chrc_df["Assigned Number"] = g_spec_gatt_chrc_df["Assigned Number"].apply(lambda x: int(x,16))
    
    return g_spec_gatt_chrc_df


def get_gatt_chrc_name_for_uuid(uuid):
    ret = None
    df = get_spec_gatt_chrc_df()
    df = df[df["Assigned Number"] == uuid]
    if len(df) == 1:
        return df.iloc[0]["Name"]
    return None

    


    
