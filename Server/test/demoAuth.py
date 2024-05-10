from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
import random
from flask_basicauth import BasicAuth

app = Flask(__name__)


class CustomBasicAuth(BasicAuth):
    def check_credentials(self, username, password):
        print(f"Username: {username}, Password: {password}")
        return (username == 'admin' or username == 'username') and (password == 'admin' or password == 'password')


# Configure basic authentication using the custom BasicAuth subclass
custom_basic_auth = CustomBasicAuth(app)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Random Sensor Data API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger_json():
    return jsonify(swagger(app))


@app.route('/data/sensors', methods=['GET'])
@custom_basic_auth.required
def get_sensors():
    """
    Get current GPS location, temperature, humidity, digital input, state of lights, and heating.
    ---
    responses:
        200:
            description: Current GPS location, temperature, and humidity.
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
    result = {
        'temperature': random.uniform(-10, 40),  # Random temperature between -10 and 40 Celsius
        'humidity': random.uniform(0, 100),     # Random humidity between 0% and 100%
        'gps_lat': random.uniform(-90, 90),      # Random latitude between -90 and 90
        'gps_lon': random.uniform(-180, 180),    # Random longitude between -180 and 180
        'digital_in': random.choice([True, False]),  # Random digital input (True or False)
        'noise': random.choice([True, False]),   # Random noise state (True or False)
        'activity': random.choice([True, False]),  # Random activity state (True or False)
        'lights': random.choice([True, False]),  # Random lights state (True or False)
        'heating': random.choice([True, False])  # Random heating state (True or False)
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
