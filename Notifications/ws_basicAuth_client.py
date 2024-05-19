import asyncio
import websockets
import base64

# Hardcoded credentials to match the server's credentials
USERNAME = "admin"
PASSWORD = "admin"

# USERNAME = "username"
# PASSWORD = "password"

# USERNAME = "wrong_username"
# PASSWORD = "blablabla"


async def test_websocket():
    uri = "ws://localhost:8765"

    # Encode the credentials
    credentials = f"{USERNAME}:{PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'basic {encoded_credentials}'
    }

    async with websockets.connect(uri, extra_headers=headers) as websocket:
        try:
            for _ in range(10):  # Receive 10 notifications
                notification = await websocket.recv()
                print(f"Received notification: {notification}")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Run the test client
asyncio.get_event_loop().run_until_complete(test_websocket())
