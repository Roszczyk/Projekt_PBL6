import os
import requests
import time
from flask import Flask

app = Flask(__name__)

# Configuration
IMAGE_URL = "http://127.0.0.1:5003/currentframe.jpg"
SAVE_DIRECTORY = "images/"
REST_ENDPOINT = "http://your_rest_endpoint.com/upload"


def fetch_save_post_image():
    try:
        # Fetch image from URL
        response = requests.get(IMAGE_URL)
        if response.status_code == 200:
            # Create save directory if not exists
            os.makedirs(SAVE_DIRECTORY, exist_ok=True)

            # Generate unique filename
            filename = f"{SAVE_DIRECTORY}demo.jpg"

            # Save image to disk
            with open(filename, 'wb') as f:
                f.write(response.content)

            # POST image to REST endpoint
            files = {'image': open(filename, 'rb')}
            response = requests.post(REST_ENDPOINT, files=files)

            # Check if POST request was successful
            if response.status_code == 200:
                print("Image successfully posted to the REST endpoint.")
            else:
                print("Failed to post image to the REST endpoint.")

    except Exception as e:
        print("An error occurred:", str(e))


def periodic_task(interval):
    while True:
        fetch_save_post_image()
        time.sleep(interval)


if __name__ == "__main__":
    # Start periodic task
    interval_seconds = 10
    periodic_task(interval_seconds)
