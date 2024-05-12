import requests
from datetime import datetime

def send_post_request(url, data):
    response = requests.post(url, data=data)
    print("Response:", response.text)

if __name__ == '__main__':
    server_url = "http://10.141.10.69:2137"  
    post_data = {
        "device_id": "2", 
        "timestamp": datetime.now(),
        "lights" : True
    }
    send_post_request(server_url, post_data)