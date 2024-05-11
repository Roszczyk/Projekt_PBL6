import os
import requests
import time
import random
from pymongo import MongoClient

from flask import Flask

app = Flask(__name__)

# Configuration
IMAGE_URL = "http://127.0.0.1:5003/currentframe.jpg"
SAVE_DIRECTORY = "images/"
REST_ENDPOINT = "http://your_rest_endpoint.com/upload"

DB_URL = "10.141.10.69:27017"
DB_NAME = "data_db"
DB_COLLECTION = "hornet"


def fetch_save_post_image(collection):
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

            # AI
            # AI
            detection = random.randint(0, 1)
            # AI
            # AI

            if not detection:
                print("No hornet detected.")
                return

            collection.insert_one({"timestamp": })

            response = requests.post(REST_ENDPOINT)  # POST do mikrousługi powiadomień

            if response.status_code == 200:
                print("Successfully posted to the REST endpoint.")
            else:
                print("Failed to post to the REST endpoint.")

    except Exception as e:
        print("An error occurred:", str(e))


def periodic_task(interval):
    client = MongoClient(DB_URL)
    database = client[DB_NAME]
    collection = database[DB_COLLECTION]

    while True:
        fetch_save_post_image(collection)
        time.sleep(interval)


if __name__ == "__main__":
    # Start periodic task
    interval_seconds = 10
    periodic_task(interval_seconds)
