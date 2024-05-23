from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="API_KEY"
)

result = CLIENT.infer("Bees/download.jpg", model_id="bees-and-hornets/5")