import os
import requests
import time
from pymongo import MongoClient
from datetime import datetime
from inference import get_model
import cv2
from flask import Flask

STREAMER_IP = 'streamer'
NOTIFICATIONS_IP = 'notifications'
MONGO_IP = 'mongo'

app = Flask(__name__)

# Configuration
IMAGE_URL = f"http://{STREAMER_IP}:5000/currentframe.jpg"
SAVE_DIRECTORY = "images/"
NOTIFICATIONS_URL = f"http://{NOTIFICATIONS_IP}:5000/notify"

DB_URL = f"{MONGO_IP}:27017"
DB_NAME = "data_db"
DB_COLLECTION = "hornet"


def fetch_save_post_image(collection, model):
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

            image = cv2.imread(filename)

            if not detect_hornet(model, image):
                print("No hornet detected.")
                return

            print("Hornet detected!!! . Uploading to the REST endpoint.")
            collection.insert_one({"timestamp": datetime.now()})

            data = {'device_id': 'camera'}
            response = requests.post(NOTIFICATIONS_URL, data=data)

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
    model = get_model(model_id="bees-and-hornets/5", api_key="CrSPqvFYNiL2LIDjXDl4")

    while True:
        fetch_save_post_image(collection, model)
        time.sleep(interval)


def detect_hornet(model, image):
    results = model.infer(image)
    results = results[0]
    predictions = dict(results)["predictions"]
    detected_animals = []

    for prediction in predictions:
        detected_animals.append(dict(prediction)["class_name"])

    if "Hornets" in detected_animals:
        return True
    return False


if __name__ == "__main__":
    # Start periodic task
    interval_seconds = 10
    periodic_task(interval_seconds)
