from pubsub_db import payload_format, add_to_database, download_from_database
from pubsub_broker import broker_to_database, broker_to_database_init, broker_to_database_loop
from pubsub_http import start_server, server_to_broker, server_to_broker_init, server_to_broker_loop
import time
from threading import Thread
import signal
import sys

MONGO_IP = 'mongo-service'
BROKER_IP = 'mosquitto-service'


def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    # payload_str = """{"f_port": 1, "frm_payload": "AGcBEwBoRgCIBcOAGcBDQBoRQ==",
    # "decoded_payload": {"temperature_0": 34.91, "presence_0":"0xFF", "relative_humidity_0": 24.95, "digital_in_1": true,
    # "digital_in_2": true}, "rx_metadata": [{"gateway_ids": {"gateway_id": "test"}, "rssi": 42, "channel_rssi": 42, "snr": 4.2}],
    # "settings": {"data_rate": {"lora": {"bandwidth": 125000, "spreading_factor": 7}}, "frequency": "868000000"},
    # "dev_EUI": "70B3D57ED0063437", "received_at": "2024-05-10T10:56:38.669"}"""

    database_addr = f"{MONGO_IP}:27017"
    broker_addr = {"ip": BROKER_IP, "port": 1883}
    http_port = 5000

    database_base = "test"
    database_collection = "test"

    mqtt_user = "rw"
    mqtt_password = "readwrite"
    mqtt_listen_topic = "PAM-PBL5-CATCHER"
    mqtt_publish_topic = "PAM-PBL6-PUB"

    httpd = server_to_broker_init(http_port, mqtt_publish_topic,
                                  broker_addr["ip"], broker_addr["port"], mqtt_user, mqtt_password)
    client = broker_to_database_init(
        mqtt_listen_topic, broker_addr["ip"], broker_addr["port"], mqtt_user, mqtt_password, database_addr, database_base, database_collection)

    mqtt_thread = Thread(target=server_to_broker_loop, args=(httpd,), daemon=True)
    http_thread = Thread(target=broker_to_database_loop, args=(client,), daemon=True)

    mqtt_thread.start()
    http_thread.start()

    mqtt_thread.join()
    http_thread.join()
