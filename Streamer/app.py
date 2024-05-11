import cv2
from flask import Flask, Response

app = Flask(__name__)


def capture_frame():
    cap = cv2.VideoCapture('rtmp://10.141.10.69/live')

    ret, frame = cap.read()
    if not ret:
        return None

    ret, buffer = cv2.imencode('.jpg', frame)
    frame_jpg = buffer.tobytes()

    cap.release()
    return frame_jpg


@app.route('/currentframe.jpg')
def current_frame():
    frame = capture_frame()
    if frame is None:
        return "Failed to capture frame from stream", 500

    return Response(frame, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True, port=5003)
