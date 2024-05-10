from flask import request
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DECIMAL

import paho.mqtt.client as mqtt

from datetime import datetime, timedelta
import json
from time import time
from distutils.util import strtobool
from collections import defaultdict


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Device_EUI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dev_eui = db.Column(db.String, unique=True)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device_eui.id'))
    device = db.relationship('Device_EUI')

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(DECIMAL(precision=4, scale=1), nullable=True)
    humidity = db.Column(DECIMAL(precision=4, scale=1), nullable=True)
    gps_lat = db.Column(DECIMAL(precision=7, scale=4), nullable=True)
    gps_lon = db.Column(DECIMAL(precision=7, scale=4), nullable=True)
    noise = db.Column(db.Boolean, nullable=True)
    activity = db.Column(db.Boolean, nullable=True)
    digital_in = db.Column(db.Boolean, nullable=True)


def payload2db(payload: str, session=db.session):
    payload = json.loads(payload)

    default_dict = defaultdict(lambda: None, payload['uplink_message']['decoded_payload'])

    print("Default dict: ", default_dict)

    dev_eui = payload["end_device_ids"]['dev_eui']
    # # timestamp = datetime.fromisoformat(payload['received_at'])
    # if payload['received_at'][-1] == 'Z':
    #     payload['received_at'] = payload['received_at'][:-1]
    # timestamp = datetime.strptime(payload['received_at'], '%Y-%m-%dT%H:%M:%S.%f')
    timestamp = datetime.now()

    temperature = default_dict['temperature_0']
    humidity = default_dict['relative_humidity_0']

    gps_lat = default_dict['gps_0']['latitude'] if default_dict['gps_0'] else None
    gps_lon = default_dict['gps_0']['longitude'] if default_dict['gps_0'] else None

    noise = None
    activity = None

    if default_dict['presence_0'] == 0xFF:
        noise = True
        activity = True
    if default_dict['presence_0'] == 0xF0:
        noise = True
        activity = False
    if default_dict['presence_0'] == 0x0F:
        noise = False
        activity = True
    if default_dict['presence_0'] == 0x01:
        noise = False
        activity = False

    # noise = default_dict['digital_in_1']
    # activity = default_dict['presence_0']
    digital_in = default_dict['digital_in_0']

    print("GPS: ", gps_lat, gps_lon, " temp: ", temperature, " hum: ", humidity)

    with app.app_context():
        # Check if the device already exists in the database
        device = Device_EUI.query.filter_by(dev_eui=dev_eui).first()

        # If the device doesn't exist, create a new one
        if device is None:
            device = Device_EUI(dev_eui=dev_eui)
            session.add(device)
            session.commit()

        # Create a new Data object and add it to the database
        data = Data(device_id=device.id, timestamp=timestamp,
                    temperature=temperature, humidity=humidity, gps_lat=gps_lat, gps_lon=gps_lon, noise=noise, activity=activity, digital_in=digital_in)
        session.add(data)
        session.commit()


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(time(), "payload received")
    payload2db(payload, db.session)


def on_publish(client, userdata, mid):
    print(time(), "Message published")


# @app.route('/data/tempHum', methods=['GET'])    # stara wersja
# def get_tempHum():
#     """
#     Get temperature and humidity data for the last 24 hours.
#     ---
#     responses:
#         200:
#             description: A list of temperature and humidity data.
#             schema:
#                 type: array
#                 items:
#                     type: object
#                     properties:
#                         timestamp:
#                             type: string
#                             format: date-time
#                         temperature:
#                             type: number
#                         humidity:
#                             type: number
#     """
#     last_24h = datetime.utcnow() - timedelta(hours=24)
#     data = Data.query.filter(Data.timestamp >= last_24h).all()
#     if data:
#         result = [{'timestamp': entry.timestamp, 'temperature': entry.temperature, 'humidity': entry.humidity}
#                   for entry in data]
#         print(time(), result[:5])
#         return jsonify(result)
#     else:
#         return jsonify({'message': 'No data available.'}), 204


@app.route('/data/temp-hum', methods=['GET'])
def get_temp_hum():
    """
    Get temperature and humidity data for the last 24 hours.
    ---
    responses:
        200:
            description: A list of temperature and humidity data.
            schema:
                type: object
                properties:
                    data:
                        type: array
                        items:
                            type: object
                            properties:
                                timestamp:
                                    type: string
                                    format: date-time
                                temperature:
                                    type: number
                                humidity:
                                    type: number
    """
    last_24h = datetime.utcnow() - timedelta(hours=24)
    data = Data.query.filter(Data.timestamp >= last_24h).all()
    result = [{'timestamp': entry.timestamp, 'temperature': entry.temperature, 'humidity': entry.humidity}
              for entry in data]
    print(time(), result[:5])

    return jsonify({"data": result})


@app.route('/data/temp-hum-chart', methods=['GET'])
def get_temp_hum_chart():
    """
    Get temperature and humidity data for the last 24 hours for usage in chart - HH:mm and only 12 reads.
    ---
    responses:
        200:
            description: A list of temperature and humidity data.
            schema:
                type: object
                properties:
                    data:
                        type: array
                        items:
                            type: object
                            properties:
                                timestamp:
                                    type: string
                                    format: time (HH:mm)
                                temperature:
                                    type: number
                                humidity:
                                    type: number
    """
    last_24h = datetime.utcnow() - timedelta(hours=24)
    data = Data.query.filter(Data.timestamp >= last_24h).order_by(
        Data.timestamp.desc()).all()
    result = [{'timestamp': entry.timestamp.strftime("%H:%M"), 'temperature': entry.temperature, 'humidity': entry.humidity}
              for entry in data[:12]]
    print(time(), result)

    return jsonify({"data": result})


@app.route('/data/sensors', methods=['GET'])
def get_sensors():
    """
    Get current GPS location, temperature, humidity and digital input and state of lights, heating.
    ---
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
    data_tempHum = Data.query.filter(Data.temperature.isnot(
        None), Data.humidity.isnot(None)).order_by(Data.timestamp.desc()).first()
    data_gps = Data.query.filter(Data.gps_lat.isnot(None), Data.gps_lon.isnot(
        None)).order_by(Data.timestamp.desc()).first()
    data_digital_in = Data.query.filter(Data.digital_in.isnot(
        None)).order_by(Data.timestamp.desc()).first()
    data_noise = Data.query.filter(Data.noise.isnot(
        None)).order_by(Data.timestamp.desc()).first()

    result = {'temperature': None, 'humidity': None,
              'gps_lat': None, 'gps_lon': None, 'digital_in': None, 'noise': None, 'activity': None}

    if data_tempHum:
        result['temperature'] = data_tempHum.temperature
        result['humidity'] = data_tempHum.humidity

    if data_gps:
        result['gps_lat'] = data_gps.gps_lat
        result['gps_lon'] = data_gps.gps_lon

    if data_digital_in:
        result['digital_in'] = data_digital_in.digital_in

    if data_noise:
        result['noise'] = data_noise.noise
        result['activity'] = data_noise.activity

    result['lights'] = app.devices['lights']
    result['heating'] = app.devices['heating']

    print(time(), result)
    return jsonify(result)


@app.route('/data/gps', methods=['GET'])
def get_gps():
    """
    Get current GPS location.
    ---
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
    """
    data = Data.query.filter(Data.gps_lat.isnot(None), Data.gps_lon.isnot(
        None)).order_by(Data.timestamp.desc()).first()

    if data:
        result = {'timestamp': data.timestamp,
                  'gps_lat': data.gps_lat, 'gps_lon': data.gps_lon}
        print(time(), result)
        return jsonify(result)
    else:
        return jsonify({'message': 'No GPS location available.'}), 204


@app.route('/data/<path>', methods=['POST'])
def post_data(path):
    """
    Publishes lights/ heating boolean value to the MQTT broker.
    ---
    parameters:
      - name: path
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
    if path not in app.devices:
        return jsonify({'message': 'Invalid path.'}), 400

    value = request.args.get('value')
    if value is None:
        return jsonify({'message': 'Invalid value. A boolean is required.'}), 400

    # Convert the value to a boolean
    try:
        value = bool(strtobool(value))
    except ValueError:
        return jsonify({'message': 'Invalid value. A boolean is required.'}), 400

    if value == app.devices[path]:
        return jsonify({'message': 'Data already up to date.'}), 200

    app.devices[path] = value

    # placeholder for proper payload to Helium/TTN
    payload = {
        "f_port": 1,
        "payload": {
            path: value
        }
    }

    payload = "Nothing"

    if path == "heating" and value == True:
        payload = '{ "downlinks": [{ "f_port": 15, "frm_payload": "SDE=", "priority": "NORMAL" }] }'
    elif path == "heating" and value == False:
        payload = '{ "downlinks": [{ "f_port": 15, "frm_payload": "SDA=", "priority": "NORMAL" }] }'
    elif path == "lights" and value == True:
        payload = '{ "downlinks": [{ "f_port": 15, "frm_payload": "TDE=", "priority": "NORMAL" }] }'
    elif path == "lights" and value == False:
        payload = '{ "downlinks": [{ "f_port": 15, "frm_payload": "TDA=", "priority": "NORMAL" }] }'
    else:
        print("Something is no yes")

    print("PAYLOAD TUTAJ !!!!!!!!!!!!!!!!!!!!!1\n", payload, "\n\n")

    client.publish(topic_pub, payload)

    return jsonify({'message': 'Data published successfully.'}), 200


@app.route('/swagger.json')
def swagger_json():
    return jsonify(swagger(app))


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.devices = {'lights': False, 'heating': False}

    client = mqtt.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    mqtt_username = "pam-pbl5-app@ttn"
    device_id = "eui-70b3d57ed0062e09"

    password_mqtt = "NNSXS.AGEJAV36C5MABKJM67MAGQ6G4EZMTL37GPWUOTQ.IIL46KPPV2QZUECWURID2IUEHIV324HLP3NEV6A7OKIRMNY4LMVA"

    client.username_pw_set(mqtt_username, password_mqtt)
    client.connect("eu1.cloud.thethings.network", 1883)
    topic_sub = f"v3/{mqtt_username}/devices/{device_id}/up"
    topic_pub = f"v3/{mqtt_username}/devices/{device_id}/down/push"

    client.subscribe(topic_sub)
    client.loop_start()

    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "PAM Server"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # NAPRAWIONE: debug=False musi być, bo inaczej callbacki mqtt są dwukrotnie.
    app.run(debug=False)
