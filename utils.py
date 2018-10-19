#!/usr/bin/env python
"""Provides generic checking/utility functions concerning mqtt-to-gatt operations.
"""

import pandas as pd
import os

__author__ = "Kasidit Yusuf"
__copyright__ = "bluez-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf."
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"


def check_int_list(int_list):
    if not isinstance(int_list, list):
        raise Exception("not a python list")
    if len(int_list) == 0:
        raise Exception("list must have at least one entry")
    for val in int_list:
        if not isinstance(val, int):
            raise Exception("entry in list not a number: "+str(val))
    return


def read_csv_in_module_path_as_df(csv_fn, sep='\t'):
    module_path = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )    
    csv_path = os.path.join(module_path, csv_fn)
    df = pd.read_csv(csv_path, sep=sep)
    return df
