import paho.mqtt.client as mqtt
import json

BROKER_IP = '10.141.10.72'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, message):
    print("Received message '")

    parsed = json.loads(message.payload.decode('utf-8'))
    print(json.dumps(parsed, indent=4))

    print("' on topic '" + message.topic + "' with QoS " + str(message.qos))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic with MID " +
          str(mid) + " and QoS " + str(granted_qos))


def on_publish(client, userdata, mid):
    print("Message published")


if __name__ == '__main__':
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_publish = on_publish

    # Connect to the MQTT broker
    client.username_pw_set("piotr", "piotr")

    # Connect to the MQTT broker
    # Replace with your MQTT broker address and port
    client.connect(BROKER_IP, 31111)

    # Subscribe to the topic
    client.subscribe("#")
    client.loop_forever()
