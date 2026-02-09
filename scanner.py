import cv2
from pyzbar.pyzbar import decode

class QRScanner:
    def __init__(self):
        self.cap = None

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)

    def read_frame(self):
        if not self.cap:
            return None, None

        ret, frame = self.cap.read()
        if not ret:
            return None, None

        data = None
        for qr in decode(frame):
            data = qr.data.decode("utf-8")
            x, y, w, h = qr.rect
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        return frame, data

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
