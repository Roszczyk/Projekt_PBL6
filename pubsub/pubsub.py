from pubsub_db import payload_format, add_to_database, download_from_database
from pubsub_broker import broker_to_database
from pubsub_http import start_server, server_to_database
import time


if __name__ == "__main__":

    payload_str = """{"f_port": 1, "frm_payload": "AGcBEwBoRgCIBcOAGcBDQBoRQ==", 
    "decoded_payload": {"temperature_0": 34.91, "presence_0":"0xFF", "relative_humidity_0": 24.95, "digital_in_1": true, 
    "digital_in_2": true}, "rx_metadata": [{"gateway_ids": {"gateway_id": "test"}, "rssi": 42, "channel_rssi": 42, "snr": 4.2}], 
    "settings": {"data_rate": {"lora": {"bandwidth": 125000, "spreading_factor": 7}}, "frequency": "868000000"}, 
    "dev_EUI": "70B3D57ED0063437", "received_at": "2024-05-10T10:56:38.669"}"""

    database_addr = "10.141.10.69:27017"
    broker_addr = {"ip":"10.141.10.69", "port":1883}

    broker_to_database("PAM-PBL5-CATCHER", broker_addr["ip"], broker_addr["port"], "rw", "readwrite", database_addr, "test", "test")
    server_to_database(2137, database_addr, "test", "test")