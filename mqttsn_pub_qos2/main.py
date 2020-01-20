from MQTTSNclient import Client
import struct
import time
import sys

class Callback:

    def published(self, MsgId):
        print("Published")

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

def register_topic():
    global topic1
    topic1 = aclient.register("topic1")
    print("topic1 registered.")

aclient = Client("client_sn_pub", "192.168.1.9", port=1885)
aclient.registerCallback(Callback())
connect_gateway()

topic1 = None
register_topic()

payload1 = 'Hello World!'

while True:
    pub_msgid = aclient.publish(topic1, payload1, qos=2)
    time.sleep(2)

aclient.disconnect()
print("Disconnected from gateway.")
