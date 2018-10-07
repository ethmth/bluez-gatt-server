import spec_gatt_chrc_list


def test():

    chrc_df = spec_gatt_chrc_list.get_spec_gatt_chrc_df()
    print "spec chrc_df len:", len(chrc_df)
    assert len(chrc_df) >= 226

    chrc_name = spec_gatt_chrc_list.get_gatt_chrc_name_for_uuid(0x2A19)
    print "0x2a19 match chrc_name:", chrc_name
    assert chrc_name == 'Battery Level'

if __name__ == '__main__':
    test()
