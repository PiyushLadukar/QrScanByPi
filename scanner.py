import cv2
from pyzbar.pyzbar import decode

class CameraScanner:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        data = None
        for qr in decode(frame):
            data = qr.data.decode("utf-8")
            x, y, w, h = qr.rect
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        return frame, data

    def release(self):
        self.cap.release()
