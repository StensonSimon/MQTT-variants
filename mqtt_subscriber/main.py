from umqtt import MQTTClient
from machine import Pin
import machine
import ubinascii

# Modify below section as required
CONFIG = {
     # Configuration details of the MQTT broker
     "MQTT_BROKER": "192.168.1.9",
     "PORT": 1883,
     "TOPIC": "mqtt",
     # unique identifier of the chip
     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}



# Method to act based on message received
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))


def listen():
    #Create an instance of MQTTClient
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'],port=CONFIG['PORT'])
    # Attach call back handler to be called on receiving messages
    client.set_callback(onMessage)
    client.connect()
    client.publish("mqtt", "ESP8266 is Connected")
    client.subscribe(CONFIG['TOPIC'])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))

    try:
        while True:
            msg = client.wait_msg()
            msg = (client.check_msg())
    finally:
        client.disconnect()

listen()
