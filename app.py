from flask import Flask, render_template, request, jsonify
from pyzbar.pyzbar import decode as pyzbar_decode
from PIL import Image
import os
from datetime import datetime

app = Flask(__name__)

def save_history(data):
    os.makedirs("history", exist_ok=True)
    with open("history/scans.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -> {data}\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file"})
    f = request.files["file"]
    try:
        img = Image.open(f.stream).convert("RGB")
        results = pyzbar_decode(img)
        if results:
            data = results[0].data.decode("utf-8")
            save_history(data)
            return jsonify({"success": True, "data": data})
        return jsonify({"success": False, "error": "No QR code detected"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/history")
def history():
    path = "history/scans.txt"
    if not os.path.exists(path):
        return jsonify({"lines": []})
    with open(path, encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    return jsonify({"lines": list(reversed(lines[-30:]))})

@app.route("/save_scan", methods=["POST"])
def save_scan():
    data = request.json.get("data", "")
    if data:
        save_history(data)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
