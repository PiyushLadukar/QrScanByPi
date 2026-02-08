import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import cv2
from scanner import CameraScanner
from utils import handle_result
from PIL import Image
from pyzbar.pyzbar import decode
import os

class QRScannerUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("QR Scanner Pro")
        self.root.geometry("1000x650")
        self.root.configure(bg="#0b1220")

        self.camera = CameraScanner()

        self.build_header()
        self.build_canvas()
        self.build_controls()

        # CAMERA AUTO START
        self.anim = FuncAnimation(
            self.fig,
            self.update_frame,
            interval=30,
            cache_frame_data=False
        )

        # Drag & Drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.on_drop)

    # ---------- UI SECTIONS ----------

    def build_header(self):
        header = tk.Label(
            self.root,
            text="🔍 QR Scanner Pro",
            font=("Segoe UI", 26, "bold"),
            fg="white",
            bg="#0b1220"
        )
        header.pack(pady=15)

    def build_canvas(self):
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor("#0b1220")
        self.ax.axis("off")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def build_controls(self):
        bar = tk.Frame(self.root, bg="#0b1220")
        bar.pack(pady=15)

        tk.Button(
            bar, text="📁 Upload Image",
            font=("Segoe UI", 13, "bold"),
            bg="#2563eb", fg="white",
            padx=20, pady=10,
            command=self.upload_image
        ).pack(side=tk.LEFT, padx=15)

        tk.Button(
            bar, text="📜 View History",
            font=("Segoe UI", 13, "bold"),
            bg="#16a34a", fg="white",
            padx=20, pady=10,
            command=self.show_history
        ).pack(side=tk.LEFT, padx=15)

        hint = tk.Label(
            self.root,
            text="📌 Tip: Drag & Drop an image anywhere to scan",
            fg="#94a3b8",
            bg="#0b1220",
            font=("Segoe UI", 11)
        )
        hint.pack(pady=5)

    # ---------- LOGIC ----------

    def update_frame(self, i):
        frame, data = self.camera.get_frame()
        if frame is None:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.ax.imshow(frame)
        self.ax.axis("off")

        if data:
            handle_result(data)

    def upload_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )
        if path:
            self.scan_image(path)

    def on_drop(self, event):
        path = event.data.strip("{}")
        if os.path.isfile(path):
            self.scan_image(path)

    def scan_image(self, path):
        img = Image.open(path)
        decoded = decode(img)
        if decoded:
            handle_result(decoded[0].data.decode("utf-8"))
        else:
            messagebox.showerror("No QR", "No QR code found in image")

    def show_history(self):
        try:
            with open("history/scans.txt", "r", encoding="utf-8") as f:
                data = f.read()
            messagebox.showinfo("Scan History", data or "No scans yet")
        except:
            messagebox.showinfo("Scan History", "No history found")

    def run(self):
        self.root.mainloop()
