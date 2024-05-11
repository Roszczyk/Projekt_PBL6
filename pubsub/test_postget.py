import requests
from datetime import datetime

def send_post_request(url, data):
    response = requests.post(url, data=data)
    print("Response:", response.text)

if __name__ == '__main__':
    server_url = "http://localhost:2137"  
    post_data = {
        'device_id': '2', 
        'timestamp': datetime.now(),
        "lights" : False
    }
    send_post_request(server_url, post_data)