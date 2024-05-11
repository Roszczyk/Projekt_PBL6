from pubsub_db import *
import paho.mqtt.client as mqtt
import time

def broker_publish(message, topic, broker_ip, broker_port, username, password):
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker_ip, broker_port)
    time.sleep(2)
    message = 'catch me'
    client.publish(topic, message)
    client.disconnect()



payload_str = """{"f_port": 1, "frm_payload": "AGcBEwBoRgCIBcOAGcBDQBoRQ==", 
"decoded_payload": {"temperature_0": 34.91, "presence_0":"0xFF", "relative_humidity_0": 24.95, "digital_in_1": true, 
"digital_in_2": true}, "rx_metadata": [{"gateway_ids": {"gateway_id": "test"}, "rssi": 42, "channel_rssi": 42, "snr": 4.2}], 
"settings": {"data_rate": {"lora": {"bandwidth": 125000, "spreading_factor": 7}}, "frequency": "868000000"}, 
"dev_EUI": "70B3D57ED0063437", "received_at": "2024-05-10T10:56:38.669"}"""

document = payload_format(payload_str)

database_addr = "10.141.10.69:27017"
broker_addr = "10.141.10.69:1883"

add_to_database(document, database_addr, "test", "test")
downloaded = download_from_database({'time': '2024-05-10 10:56:38'}, database_addr, "test", "test")

print(downloaded)