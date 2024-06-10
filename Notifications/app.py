import asyncio
import websockets
import json
from flask import Flask, jsonify, request
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_pymongo import PyMongo
from threading import Thread
import requests
import base64
from websockets.http import Headers

MYSQL_IP = 'mysql-service'
MONGO_IP = 'mongo-service'

AUTHORIZE_IP = 'authorize-service'

app = Flask(__name__)
app.config['MONGO_URI'] = f'mongodb://{MONGO_IP}:27017/data_db'
mongo = PyMongo(app)

# Database configuration
db_config = {
    'host': MYSQL_IP,
    'port': '3333',
    'user': 'root',
    'password': 'password',
    'database': 'mysql'
}

auth_service_url = f'http://{AUTHORIZE_IP}:5000'

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

# Dict to keep track of connected WebSocket clients
clients = {}


def check_credentials(username, password):
    data = {'username': username, 'password': password}
    response = requests.post(auth_service_url + '/check_credentials', data=data)

    if response.status_code == 200:
        return response.json()['valid']
    return False


def get_user_of_device(device_id):
    user = mongo.db.hives.find_one({"hives": device_id})

    return user['user_id'] if user else None


async def authenticate(path, headers):
    auth_header = headers.get("Authorization")
    if auth_header is None:
        return False

    auth_type, auth_credentials = auth_header.split(' ', 1)
    if auth_type.lower() != "basic":
        return False

    decoded_credentials = base64.b64decode(auth_credentials).decode("utf-8")
    input_username, input_password = decoded_credentials.split(":", 1)

    if check_credentials(input_username, input_password):
        return input_username
    return False


async def handler(websocket, path):
    headers = websocket.request_headers
    username = await authenticate(path, headers)

    if not username:
        # Send 401 Unauthorized response
        response_headers = Headers()
        response_headers["WWW-Authenticate"] = 'Basic realm="Access to websocket"'
        await websocket.send(json.dumps({"error": "Unauthorized"}))
        await websocket.close(code=1008)
        return

    # Authentication successful
    await websocket.send(f"Hello {username}, authenticated client!")
    clients[username] = websocket

    try:
        async for message in websocket:
            await websocket.send(f"Received your message: {message}")
    finally:
        print(f"Client {username} disconnected")
        del clients[username]


@app.route('/notify', methods=['POST'])
def notify():
    """
    Send a notification to the user associated with the device.
    ---
    parameters:
      - name: device_id
        in: formData
        description: The device ID to send the notification to.
        required: true
        type: string
        responses:
            200:
                description: A response indicating the notification was sent.
                schema:
                    type: object
                    properties:
                        status:
                            type: string
                            description: Indicates the status of the notification.
                        notification:
                            type: object
                            description: The notification message sent.
                            properties:
                                message:
                                    type: string
                                    description: The message of the notification.
            404:
                description: The device ID or user was not found.
                schema:
                    type: object
                    properties:
                        status:
                            type: string
                            description: Indicates the status of the notification.
                        message:
                            type: string
                            description: The error message.
    """

    device_id = request.form.get('device_id')
    username = get_user_of_device(device_id)

    if not username:
        return jsonify({'status': 'Failed', 'message': 'User not found'}), 404

    if username not in clients:
        return jsonify({'status': 'Failed', 'message': 'User not connected'}), 404

    notification = {'message': f'Notification for {username} from device {device_id}'}
    asyncio.run(send_notification(notification, username))

    return jsonify({'status': 'Notification sent', 'notification': notification})


async def send_notification(notification, username):
    if username in clients:
        websocket = clients[username]
        await websocket.send(json.dumps(notification))
    else:
        print(f'User {username} not connected')


@app.route(API_URL)
def swagger_json():
    return jsonify(swagger(app))


def run_flask():
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "PAM Server"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.run(host='0.0.0.0')


async def run_socket_server():
    server = await websockets.serve(handler, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    asyncio.run(run_socket_server())
