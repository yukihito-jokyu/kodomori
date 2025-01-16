import threading

import cv2

lock = threading.Lock()
camera = cv2.VideoCapture(0)
frame = None


def capture_frames():
    global frame
    while True:
        success, new_frame = camera.read()
        if success:
            with lock:
                frame = new_frame


def generate_frames():
    global frame
    while True:
        with lock:
            if frame is not None:
                ret, buffer = cv2.imencode(".jpg", frame)
                frame_data = buffer.tobytes()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_data + b"\r\n"
                )
