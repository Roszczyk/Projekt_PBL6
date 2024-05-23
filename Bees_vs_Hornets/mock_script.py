from inference import get_model
import supervision as sv
import cv2

# rf = Roboflow(api_key="API_KEY")
# workspace = rf.workspace("bees-and-hornets-20yku")
# project = workspace.project("bees-and-hornets")
# model = project.version(5).model

IMAGE = "Bees/images17.jpg"
image = cv2.imread(IMAGE)

model = get_model(model_id="bees-and-hornets/5", api_key="CrSPqvFYNiL2LIDjXDl4")

# result = model.predict(IMAGE, confidence=40, overlap=30).json()

results = model.infer(image)

results = results[0]

predictions = dict(results)["predictions"]

detected_animals = []

for prediction in predictions:
    detected_animals.append(dict(prediction)["class_name"])

print(detected_animals)

# load the results into the supervision Detections api
detections = sv.Detections.from_inference(results)

# create supervision annotators
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

# annotate the image with our inference results
annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

# display the image
sv.plot_image(annotated_image)