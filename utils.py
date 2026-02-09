import webbrowser
import os
from datetime import datetime

def save_history(data):
    os.makedirs("history", exist_ok=True)
    with open("history/scans.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} -> {data}\n")

def open_browser(url):
    webbrowser.open(url)
