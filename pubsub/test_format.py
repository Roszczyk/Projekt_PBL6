from pubsub_db import payload_format
from pubsub_db import add_to_database

payload_str = """{"f_port": 1, "device_id" : "2", "frm_payload": "AGcBEwBoRgCIBcOAGcBDQBoRQ==", \\ 
    "decoded_payload": {"temperature_0": 34.91, "presence_0":"0xFF", "relative_humidity_0": 24.95, "digital_in_1": true, \\
    "digital_in_2": true}, "rx_metadata": [{"gateway_ids": {"gateway_id": "test"}, "rssi": 42, "channel_rssi": 42, "snr": 4.2}], \\
    "settings": {"data_rate": {"lora": {"bandwidth": 125000, "spreading_factor": 7}}, "frequency": "868000000"}, \\
    "dev_EUI": "70B3D57ED0063437", "received_at": "2024-05-10T10:56:38.669"}"""

formated = payload_format(payload_str)

add_to_database(formated, "mongodb://10.141.10.72:32717/", "data_db", "telemetry")

print(formated)