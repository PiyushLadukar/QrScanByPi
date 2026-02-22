<div align="center">

<img src="https://capsule-render.vercel.app/api?type=venom&height=280&text=QR_SCANNER&fontSize=85&color=0:00fff7,50:ff00c8,100:ffe500&fontColor=ffffff&fontAlignY=55&stroke=00fff7&strokeWidth=2&desc=by%20PI%20%E2%80%94%20Web-Based%20QR%20Scanner&descAlignY=75&descSize=18&animation=fadeIn" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=800&size=18&duration=2000&pause=300&color=00FFF7&center=true&vCenter=true&width=800&height=40&lines=⚡+Real-time+camera+QR+scanning;🌐+Flask+powered+web+app;🖼️+Upload+any+image,+decode+instantly;🖱️+Drag+%26+Drop+support;🔥+Zero+popups.+Zero+friction.+Pure+speed." alt="Typing SVG"/>

<br/><br/>

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d1117"/>
<img src="https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white&labelColor=0d1117"/>
<img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white&labelColor=0d1117"/>
<img src="https://img.shields.io/badge/Platform-Web%20Browser-00fff7?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0d1117"/>

<br/>

<img src="https://img.shields.io/badge/Status-🔥%20ACTIVE-ffe500?style=for-the-badge&labelColor=0d1117"/>
<img src="https://img.shields.io/badge/Made%20with-💜%20by%20PI-ff00c8?style=for-the-badge&labelColor=0d1117"/>
<img src="https://img.shields.io/github/stars/piyushladukar/QR_SCANNER?style=for-the-badge&logo=github&labelColor=0d1117&color=00fff7"/>

</div>

---

## ⚡ WHAT IS QR\_SCANNER?

> 🔥 **QR\_SCANNER** is a lightning-fast, **web-based** QR decoder powered by **Flask + OpenCV**. No clunky desktop installs — just spin up the server, open your browser, and scan. Point your webcam. Upload an image. Drag-and-drop. Results appear **instantly on the page**. No popups. No cloud. 100% local. Pure speed.

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   📷  CAMERA SCAN    →  Real-time webcam QR decode via browser           ║
║   🖼️  IMAGE UPLOAD   →  Any image format. Decoded under 1 second.        ║
║   🖱️  DRAG & DROP    →  Drop any image onto the page. Zero friction.     ║
║   🪟  IN-PAGE RESULT →  No popups. Results live right on the page.       ║
║   🌐  URL LAUNCH     →  Scanned a link? One click opens it.              ║
║   📋  COPY TO CLIP   →  Copy decoded content instantly.                  ║
║   🎨  CLEAN UI       →  Glass-style web interface. Looks insane.         ║
║   ⚡  ZERO FRICTION  →  Local Flask server. No accounts. No cloud.       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🛠️ THE ARSENAL

<div align="center">
<img src="https://skillicons.dev/icons?i=python,flask,opencv,html,css,js&theme=dark&perline=6"/>
</div>

<br/>

```bash
╔══════════════════════════════════════════════════════════════════╗
║                    ⚙️  TECH STACK  ⚙️                            ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  🐍  Python     3.10+   →  Core language                         ║
║  🌐  Flask      3.x     →  Web server & routing                  ║
║  📸  OpenCV     4.x     →  Camera feed + image processing        ║
║  📦  pyzbar     0.1.x   →  QR & Barcode decoding engine          ║
║  🖼️  Pillow     10.x    →  Image format handling                 ║
║  🎨  HTML/CSS/JS        →  Frontend interface                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🗂️ PROJECT STRUCTURE

```
QR_SCANNER/
│
├── 📄  app.py                   ←  Flask entry point — run this
│
├── 🔍  scanner/
│   ├── camera_scanner.py        ←  Live camera QR decode logic
│   └── image_scanner.py         ←  File / image QR decode logic
│
├── 🎨  templates/
│   └── index.html               ←  Main web UI
│
├── 🖼️  static/
│   ├── css/style.css            ←  Styling
│   └── js/main.js               ←  Frontend logic
│
└── 📦  requirements.txt         ←  All dependencies
```

---

## 🚀 60 SECONDS TO LAUNCH

### `STEP 1` — Clone
```bash
git clone https://github.com/piyushladukar/QR_SCANNER.git
cd QR_SCANNER
```

### `STEP 2` — Virtual Environment
```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Linux / Mac
source venv/bin/activate
```

### `STEP 3` — Install
```bash
pip install flask opencv-python pyzbar pillow
```

### `STEP 4` — 🔥 Launch
```bash
python app.py
```

### `STEP 5` — Open Browser
```
http://127.0.0.1:5000
```
> You're live. Go scan something. ⚡

---

## 🎮 HOW TO USE

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. 🟢  python app.py           →  Start Flask server  │
│  2. 🌐  Open browser            →  localhost:5000       │
│  3. 📷  Pick your mode          →  Camera / Upload / DnD│
│  4. 🔍  Scan your QR            →  URL, text, wifi, etc │
│  5. 👀  See result instantly    →  On page, no popups!  │
│  6. 🌐  Open URL or 📋 Copy     →  One click each       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🗺️ ROADMAP

```
SHIPPED ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
- [x] 📷 Live camera QR scanning via browser
- [x] 🖼️ Image upload & decoding
- [x] 🖱️ Drag & Drop image support
- [x] 🪟 In-page result display (zero popups)
- [x] 📋 One-click clipboard copy
- [x] 🌐 One-click URL open

```
INCOMING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
- [ ] 🌙 Dark / Light mode toggle
- [ ] 📊 Scan history log with timestamps
- [ ] 🔊 Audio feedback on successful scan
- [ ] 📱 Multi-QR detection in a single frame
- [ ] 🔧 Built-in QR code generator

---

## 👨‍💻 BUILT BY

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-piyushladukar-181717?style=for-the-badge&logo=github&logoColor=white&labelColor=0d1117)](https://github.com/piyushladukar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=0d1117)](https://linkedin.com/in/piyushladukar)

<br/>

**PIYUSH LADUKAR** — Python & Flask Dev

> *"Built this because every QR scanner I found was either ugly, bloated,*
> *or made you install 47 dependencies for a desktop app.*
> *Flask. Browser. Done."*
>
> **— PI ⚡**

<br/>

<img src="https://github-readme-stats.vercel.app/api?username=piyushladukar&show_icons=true&theme=chartreuse-dark&hide_border=true&bg_color=0d1117&title_color=00fff7&icon_color=ff00c8&text_color=ffffff" height="160"/>
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=piyushladukar&layout=compact&theme=chartreuse-dark&hide_border=true&bg_color=0d1117&title_color=00fff7&text_color=ffffff" height="160"/>

<br/><br/>

<img src="https://streak-stats.demolab.com?user=piyushladukar&theme=neon-dark&hide_border=true&background=0d1117&ring=00fff7&fire=ff00c8&currStreakLabel=ffe500&sideLabels=00fff7" width="55%"/>

<br/><br/>


</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ffe500,50:ff00c8,100:00fff7&height=110&section=footer&text=⭐%20Star%20if%20it%20helped!&fontSize=20&fontColor=ffffff&fontAlignY=65&animation=twinkling" width="100%"/>

```
[ QR_SCANNER · Flask Edition · Built by Piyush Ladukar ]
[ SYSTEM ONLINE · ALL MODULES ACTIVE · READY TO SCAN ⚡ ]
```

</div>
