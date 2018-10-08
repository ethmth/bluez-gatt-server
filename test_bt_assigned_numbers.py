import bt_assigned_numbers


def test():

    chrc_df = bt_assigned_numbers.get_assigned_numbers_df(bt_assigned_numbers.BT_GATT_CHRC_ASSIGNED_NUMBERS_CSV)
    print "bt spec chrc_df len:", len(chrc_df)
    assert len(chrc_df) >= 226

    service_name = bt_assigned_numbers.get_gatt_service_name_for_assigned_number(0x180f)
    print "0x180f match service_name:", service_name
    assert service_name == 'Battery Service'


    chrc_name = bt_assigned_numbers.get_gatt_chrc_name_for_assigned_number(0x2A19)
    print "0x2a19 match chrc_name:", chrc_name
    assert chrc_name == 'Battery Level'


if __name__ == '__main__':
    test()
