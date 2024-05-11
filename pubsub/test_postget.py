import requests

def send_post_request(url, data):
    response = requests.post(url, data=data)
    print("Response:", response.text)

# Przykład użycia
if __name__ == '__main__':
    # Adres URL serwera, na którym nasłuchuje aplikacja
    server_url = "http://localhost:2137"  # Zmodyfikuj port, jeśli inny został użyty

    # Dane, które chcesz przesłać w żądaniu POST
    post_data = {'key1': 'value1', 'key2': 'value2'}

    # Wysłanie żądania POST
    send_post_request(server_url, post_data)