import asyncio
import websockets
import json
from flask import Flask, jsonify, request
import mysql.connector
from threading import Thread

app = Flask(__name__)

# Database configuration
db_config = {
    'host': '10.141.10.69',
    'port': '3333',
    'user': 'root',
    'password': 'password',
    'database': 'mysql'
}

# List to keep track of connected WebSocket clients
clients = {}


async def push_notifications(websocket, path):
    ip = websocket.remote_address[0]  # IS it correct?
    clients[ip] = websocket
    try:
        while True:
            await asyncio.sleep(5)  # Keep connection alive with dummy notification
    except websockets.exceptions.ConnectionClosedError:
        print("Connection with client closed.")
    finally:
        clients.pop(ip)


async def send_notification(notification, ip):
    notification_json = json.dumps(notification)
    if clients:

        await asyncio.wait([client.send(notification_json) for client in clients])


def get_recent_user_ip(username):
    """Retrieve the recent IP address of the user from the MySQL database."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT recent_ip FROM users_ip WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None


@app.route('/notify', methods=['POST'])
def notify():
    device_id = request.form.get('device_id')
    username = get_user_of_device(device_id)
    ip = get_recent_ip(username)
    notification = {'message': f'Notification for {username}: Recent IP is {ip}'}

    # Send notification via WebSocket
    asyncio.run(send_notification(notification, ip))

    return jsonify({'status': 'Notification sent', 'notification': notification})


def run_flask():
    app.run(debug=True, port=5001)


# Start Flask app in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Start WebSocket server
start_server = websockets.serve(push_notifications, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
