import asyncio
import websockets
import json
import random
import base64

# Hardcoded username and password for basic authentication
USERNAME = "user"
PASSWORD = "pass"


async def push_notifications(websocket, path):
    try:
        # Retrieve the request headers
        headers = websocket.request_headers

        # Check for the Authorization header
        auth_header = headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            await websocket.close(code=websockets.exceptions.WSCloseCode.UNAUTHORIZED, reason="Unauthorized")
            return

        # Decode the base64 encoded credentials
        encoded_credentials = auth_header.split(' ', 1)[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':')

        # Validate the credentials
        if username != USERNAME or password != PASSWORD:
            await websocket.close(code=websockets.exceptions.WSCloseCode.UNAUTHORIZED, reason="Unauthorized")
            return

        while True:
            # Generate a random value for the notification
            notification = {'message': 'Nowe powiadomienie: ' + str(random.randint(1, 100))}

            # Convert to JSON format
            notification_json = json.dumps(notification)

            # Send the notification to the WebSocket client
            await websocket.send(notification_json)

            # Wait for the next notification for a specified time (e.g., 5 seconds)
            await asyncio.sleep(5)
    except websockets.exceptions.ConnectionClosedError:
        print("Połączenie z klientem zostało zamknięte.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run the server
start_server = websockets.serve(push_notifications, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
