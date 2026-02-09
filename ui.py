from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
import cv2
import pyperclip
from scanner import QRScanner
from utils import save_history, open_browser
from pyzbar.pyzbar import decode
from PIL import Image


class QRScannerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Scan By Piyush Ladukar")
        self.setGeometry(200, 80, 1100, 800)
        self.setAcceptDrops(True)
        self.setStyleSheet("background:#f8fafc;")

        self.scanner = QRScanner()
        self.timer = QTimer()
        self.scan_line_y = 0
        self.scan_dir = 5

        self.build_ui()

    # ---------------- UI ----------------
    def build_ui(self):
        main = QVBoxLayout(self)
        main.setSpacing(18)

        # 🧊 DROP ZONE
        self.drop_zone = QLabel("Drag & Drop QR Image Here")
        self.drop_zone.setFixedHeight(200)
        self.drop_zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_zone.setStyleSheet("""
            QLabel {
                background: rgba(255,255,255,0.9);
                border: 2px dashed #2563eb;
                border-radius: 20px;
                color: #2563eb;
                font-size: 22px;
                font-weight: 600;
            }
        """)
        main.addWidget(self.drop_zone)

        # 🎥 CAMERA PANEL
        self.video = QLabel("Camera Preview")
        self.video.setMinimumHeight(320)
        self.video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video.setStyleSheet("""
            QLabel {
                background: white;
                border-radius: 18px;
                border: 1px solid #e2e8f0;
                color:#64748b;
                font-size:18px;
            }
        """)
        main.addWidget(self.video)

        # 🔘 BUTTONS
        btns = QHBoxLayout()

        cam_btn = QPushButton("📷 Open Camera")
        cam_btn.clicked.connect(self.start_camera)

        upload_btn = QPushButton("📁 Upload Image")
        upload_btn.clicked.connect(self.upload_image)

        for b in (cam_btn, upload_btn):
            b.setStyleSheet(self.btn_style())
            btns.addWidget(b)

        main.addLayout(btns)

        # 🟦 RESULT PANEL
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFixedHeight(140)
        self.result_box.setPlaceholderText("Scanned result will appear here...")
        self.result_box.setStyleSheet("""
            QTextEdit {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
                padding: 14px;
                font-size: 15px;
            }
        """)
        main.addWidget(self.result_box)

        # RESULT ACTION BUTTONS
        actions = QHBoxLayout()

        open_btn = QPushButton("🌐 Open Browser")
        open_btn.clicked.connect(self.open_link)

        copy_btn = QPushButton("📋 Copy")
        copy_btn.clicked.connect(self.copy_text)

        clear_btn = QPushButton("✖ Clear")
        clear_btn.clicked.connect(self.clear_result)

        for b in (open_btn, copy_btn, clear_btn):
            b.setStyleSheet(self.btn_style(light=True))
            actions.addWidget(b)

        main.addLayout(actions)

        # 👣 FOOTER
        footer = QLabel("Built by Piyush Ladukar")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color:#64748b; font-size:13px;")
        main.addWidget(footer)

    def btn_style(self, light=False):
        if light:
            return """
            QPushButton {
                background: #e2e8f0;
                color: #0f172a;
                font-size: 14px;
                padding: 10px 22px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: #cbd5f5;
            }
            """
        return """
        QPushButton {
            background: #2563eb;
            color: white;
            font-size: 16px;
            padding: 14px 34px;
            border-radius: 14px;
        }
        QPushButton:hover {
            background: #1d4ed8;
        }
        """

    # ---------------- CAMERA ----------------
    def start_camera(self):
        self.scanner.start_camera()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        frame, data = self.scanner.read_frame()
        if frame is None:
            return

        h, w, _ = frame.shape
        self.scan_line_y += self.scan_dir
        if self.scan_line_y > h or self.scan_line_y < 0:
            self.scan_dir *= -1

        cv2.line(frame, (0, self.scan_line_y), (w, self.scan_line_y),
                 (37, 99, 235), 2)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(rgb.data, w, h, 3*w, QImage.Format.Format_RGB888)
        self.video.setPixmap(QPixmap.fromImage(img))

        if data:
            self.timer.stop()
            self.scanner.stop_camera()
            self.display_result(data)

    # ---------------- IMAGE ----------------
    def upload_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            self.scan_image(path)

    def scan_image(self, path):
        img = Image.open(path)
        decoded = decode(img)
        if decoded:
            self.display_result(decoded[0].data.decode("utf-8"))

    # ---------------- RESULT HANDLING ----------------
    def display_result(self, data):
        self.result_box.setText(data)
        save_history(data)

    def open_link(self):
        text = self.result_box.toPlainText()
        if text.startswith("http"):
            open_browser(text)

    def copy_text(self):
        pyperclip.copy(self.result_box.toPlainText())

    def clear_result(self):
        self.result_box.clear()

    # ---------------- DRAG & DROP ----------------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        path = event.mimeData().urls()[0].toLocalFile()
        self.scan_image(path)
