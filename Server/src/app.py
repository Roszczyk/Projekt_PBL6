# MobileApi
# Author: PAM

import requests
from datetime import datetime
from time import time
from distutils.util import strtobool

from flask import Flask, request, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_pymongo import PyMongo
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://10.141.10.69:27017/data_db'
mongo = PyMongo(app)

EXIST = {"$exists": True}
DESC = [("timestamp", -1)]

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'


class CustomBasicAuth(BasicAuth):
    def __init__(self, app, auth_service_url):
        super().__init__(app)
        self.auth_service_url = auth_service_url

    def check_credentials(self, username, password):
        data = {'username': username, 'password': password}
        response = requests.post(self.auth_service_url + '/check_credentials', data=data)
        if response.status_code == 200:
            return response.json()['valid']
        return False

    # FUNKCJA DO TESTÓW
    # def check_credentials(self, username, password):
    #     return (username == 'admin' and password == 'admin') or (username == 'username' and password == 'password')


auth_service_url = 'http://localhost:5001'
custom_basic_auth = CustomBasicAuth(app, auth_service_url)


class Command:
    def __init__(self, device_id=None, timestamp=None, lights=None, heating=None):
        self.device_id = device_id
        self.timestamp = timestamp
        self.lights = lights
        self.heating = heating


class SensorData:
    def __init__(self, device_id=None, timestamp=None, temperature=None, humidity=None, gps_lat=None, gps_lon=None, digital_in=None, noise=None, activity=None, lights=None, heating=None):
        self.device_id = device_id
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity
        self.gps_lat = gps_lat
        self.gps_lon = gps_lon
        self.digital_in = digital_in
        self.noise = noise
        self.activity = activity
        self.lights = lights
        self.heating = heating


class UserHives:
    def __init__(self, user_id=None, hives=[]):
        self.user_id = user_id
        self.hives = hives


@app.route('/<user_id>/hives', methods=['GET'])
@custom_basic_auth.required
def get_hives(user_id):
    """
    Get the list of hives for a user.
    ---
    parameters:
      - name: user_id
        in: path
        description: The user ID.
        required: true
        type: string
    responses:
        200:
            description: The list of hives.
            schema:
                type: object
                properties:
                    user_id:
                        type: string
                    hives:
                        type: array
                        items:
                            type: string
        204:
            description: No hives found.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    user_hives = mongo.db.hives.find_one({"user_id": user_id})

    if user_hives:
        return jsonify(user_hives)
    else:
        return jsonify({'message': 'No hives found.'}), 204


@app.route('/<device_id>/sensors', methods=['GET'])
@custom_basic_auth.required
def get_sensors(device_id):
    """
    Get current GPS location, temperature, humidity and digital input and state of lights, heating.
    ---
    parameters:
      - name: device_id
        in: path
        description: The device ID.
        required: true
        type: string
    responses:
        200:
            description: Current GPS location, temperature and humidity.
            schema:
                type: object
                properties:
                    gps_lat:
                        type: number
                    gps_lon:
                        type: number
                    temperature:
                        type: number
                    humidity:
                        type: number
                    digital_in:
                        type: boolean
                    noise:
                        type: boolean
                    activity:
                        type: boolean
                    lights:
                        type: boolean
                    heating:
                        type: boolean
    """

    data_tempHum = mongo.db.telemetry.find_one(
        {"temperature": EXIST, "humidity": EXIST, "device_id": device_id}, sort=DESC)
    data_gps = mongo.db.telemetry.find_one({"gps_lat": EXIST, "gps_lon": EXIST, "device_id": device_id}, sort=DESC)
    data_digital_in = mongo.db.telemetry.find_one({"digital_in": EXIST, "device_id": device_id}, sort=DESC)
    data_noise = mongo.db.telemetry.find_one({"noise": EXIST, "device_id": device_id}, sort=DESC)

    sensor_data = SensorData(device_id=device_id, timestamp=datetime.now())

    if data_tempHum:
        sensor_data.temperature = data_tempHum['temperature']
        sensor_data.humidity = data_tempHum['humidity']

    if data_gps:
        sensor_data.gps_lat = data_gps['gps_lat']
        sensor_data.gps_lon = data_gps['gps_lon']

    if data_digital_in:
        sensor_data.digital_in = data_digital_in['digital_in']

    if data_noise:
        sensor_data.noise = data_noise['noise']
        sensor_data.activity = data_noise['activity']

    cmd_lights = mongo.db.commands.find_one({"lights": EXIST, "device_id": device_id}, sort=DESC)
    cmd_heating = mongo.db.commands.find_one({"heating": EXIST, "device_id": device_id}, sort=DESC)

    if cmd_lights:
        sensor_data.lights = cmd_lights['lights']
    if cmd_heating:
        sensor_data.heating = cmd_heating['heating']

    print(time(), sensor_data.__dict__)
    return jsonify(sensor_data.__dict__)


@app.route('/<device_id>/gps', methods=['GET'])
@custom_basic_auth.required
def get_gps(device_id):
    """
    Get current GPS location.
    ---
    parameters:
      - name: device_id
        in: path
        description: The device ID.
        required: true
        type: string
    responses:
        200:
            description: Current GPS location.
            schema:
                type: object
                properties:
                    timestamp:
                        type: string
                        format: date-time
                    gps_lat:
                        type: number
                    gps_lon:
                        type: number
        204:
            description: No GPS location available.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    sensor_data = SensorData(device_id=device_id, timestamp=datetime.now())

    data = mongo.db.telemetry.find_one({"gps_lat": EXIST, "gps_lon": EXIST, "device_id": device_id}, sort=DESC)

    if data:
        sensor_data.gps_lat = data['gps_lat']
        sensor_data.gps_lon = data['gps_lon']
        print(time(), sensor_data.__dict__)
        return jsonify(sensor_data.__dict__)
    else:
        return jsonify({'message': 'No GPS location available.'}), 204


@app.route('/<device_id>/<cmd>', methods=['POST'])
@custom_basic_auth.required
def post_data(device_id, cmd):
    """
    Publishes lights/ heating boolean value to the MQTT broker.
    ---
    parameters:
      - name: device_id
        in: path
        description: The device ID.
        required: true
        type: string
      - name: cmd
        in: path
        description: The path to publish the data to.
        required: true
        type: string
        enum: [lights, heating]
      - name: value
        in: query
        description: The value to publish.
        required: true
        type: boolean
    responses:
        200:
            description: Data published successfully.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The success message.
        400:
            description: Invalid path or value.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    if cmd not in ('lights', 'heating'):
        return jsonify({'message': 'Invalid path.'}), 400

    value = request.args.get('value')
    if value is None:
        return jsonify({'message': 'Invalid value. A boolean is required.'}), 400

    # Convert the value to a boolean
    try:
        value = bool(strtobool(value))
    except ValueError:
        return jsonify({'message': 'Invalid value. A boolean is required.'}), 400

    last_value = mongo.db.commands.find_one({cmd: EXIST, "device_id": device_id}, sort=DESC)
    if value == last_value:
        return jsonify({'message': 'Data already up to date.'}), 200

    mongo.db.commands.insert_one(Command(device_id=device_id, timestamp=datetime.now(), **{cmd: value}).__dict__)

    # POST to PubSub over http

    return jsonify({'message': 'Data published successfully.'}), 200


@app.route(API_URL)
def swagger_json():
    return jsonify(swagger(app))


if __name__ == '__main__':
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "PAM Server"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    app.run()
