import cv2
from flask import Flask, Response
import time
from threading import Thread

app = Flask(__name__)


frame = None
thread = None
thread_stop = False

STREAM_URL = 'rtmp://127.0.0.1/live'


def capture_frames():
    global frame, thread_stop
    cap = cv2.VideoCapture(STREAM_URL)

    while not thread_stop:
        ret, frame = cap.read()
        if not ret:
            break

        time.sleep(10)

    cap.release()


def start_capture():
    global thread
    if thread is None:
        thread = Thread(target=capture_frames)
        thread.start()


@app.route('/currentframe.jpg')
def current_frame():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames():
    global frame

    while True:
        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')


@app.route('/start')
def start():
    start_capture()
    return 'Capture started'


if __name__ == '__main__':
    app.run(debug=True)
