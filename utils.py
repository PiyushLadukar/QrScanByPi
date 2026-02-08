import webbrowser
from datetime import datetime
from tkinter import messagebox
import os

def handle_result(data):
    save_history(data)

    if data.startswith("http"):
        if messagebox.askyesno("QR Detected", "Open link in browser?"):
            webbrowser.open(data)
    else:
        messagebox.showinfo("QR Result", data)

def save_history(data):
    os.makedirs("history", exist_ok=True)
    with open("history/scans.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} -> {data}\n")
