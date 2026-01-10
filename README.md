# 🚦 AI Accident Detection System

An intelligent accident detection system powered by **YOLOv8s** and **OpenAI GPT** that analyzes CCTV/video footage to detect road accidents, reduce false positives, and automatically generate SOS alerts with evidence (video + image).  

This project is a backend-focused prototype, with a **Streamlit-based frontend** for demonstration, and supports integration with a **Telegram bot** for fast SOS notifications.

---

## 📌 Features
- 🎥 **Accident Detection from Video Clips** using YOLOv8s.  
- ✅ **False Positive Reduction** – accident confirmed only if detected in `N` consecutive frames.  
- 🖼️ **Automatic Clip & Frame Capture** – saves a 10s accident clip + the most confident accident frame.  
- 🧠 **SOS Message Generation** – uses OpenAI GPT with accident info + frame for descriptive emergency alerts.  
- 📲 **Telegram Bot Integration** – sends SOS message + accident video instantly.  
- 🌐 **Streamlit Frontend** – simple dashboard for uploading and testing video clips.  

---

## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) – REST API backend  
- [YOLOv8 (Ultralytics)](https://docs.ultralytics.com/) – accident detection model  
- [OpenCV](https://opencv.org/) – video processing  
- [OpenAI API (gpt-4o-mini)](https://platform.openai.com/) – SOS alert message generation  
- [Streamlit](https://streamlit.io/) – demo frontend  
- [Telegram Bot API](https://core.telegram.org/bots/api) – real-time SOS alerts  
- [Python-dotenv](https://pypi.org/project/python-dotenv/) – environment management  

---

## 📂 Project Structure

```
accident-detection-ai/
│── backend/
  │── main.py                    # FastAPI entrypoint
  │── modelv2.py                 # AccidentDetector (YOLOv8 logic)
  │── sos_generator.py           # OpenAI GPT SOS message generator
  │── send_sos.py                # Sends SOS message along with a 10 ec accident clip
│── uploads/                   # Uploaded video storage
  │── post_accident_output/      # Accident clips & best frames
│── requirements.txt           # Dependencies
│── .env                       # API keys and secrets
```

---

## ⚙️ How It Works

**Workflow:**
1. **Video Input** → Upload CCTV footage or video clip
2. **YOLOv8 Detection** → Analyze each frame for accidents
3. **Frame Validation** → Confirm accident if detected in ≥4 consecutive frames
4. **Evidence Capture** → Save 10-second clip + best accident frame
5. **SOS Generation** → Create emergency message using OpenAI GPT
6. **Alert System** → Send SOS + video via Telegram Bot
7. **Demo Interface** → View results through Streamlit UI## ⚙️ How It Works

---

## 🚀 Setup & Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/accident-detection-ai.git
cd accident-detection-ai
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 5️⃣ Run FastAPI Backend
```bash
uvicorn main:app --reload
```

API will be live at 👉 http://127.0.0.1:8000/docs

### 6️⃣ Run Streamlit Frontend
```bash
streamlit run app.py
```

---

## 📡 API Endpoints

### `POST /upload-video/`

Upload a video for accident detection.

**Request:**
- File upload (.mp4, .avi, .mov, .mkv)
- Max size: 50 MB

---

## 📲 Telegram Bot Integration

- Automatically sends the SOS message + 10s accident clip to a predefined Telegram group/channel.
- Requires setting up `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`.

---

## 🎯 Future Improvements

- Direct CCTV integration instead of local video files.
- Multi-camera accident detection & tracking.


---

## 👨‍💻 Contributors

- **Sahil Sohani**
- **Dushyant Atalkar**


---

## 📜 License

This project is licensed under the MIT License.




