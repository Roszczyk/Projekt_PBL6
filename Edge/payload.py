import json
from datetime import datetime
from measurements import measure_temp, measure_humidity, measure_gps, measure_digital_ins

def prepare_payload(dev):
    payload_str = """
    {
        "f_port": 1,
        "frm_payload": "AGcBEwBoRgCIBcOAGcBDQBoRQ==",
        "decoded_payload": {
        },
        "rx_metadata": [
            {
                "gateway_ids": {
                    "gateway_id": "test"
                },
                "rssi": 42,
                "channel_rssi": 42,
                "snr": 4.2
            }
        ],
        "settings": {
            "data_rate": {
                "lora": {
                    "bandwidth": 125000,
                    "spreading_factor": 7
                }
            },
            "frequency": "868000000"
        }
    }
    """
    
    data = json.loads(payload_str)

    data["decoded_payload"]["temperature_0"] = dev.temperature
    data["decoded_payload"]["relative_humidity_0"] = dev.humidity
    data["device_id"] = dev.device_id

    time = datetime.now()

    formatted_time = time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    data["received_at"] = formatted_time
    print(data["received_at"])

    data["decoded_payload"]["gps_0"] = {}
    data["decoded_payload"]["gps_0"]["latitude"] = dev.gps["latitude"]
    data["decoded_payload"]["gps_0"]["longitude"] = dev.gps["longitude"]
    data["decoded_payload"]["gps_0"]["altitude"] = 0

    if dev.digital_in["digital_in_0"] != None:
        data["decoded_payload"]["digital_in_0"] = dev.digital_in["digital_in_0"]
    if dev.digital_in["digital_in_1"] != None:
        data["decoded_payload"]["digital_in_1"] = dev.digital_in["digital_in_1"]    
    if dev.digital_in["digital_in_2"] != None:
        data["decoded_payload"]["digital_in_2"] = dev.digital_in["digital_in_2"]

    return json.dumps(data)