import gatt_characteristics


def test():
    chrc_df = gatt_characteristics.get_spec_gatt_chrc_df()
    print "spec chrc_df len:", len(chrc_df)
    assert len(chrc_df) >= 226


if __name__ == '__main__':
    test()
