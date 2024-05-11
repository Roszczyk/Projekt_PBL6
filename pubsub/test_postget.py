import requests

def send_post_request(url, data):
    response = requests.post(url, data=data)
    print("Response:", response.text)

if __name__ == '__main__':
    server_url = "http://localhost:2137"  
    post_data = {'key1': 'value1', 'key2': 'value2'}
    send_post_request(server_url, post_data)