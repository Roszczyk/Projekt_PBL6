import asyncio
import base64
import websockets
from websockets.exceptions import InvalidHandshake, InvalidStatusCode
from websockets.http import Headers

# Ustawienia użytkownika i hasła
USERNAME = "user"
PASSWORD = "password"

async def authenticate(path, headers):
    auth_header = headers.get("Authorization")
    if auth_header is None:
        return False

    auth_type, auth_credentials = auth_header.split(' ', 1)
    if auth_type.lower() != "basic":
        return False

    decoded_credentials = base64.b64decode(auth_credentials).decode("utf-8")
    input_username, input_password = decoded_credentials.split(":", 1)

    return input_username == USERNAME and input_password == PASSWORD

async def handler(websocket, path):
    headers = websocket.request_headers
    if not await authenticate(path, headers):
        # Wysłanie odpowiedzi 401 Unauthorized
        response_headers = Headers()
        response_headers["WWW-Authenticate"] = 'Basic realm="Access to websocket"'
        raise InvalidHandshake(
            status_code=401,
            headers=response_headers
        )
    
    # Jeśli uwierzytelnianie zakończyło się sukcesem
    await websocket.send("Hello, authenticated client!")
    async for message in websocket:
        await websocket.send(f"Received your message: {message}")

async def main():
    server = await websockets.serve(handler, "localhost", 8765)

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
