from MQTTSNclient import Client
import struct
import time
import sys

class Callback:

    def messageArrived(self, topicName, payload, qos, retained, msgid):
        print('Got msg %s from %s' % (payload, topicName))
        return True

def connect_gateway():
    try:
        while True:
            try:
                aclient.connect()
                print('Connected to gateway...')
                break
            except:
                print('Failed to connect to gateway, reconnecting...')
                time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit()

def subscribe_topic():
    aclient.subscribe("topic3", qos=2)
    print("Subscribed to topic3.")
    aclient.subscribe("topic2", qos=1)
    print("Subscribed to topic2.")
    aclient.subscribe("topic1", qos=0)
    print("Subscribed to topic1.")

aclient = Client("client_sn_sub", "192.168.1.9", port=1885)
aclient.registerCallback(Callback())
connect_gateway()

subscribe_topic()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    aclient.unsubscribe('topic1')
    print("Unsubscribe from topic1.")
    aclient.unsubscribe('topic2')
    print("Unsubscribe from topic2.")
    aclient.unsubscribe('topic3')
    print("Unsubscribe from topic3.")
    aclient.disconnect()
    print("Disconnected from gateway.")
