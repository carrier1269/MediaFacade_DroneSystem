from flask import Flask, render_template, Response, request
from flask_cors import CORS
import threading
from drone_opencv import window
import cv2
import win32gui

window_yolov5_capture = "Result View"

output_frame = None
output_yolov5_frame = None
lock = threading.Lock()

app = Flask(__name__)
CORS(app)

def capture_yolov5_frames():
    global output_yolov5_frame
    ESC_KEY = 27
    FRAME_RATE = 120
    SLEEP_TIME = 1 / FRAME_RATE

    capture = window.WindowCapture(window_yolov5_capture, FRAME_RATE)

    while True:
        _, frame = capture.screenshot()
        with lock:
            output_yolov5_frame = frame.copy()

def generate_yolov5_frames():
    global output_yolov5_frame
    while True:
        with lock:
            if output_yolov5_frame is None:
                continue

            flag, encoded_image = cv2.imencode('.jpg', output_yolov5_frame)
            if not flag:
                continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')
        
@app.route('/')
def index():
    # return render_template('index.html')
    return print('6000!!!')

@app.route('/yolov5_live_stream')
def yolov5_live_stream():
    return Response(generate_yolov5_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    capture_yolov5_thread = threading.Thread(target=capture_yolov5_frames)
    capture_yolov5_thread.start()
    app.run(host='0.0.0.0', port=8080)