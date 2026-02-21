from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QTextEdit, QGraphicsDropShadowEffect,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve, pyqtProperty, QPoint, QSize
from PyQt6.QtGui import (
    QPixmap, QImage, QColor, QPainter, QPen, QBrush,
    QLinearGradient, QFont, QPainterPath, QConicalGradient,
    QRadialGradient, QFontDatabase, QIcon, QPolygon
)
import cv2
import pyperclip
import math
import time
from scanner import QRScanner
from utils import save_history, open_browser
from pyzbar.pyzbar import decode
from PIL import Image


# ─────────────────────────────────────────
#  Animated Glow Button
# ─────────────────────────────────────────
class GlowButton(QPushButton):
    def __init__(self, text, accent=(0, 212, 255), parent=None):
        super().__init__(text, parent)
        self.accent = accent
        self._glow = 0
        self.setFixedHeight(52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._anim = QPropertyAnimation(self, b"glow")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_glow(self): return self._glow
    def set_glow(self, v):
        self._glow = v
        self.update()
    glow = pyqtProperty(int, get_glow, set_glow)

    def enterEvent(self, e):
        self._anim.stop()
        self._anim.setStartValue(self._glow)
        self._anim.setEndValue(255)
        self._anim.start()
    def leaveEvent(self, e):
        self._anim.stop()
        self._anim.setStartValue(self._glow)
        self._anim.setEndValue(0)
        self._anim.start()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()
        a = self.accent

        # Glow halo
        if self._glow > 0:
            for i in range(8, 0, -1):
                alpha = int(self._glow * 0.04 * i)
                pen = QPen(QColor(a[0], a[1], a[2], alpha), i * 2)
                p.setPen(pen)
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawRoundedRect(r.adjusted(i, i, -i, -i), 12, 12)

        # Background
        t = self._glow / 255.0
        bg = QLinearGradient(0, 0, r.width(), r.height())
        bg.setColorAt(0, QColor(
            int(a[0] * 0.15 + a[0] * 0.25 * t),
            int(a[1] * 0.15 + a[1] * 0.25 * t),
            int(a[2] * 0.15 + a[2] * 0.25 * t),
            220
        ))
        bg.setColorAt(1, QColor(
            int(a[0] * 0.05 + a[0] * 0.15 * t),
            int(a[1] * 0.05 + a[1] * 0.15 * t),
            int(a[2] * 0.05 + a[2] * 0.15 * t),
            200
        ))
        p.setBrush(QBrush(bg))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(r.adjusted(1, 1, -1, -1), 12, 12)

        # Border
        border_alpha = 120 + int(135 * t)
        p.setPen(QPen(QColor(a[0], a[1], a[2], border_alpha), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r.adjusted(1, 1, -1, -1), 12, 12)

        # Text
        font = QFont("Consolas", 13, QFont.Weight.Bold)
        p.setFont(font)
        text_color = QColor(
            min(255, int(180 + 75 * t)),
            min(255, int(180 + 75 * t)),
            255,
            255
        )
        p.setPen(text_color)
        p.drawText(r, Qt.AlignmentFlag.AlignCenter, self.text())


# ─────────────────────────────────────────
#  Corner Frame Overlay Widget
# ─────────────────────────────────────────
class CornerFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._pulse = 0
        self._t = QTimer()
        self._t.timeout.connect(self._tick)
        self._t.start(16)
        self._phase = 0.0

    def _tick(self):
        self._phase += 0.05
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()
        glow = abs(math.sin(self._phase)) * 0.6 + 0.4
        c = QColor(0, int(212 * glow), int(255 * glow), int(200 * glow))
        pen = QPen(c, 3)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)

        size = 22
        corners = [
            (r.left(), r.top(), 1, 1),
            (r.right(), r.top(), -1, 1),
            (r.left(), r.bottom(), 1, -1),
            (r.right(), r.bottom(), -1, -1),
        ]
        for cx, cy, dx, dy in corners:
            p.drawLine(cx, cy, cx + dx * size, cy)
            p.drawLine(cx, cy, cx, cy + dy * size)


# ─────────────────────────────────────────
#  Animated Scan Line Label
# ─────────────────────────────────────────
class ScanLabel(QLabel):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._scan_y = 0
        self._scan_dir = 2
        self._phase = 0.0
        self._particles = []
        self._t = QTimer()
        self._t.timeout.connect(self._tick)
        self._t.start(16)

    def _tick(self):
        self._scan_y += self._scan_dir
        h = self.height()
        if self._scan_y > h: self._scan_dir = -2
        if self._scan_y < 0: self._scan_dir = 2
        self._phase += 0.04
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.pixmap() is None:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        glow = abs(math.sin(self._phase)) * 0.5 + 0.5

        # Scan line
        grad = QLinearGradient(0, self._scan_y, w, self._scan_y)
        grad.setColorAt(0, QColor(0, 0, 0, 0))
        grad.setColorAt(0.3, QColor(0, 212, 255, int(180 * glow)))
        grad.setColorAt(0.5, QColor(120, 255, 220, int(255 * glow)))
        grad.setColorAt(0.7, QColor(0, 212, 255, int(180 * glow)))
        grad.setColorAt(1, QColor(0, 0, 0, 0))
        p.setPen(QPen(QBrush(grad), 2))
        p.drawLine(0, self._scan_y, w, self._scan_y)

        # Glow above
        for i in range(1, 12):
            alpha = int((1 - i / 12) * 60 * glow)
            p.setPen(QPen(QColor(0, 212, 255, alpha), 1))
            p.drawLine(0, self._scan_y - i, w, self._scan_y - i)


# ─────────────────────────────────────────
#  Hexagonal Background Widget
# ─────────────────────────────────────────
class HexBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._phase = 0.0
        self._t = QTimer()
        self._t.timeout.connect(self._tick)
        self._t.start(33)

    def _tick(self):
        self._phase += 0.012
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Deep background gradient
        bg = QLinearGradient(0, 0, w, h)
        bg.setColorAt(0, QColor(2, 6, 23))
        bg.setColorAt(0.4, QColor(4, 12, 36))
        bg.setColorAt(1, QColor(2, 6, 23))
        p.fillRect(self.rect(), QBrush(bg))

        # Hex grid
        size = 32
        pw = size * 2
        ph = int(size * math.sqrt(3))
        p.setPen(QPen(QColor(0, 212, 255, 14), 1))
        p.setBrush(Qt.BrushStyle.NoBrush)
        for row in range(-1, h // ph + 2):
            for col in range(-1, w // pw + 2):
                x = col * pw + (pw // 2 if row % 2 else 0)
                y = row * ph
                wave = math.sin(self._phase + col * 0.3 + row * 0.2) * 0.5 + 0.5
                alpha = int(8 + wave * 18)
                p.setPen(QPen(QColor(0, 212, 255, alpha), 1))
                pts = []
                for i in range(6):
                    angle = math.pi / 3 * i - math.pi / 6
                    pts.append(QPoint(int(x + size * math.cos(angle)),
                                      int(y + size * math.sin(angle))))
                poly = QPolygon(pts)
                p.drawPolygon(poly)

        # Radial center glow
        glow = abs(math.sin(self._phase * 0.5)) * 0.3 + 0.05
        rg = QRadialGradient(w // 2, h // 2, max(w, h) * 0.6)
        rg.setColorAt(0, QColor(0, 100, 200, int(glow * 60)))
        rg.setColorAt(0.4, QColor(0, 50, 120, int(glow * 20)))
        rg.setColorAt(1, QColor(0, 0, 0, 0))
        p.fillRect(self.rect(), QBrush(rg))


# ─────────────────────────────────────────
#  Drop Zone with animated border
# ─────────────────────────────────────────
class DropZone(QLabel):
    def __init__(self, parent=None):
        super().__init__("⬇  DROP QR CODE HERE  ⬇", parent)
        self.setFixedHeight(110)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._phase = 0.0
        self._hover = False
        self._t = QTimer()
        self._t.timeout.connect(self._tick)
        self._t.start(16)
        self.setFont(QFont("Consolas", 15, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _tick(self):
        self._phase += 0.03
        self.update()

    def enterEvent(self, e): self._hover = True
    def leaveEvent(self, e): self._hover = False

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()
        glow = abs(math.sin(self._phase)) * 0.6 + 0.4
        intensity = 1.5 if self._hover else 1.0

        # Background
        bg = QLinearGradient(0, 0, r.width(), r.height())
        bg.setColorAt(0, QColor(0, 30, 60, 160))
        bg.setColorAt(1, QColor(0, 10, 30, 120))
        p.fillRect(r, QBrush(bg))

        # Animated dashed border
        alpha = int(min(255, 160 * glow * intensity))
        pen = QPen(QColor(0, 212, 255, alpha), 2, Qt.PenStyle.DashLine)
        pen.setDashOffset(self._phase * 8)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r.adjusted(2, 2, -2, -2), 16, 16)

        # Icon + text
        text_alpha = int(min(255, 200 * glow * intensity))
        p.setPen(QColor(0, 212, 255, text_alpha))
        p.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        p.drawText(r, Qt.AlignmentFlag.AlignCenter, self.text())


# ─────────────────────────────────────────
#  Status LED indicator
# ─────────────────────────────────────────
class StatusLED(QWidget):
    def __init__(self, label="READY", color=(0, 255, 120), parent=None):
        super().__init__(parent)
        self.label = label
        self.color = color
        self._phase = 0.0
        self.setFixedSize(120, 28)
        self._t = QTimer()
        self._t.timeout.connect(self._tick)
        self._t.start(33)

    def _tick(self):
        self._phase += 0.08
        self.update()

    def set_state(self, label, color):
        self.label = label
        self.color = color

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        glow = abs(math.sin(self._phase)) * 0.5 + 0.5
        c = self.color

        # LED dot
        dot_r = 7
        rg = QRadialGradient(dot_r + 2, 14, dot_r * 2)
        rg.setColorAt(0, QColor(c[0], c[1], c[2], int(255 * glow)))
        rg.setColorAt(0.5, QColor(c[0], c[1], c[2], int(180 * glow)))
        rg.setColorAt(1, QColor(c[0], c[1], c[2], 0))
        p.setBrush(QBrush(rg))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(2, 14 - dot_r, dot_r * 2 + 1, dot_r * 2)

        # Label
        p.setFont(QFont("Consolas", 9, QFont.Weight.Bold))
        p.setPen(QColor(c[0], c[1], c[2], 220))
        p.drawText(QRect(22, 0, 100, 28), Qt.AlignmentFlag.AlignVCenter, self.label)


# ─────────────────────────────────────────
#  Main App
# ─────────────────────────────────────────
class QRScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QRSCAN // By Pi")
        self.setGeometry(100, 60, 1000, 820)
        self.setAcceptDrops(True)
        self.setMinimumSize(800, 700)

        self.scanner = QRScanner()
        self.timer = QTimer()

        self._build_ui()

    # ─── UI BUILD ───────────────────────────
    def _build_ui(self):
        # Layered layout: background + foreground
        self.bg = HexBackground(self)
        self.bg.setGeometry(self.rect())

        # Foreground container
        self.fg = QWidget(self)
        self.fg.setGeometry(self.rect())
        self.fg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main = QVBoxLayout(self.fg)
        main.setContentsMargins(28, 20, 28, 20)
        main.setSpacing(14)

        # ── HEADER ──────────────────────────
        hdr = QHBoxLayout()
        title = QLabel("◈ QRSCAN By PI ◈")
        title.setFont(QFont("Consolas", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #00d4ff; letter-spacing: 4px;")
        effect = QGraphicsDropShadowEffect()
        effect.setColor(QColor(0, 212, 255, 160))
        effect.setBlurRadius(20)
        effect.setOffset(0, 0)
        title.setGraphicsEffect(effect)

        self.status_led = StatusLED("STANDBY", (0, 212, 255))
        version = QLabel("created by : piyush ladukar 25")
        version.setFont(QFont("Consolas", 9))
        version.setStyleSheet("color: #334155;")

        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self.status_led)
        hdr.addWidget(version)
        main.addLayout(hdr)

        # Separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #1e3a5f; background: #0d2137; max-height: 1px;")
        main.addWidget(sep)

        # ── DROP ZONE ───────────────────────
        self.drop_zone = DropZone()
        main.addWidget(self.drop_zone)

        # ── VIDEO PANEL ─────────────────────
        video_wrap = QWidget()
        video_wrap.setMinimumHeight(300)
        video_wrap.setStyleSheet("""
            QWidget {
                background: rgba(0,10,25,0.85);
                border: 1px solid #0d3a5c;
                border-radius: 20px;
            }
        """)
        vl = QVBoxLayout(video_wrap)
        vl.setContentsMargins(4, 4, 4, 4)

        self.video = ScanLabel()
        self.video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video.setFont(QFont("Consolas", 13))
        self.video.setStyleSheet("""
            QLabel {
                background: transparent;
                color: #1e4d6b;
                border-radius: 18px;
            }
        """)
        self.video.setText("[ CAMERA FEED OFFLINE ]")
        vl.addWidget(self.video)

        # Corner frame decorations
        self.corner_frame = CornerFrame(video_wrap)
        self.corner_frame.setGeometry(4, 4, video_wrap.width() - 8, video_wrap.height() - 8)

        main.addWidget(video_wrap, 1)

        # ── BUTTONS ─────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.cam_btn = GlowButton("  📷  OPEN CAMERA", accent=(0, 212, 255))
        self.cam_btn.clicked.connect(self.start_camera)

        self.upload_btn = GlowButton("  📁  UPLOAD IMAGE", accent=(120, 80, 255))
        self.upload_btn.clicked.connect(self.upload_image)

        btn_row.addWidget(self.cam_btn)
        btn_row.addWidget(self.upload_btn)
        main.addLayout(btn_row)

        # ── RESULT BOX ──────────────────────
        result_label = QLabel("◆  DECODED OUTPUT")
        result_label.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        result_label.setStyleSheet("color: #334a60; letter-spacing: 3px;")
        main.addWidget(result_label)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFixedHeight(100)
        self.result_box.setPlaceholderText("Awaiting scan data...")
        self.result_box.setFont(QFont("Consolas", 13))
        self.result_box.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 8, 20, 0.9);
                border: 1px solid #0d3a5c;
                border-radius: 14px;
                padding: 14px 18px;
                color: #00d4ff;
                selection-background-color: #0d3a5c;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
            }
            QScrollBar::handle:vertical {
                background: #0d3a5c;
                border-radius: 3px;
            }
        """)
        main.addWidget(self.result_box)

        # ── ACTION BUTTONS ──────────────────
        act_row = QHBoxLayout()
        act_row.setSpacing(10)

        self.open_btn = GlowButton("🌐  OPEN URL", accent=(0, 220, 160))
        self.open_btn.clicked.connect(self.open_link)

        self.copy_btn = GlowButton("📋  COPY", accent=(200, 160, 0))
        self.copy_btn.clicked.connect(self.copy_text)

        self.clear_btn = GlowButton("✖  CLEAR", accent=(220, 50, 80))
        self.clear_btn.clicked.connect(self.clear_result)

        for b in (self.open_btn, self.copy_btn, self.clear_btn):
            b.setFixedHeight(42)
            act_row.addWidget(b)

        main.addLayout(act_row)

        # ── FOOTER ──────────────────────────
        footer = QLabel("BUILT BY PIYUSH LADUKAR  //  QR SYSTEMS  //  2026")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setFont(QFont("Consolas", 8))
        footer.setStyleSheet("color: #1e3a5f; letter-spacing: 2px;")
        main.addWidget(footer)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.bg.setGeometry(self.rect())
        self.fg.setGeometry(self.rect())

    # ─── CAMERA ─────────────────────────────
    def start_camera(self):
        self.scanner.start_camera()
        self.status_led.set_state("SCANNING", (0, 255, 120))
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        frame, data = self.scanner.read_frame()
        if frame is None:
            return

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(rgb.data, w, h, 3 * w, QImage.Format.Format_RGB888)
        self.video.setPixmap(QPixmap.fromImage(img).scaled(
            self.video.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))

        if data:
            self.timer.stop()
            self.scanner.stop_camera()
            self.status_led.set_state("ACQUIRED", (0, 255, 120))
            self.display_result(data)

    # ─── IMAGE ──────────────────────────────
    def upload_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select QR Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if path:
            self.scan_image(path)

    def scan_image(self, path):
        img = Image.open(path)
        decoded = decode(img)
        if decoded:
            self.status_led.set_state("ACQUIRED", (0, 255, 120))
            self.display_result(decoded[0].data.decode("utf-8"))
        else:
            self.status_led.set_state("NO DATA", (255, 80, 80))

    # ─── RESULTS ────────────────────────────
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
        self.status_led.set_state("STANDBY", (0, 212, 255))

    # ─── DRAG & DROP ────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        path = event.mimeData().urls()[0].toLocalFile()
        self.scan_image(path)