from edge_mqtt import broker_publish, broker_subscribe_init, broker_subscribe_loop, publish_measurements_thread
from payload import prepare_payload
from measurements import measure_temp, measure_humidity, measure_gps, measure_digital_ins, measure_function
import time
from threading import Thread

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
        # operacja zmiany diody na hardware
        self.light = new_state

    def change_heating(self, new_state):
        # operacja zmiany diody na hardware
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


if __name__ == "__main__":
    mqtt_user = "rw"
    mqtt_password = "readwrite"
    mqtt_listen_topic = "PAM-PBL6-PUB"
    mqtt_publish_topic = "PAM-PBL5-CATCHER"
    broker_addr = {"ip":"10.141.10.69", "port":1883}

    dev = DeviceStatus("2")

    dev.measure_all()
    client = broker_subscribe_init(mqtt_listen_topic, broker_addr["ip"], broker_addr["port"], mqtt_user, mqtt_password, dev)

    thread_sub = Thread(target=broker_subscribe_loop, args=(client,), daemon=True)
    thread_pub = Thread(target=publish_measurements_thread, args=(dev, broker_addr, mqtt_user, mqtt_password, mqtt_publish_topic), daemon=True)
    thread_meas = Thread(target=measure_function, args=(dev,), daemon=True)

    thread_sub.start()
    thread_pub.start()
    thread_meas.start()

    thread_sub.join()
    thread_pub.join()
    thread_meas.join()

