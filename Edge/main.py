from edge_mqtt import broker_publish, broker_subscribe_init, broker_subscribe_loop
from payload import prepare_payload
from measurements import measure_temp, measure_humidity, measure_gps, measure_digital_ins
import time

class DeviceStatus:
    def __init__(self, device_id):
        self.device_id = device_id
        self.light = False
        self.heating = False
        self.temperature = None
        self.humidity = None
        self.gps = None
        self.digital_in = None

    def measure_temp(self):
        self.temperature = measure_temp()

    def measure_humidity(self):
        self.humidity = measure_humidity()

    def measure_gps(self):
        self.gps = measure_gps()

    def measure_digital_ins(self):
        self.digital_in = measure_digital_ins()

    def change_light(self, new_state):
        self.light = new_state

    def change_heating(self, new_state):
        self.heating = new_state

    def measure_all(self):
        self.measure_temp()
        self.measure_humidity()
        self.measure_gps()
        self.measure_digital_ins()

    def print_all(self):
        print(f"DEVICE ID: {self.device_id}\n")
        print(f"Temperature \n{self.temperature}\n\nHumidity \n{self.humidity}\n")
        print(f'GPS:\nLAT {self.gps["latitude"]}\nLON {self.gps["longitude"]}\n')
        print(f'Digital INs:\n0: {self.digital_in["digital_in_0"]}\n1: {self.digital_in["digital_in_1"]}\n2: {self.digital_in["digital_in_2"]}\n')
        print(f'Lights: \n{self.light}\n\nHeating\n{self.heating}\n')


def publish_measurements(dev, mqtt_user, mqtt_password, mqtt_topic):
    message = prepare_payload(dev)
    broker_publish(message, mqtt_topic, broker_addr["ip"], broker_addr["port"], mqtt_user, mqtt_password)
    time.sleep(10)


if __name__ == "__main__":
    mqtt_user = "rw"
    mqtt_password = "readwrite"
    mqtt_listen_topic = "PAM-PBL6-PUB"
    mqtt_publish_topic = "PAM-PBL5-CATCHER"
    broker_addr = {"ip":"10.141.10.69", "port":1883}

    dev = DeviceStatus("2")

    dev.measure_all()
    client = broker_subscribe_init(mqtt_listen_topic, broker_addr["ip"], broker_addr["port"], mqtt_user, mqtt_password, dev)
    broker_subscribe_loop(client)

