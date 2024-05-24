from inference import get_model
import supervision as sv
import cv2
import time

begin = time.time()

IMAGE = "NIC.jpg"
image = cv2.imread(IMAGE)

model = get_model(model_id="bees-and-hornets/5", api_key="CrSPqvFYNiL2LIDjXDl4")

# result = model.predict(IMAGE, confidence=40, overlap=30).json()

print(f"Load model time: {round(1000*(time.time() - begin))} ms")

begin = time.time()

results = model.infer(image)
results = results[0]
predictions = dict(results)["predictions"]
detected_animals = []

for prediction in predictions:
    detected_animals.append(dict(prediction)["class_name"])

print(detected_animals)

if len(detected_animals) == 0:
    end_result = "Nothing"
elif "Hornets" in detected_animals:
    end_result = "Hornet"
else:
    end_result = "Bees only"

print(end_result)

print(f"Time inference: {round(1000*(time.time() - begin))} ms")

detections = sv.Detections.from_inference(results)
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

sv.plot_image(annotated_image)