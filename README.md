# 🚦 ResQ-Vision

### AI-Powered Accident Detection and Emergency Response System

ResQ-Vision is a backend-centric, real-time accident detection and emergency alerting system designed to operate on live traffic surveillance feeds. It leverages deep learning–based video analysis to autonomously detect road accidents, validate them temporally to reduce false positives, and immediately trigger SOS alerts with visual evidence.

While the demo operates on uploaded video clips, the system is architected for continuous ingestion from live CCTV camera streams deployed across highways and urban road infrastructure.

---

## 🧠 System Overview

Modern road networks already deploy large-scale CCTV infrastructure, yet these feeds are largely used for passive monitoring or post-incident analysis. ResQ-Vision transforms this passive infrastructure into an active, intelligent first-responder system.

The platform continuously analyzes video streams, detects accident events using a trained YOLOv8 model, validates incidents across multiple consecutive frames, extracts visual evidence, and dispatches emergency alerts automatically without human intervention.

---

## 🏗️ Architecture

The system follows a clean separation of concerns between frontend presentation and backend orchestration.

### Backend

FastAPI-based service responsible for video ingestion, accident detection, evidence extraction, SOS generation, and alert dispatch.

### Frontend

ReactJS application styled with Tailwind CSS, providing an intuitive interface for uploading videos and visualizing detection results during demonstration and testing.

### Alerting Layer

Telegram Bot integration for instant delivery of SOS alerts along with accident video clips.

---

## ⚙️ Core Workflow

1. Video feed is ingested through the backend API
2. Each frame is processed using a YOLOv8 accident detection model
3. Accident detection is confirmed only if it persists across a defined number of consecutive frames
4. Upon confirmation, the system automatically extracts
   a short contextual video clip
   the most representative accident frame
5. Structured accident metadata is generated
6. An SOS alert is dispatched to emergency responders via Telegram
7. Processed outputs are exposed via static endpoints for frontend consumption

---

## 🛠️ Tech Stack

### Backend

FastAPI
Python
YOLOv8 (Ultralytics)
OpenCV
Python-dotenv

### Frontend

ReactJS
Vite
Tailwind CSS
TypeScript

### Alerts and Messaging

Telegram Bot API

---

## 📂 Project Structure

```
accident-detection-ai/
│
├── backend/
│   ├── main.py                  FastAPI entry point
│   ├── modelv2.py               YOLOv8 accident detection logic
│   ├── sos_generator.py         SOS message generation module
│   ├── send_sos.py              Telegram notification handler
│
├── frontend/
│   ├── src/                     React application source
│   ├── public/                  Static frontend assets
│   ├── tailwind.config.ts
│   ├── vite.config.ts
│
├── model/
│   └── best.pt                  Trained YOLOv8 accident detection model
│
├── uploads/                     Temporarily stored input videos
├── post_accident_output/        Generated clips and best frames
│
├── requirements.txt
├── package.json
└── README.md
```

---

## 🚀 Backend Setup and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/accident-detection-ai.git
cd accident-detection-ai
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux or macOS
venv\Scripts\activate           # Windows
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

### 5. Run FastAPI Server

```bash
uvicorn backend.main:app --reload
```

Swagger UI will be available at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🌐 Frontend Setup and Execution

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

Frontend will run on
[http://localhost:5173](http://localhost:5173)

---

## 📡 API Reference

### POST `/upload-video/`

Uploads a video file for accident detection.

**Input**
Supported formats mp4 avi mov mkv
Maximum size 50 MB

**Processing**
Runs accident detection with temporal validation
Extracts evidence upon detection
Triggers SOS alert

**Response**
Accident metadata
Clip and frame URLs
SOS message status
Telegram dispatch confirmation

---

## 🔔 Telegram Alerting

When an accident is confirmed, the system automatically sends an SOS alert containing
A concise emergency message
The extracted accident video clip

This ensures rapid situational awareness for emergency responders.

---

## 🌍 Real-World Deployment Vision

Although the current implementation accepts uploaded videos for demonstration, ResQ-Vision is designed to operate on continuous live CCTV streams. The backend orchestration layer can be directly connected to traffic cameras deployed on highways, intersections, and smart city infrastructure to enable real-time accident detection and response at scale.

---

## 🔮 Future Enhancements

Live RTSP and CCTV stream ingestion
Multi-camera accident correlation
Geo-tagged emergency alerts
Integration with government emergency response systems
Dashboard analytics for traffic authorities

---

## 👨‍💻 Contributors

Sahil Sohani
Dushyant Atalkar

---

## 📜 License

This project is licensed under the Apache 2.0 License.

---
