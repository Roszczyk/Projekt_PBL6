import paho.mqtt.client as mqtt
import time
from functools import partial
import json
from collections import defaultdict
from payload import prepare_payload

def execute_command(message : str, dev):
    payload = json.loads(message)
    payload = defaultdict(lambda: None, payload)
    if payload["device_id"] == dev.device_id:
        if payload["lights"] != None:
            new_state = (payload["lights"] == "True")
            dev.change_light(new_state)
        if payload["heating"] != None:
            new_state = (payload["heating"] == "True")
            dev.change_heating(new_state)
    dev.print_all()


def on_message(client, userdata, message, dev):
    raw_command = f"""{message.payload.decode("utf-8")}""".replace("'", '"')
    print(raw_command)
    execute_command(raw_command, dev)
    

def broker_publish(message, topic, broker_ip, broker_port, username, password):
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker_ip, broker_port)
    time.sleep(2)
    client.publish(topic, message)
    client.disconnect()

def broker_subscribe_init(topic, broker_ip, broker_port, username, password, device):
    client = mqtt.Client()
    client.on_message = partial(on_message, dev=device)
    client.username_pw_set(username, password)
    client.connect(broker_ip, broker_port)
    client.subscribe(topic)
    print("MQTT client initialized")
    return client

def broker_subscribe_loop(client):
    client.loop_forever()


def publish_measurements(dev, broker_addr, mqtt_user, mqtt_password, mqtt_topic):
    message = prepare_payload(dev)
    broker_publish(message, mqtt_topic, broker_addr["ip"], broker_addr["port"], mqtt_user, mqtt_password)
    print("measurements published")

def publish_measurements_thread(dev, broker_addr, mqtt_user, mqtt_password, mqtt_topic):
    while True:
        publish_measurements(dev, broker_addr, mqtt_user, mqtt_password, mqtt_topic)
        time.sleep(40)