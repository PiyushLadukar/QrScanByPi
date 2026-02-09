import sys
from PyQt6.QtWidgets import QApplication
from ui import QRScannerApp

app = QApplication(sys.argv)
window = QRScannerApp()
window.show()
sys.exit(app.exec())
self.setAcceptDrops(True)   
