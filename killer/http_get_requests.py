import sys
import time
import requests


def send_requests(url, req_per_sec):
    while True:
        start_time = time.time()
        requests_sent = 0

        while time.time() - start_time < 1:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    requests_sent += 1
            except requests.exceptions.RequestException as e:
                print("Error:", e)

        print("Requests sent in 1 second:", requests_sent)
        time.sleep(1 / req_per_sec)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 http_get_requests.py <URL> <Requests per second>")
        url = 'http://10.141.10.72:30003/swagger/#/default/get__user_id__hives/index.html'
        req_per_sec = 10
        print(f"Using default values: URL = {url}, Requests per second = {req_per_sec}")

    else:
        url = sys.argv[1]
        req_per_sec = float(sys.argv[2])

    send_requests(url, req_per_sec)
