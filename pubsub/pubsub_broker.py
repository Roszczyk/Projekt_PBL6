from pubsub_db import payload_format, add_to_database
import paho.mqtt.client as mqtt
from functools import partial
import time

def on_message_db(client, userdata, message, db_addr, db_base, db_collection):
    print(f"received message: \n{message.payload}")
    formated_message = payload_format(message.payload)
    print(f"formated message: \n{formated_message}")
    add_to_database(formated_message, db_addr, db_base, db_collection)

def on_message(client, userdata, message):
    print(f"received message: {message.payload}")

def broker_publish(message, topic, broker_ip, broker_port, username, password):
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker_ip, broker_port)
    time.sleep(2)
    message = 'catch me'
    client.publish(topic, message)
    client.disconnect()

def broker_subscribe(topic, broker_ip, broker_port, username, password):
    client = mqtt.Client()
    client.on_message = on_message
    client.username_pw_set(username, password)
    client.connect(broker_ip, broker_port)
    client.subscribe(topic)
    client.loop_forever()

def broker_to_basabase(topic, broker_ip, broker_port, username, password, db_addr, db_base, db_collection):
    client = mqtt.Client()
    client.on_message = partial(on_message_db, db_addr=db_addr, db_base=db_base, db_collection=db_collection)
    client.username_pw_set(username, password)
    client.connect(broker_ip, broker_port)
    client.subscribe(topic)
    client.loop_forever()   