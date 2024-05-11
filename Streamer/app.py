import cv2
from flask import Flask, Response
import numpy as np

app = Flask(__name__)

# Function to generate frames from the RTMP stream


def generate_frames():
    # Replace 'rtmp://your_stream_url' with your RTMP stream URL
    cap = cv2.VideoCapture('rtmp://10.141.10.69/live')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Route to serve the current frame as JPEG


@app.route('/currentframe.jpg')
def current_frame():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, port=5003)
