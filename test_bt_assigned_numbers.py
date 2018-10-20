import bt_assigned_numbers


def test():

    chrc_df = bt_assigned_numbers.get_assigned_numbers_df(bt_assigned_numbers.BT_GATT_CHRC_ASSIGNED_NUMBERS_CSV)
    print "bt spec chrc_df len:", len(chrc_df)
    assert len(chrc_df) >= 226

    service_name = bt_assigned_numbers.get_gatt_service_name_for_assigned_number(0x180f)
    print "0x180f match service_name:", service_name
    assert service_name == 'Battery Service'

    san = bt_assigned_numbers.get_gatt_service_assigned_number_for_name('Battery Service')
    print "'Battery Service' match assigned_number:", san
    assert san == 0x180f

    chrc_name = bt_assigned_numbers.get_gatt_chrc_name_for_assigned_number(0x2A19)
    print "0x2a19 match chrc_name:", chrc_name
    assert chrc_name == 'Battery Level'

    can = bt_assigned_numbers.get_gatt_chrc_assigned_number_for_name('Battery Level')
    print "Battery Level match chrc_assigned_number:", can
    assert can == 0x2a19


if __name__ == '__main__':
    test()
