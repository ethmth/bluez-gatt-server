import os

def test():

    import pandas
    import paho.mqtt.client

    assert os.system("which mosquitto_pub") == 0
    

if __name__ == '__main__':
    test()
