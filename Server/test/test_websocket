
import asyncio
import websockets
import json
import random

async def push_notifications(websocket, path):
    try:
        while True:
            # Generowanie losowej wartości dla powiadomienia
            notification = {'message': 'Nowe powiadomienie: ' + str(random.randint(1, 100))}
            
            # Konwersja na format JSON
            notification_json = json.dumps(notification)
            
            # Wysyłanie powiadomienia do klienta WebSocket
            await websocket.send(notification_json)
            
            # Oczekiwanie na kolejne powiadomienie przez określony czas (np. 5 sekund)
            await asyncio.sleep(5)
    except websockets.exceptions.ConnectionClosedError:
        print("Połączenie z klientem zostało zamknięte.")

# Uruchomienie serwera
start_server = websockets.serve(push_notifications, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
