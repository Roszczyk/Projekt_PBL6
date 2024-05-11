from pubsub_db import payload_format, add_to_database, download_from_database
import paho.mqtt.client as mqtt
from functools import partial
import time

def on_message_db(client, userdata, message, db_addr, db_base, db_collection):
    print(f"received message: {message}")
    formated_message = payload_format(message)
    add_to_database(formated_message, db_addr, db_base, db_collection)

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))

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


payload_str = """{"f_port": 1, "frm_payload": "AGcBEwBoRgCIBcOAGcBDQBoRQ==", 
"decoded_payload": {"temperature_0": 34.91, "presence_0":"0xFF", "relative_humidity_0": 24.95, "digital_in_1": true, 
"digital_in_2": true}, "rx_metadata": [{"gateway_ids": {"gateway_id": "test"}, "rssi": 42, "channel_rssi": 42, "snr": 4.2}], 
"settings": {"data_rate": {"lora": {"bandwidth": 125000, "spreading_factor": 7}}, "frequency": "868000000"}, 
"dev_EUI": "70B3D57ED0063437", "received_at": "2024-05-10T10:56:38.669"}"""

database_addr = "10.141.10.69:27017"
broker_addr = {"ip":"10.141.10.69", "port":1883}

broker_to_basabase("PAM-PBL5-CATCHER", broker_addr["ip"], broker_addr["port"], "rw", "readwrite", database_addr, "test", "test")