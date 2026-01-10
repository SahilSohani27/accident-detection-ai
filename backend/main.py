import os
import shutil
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from urllib3 import response
from modelv2 import AccidentDetector
from sos_generator import SOSGenerator
from dotenv import load_dotenv
from send_sos import TelegramNotifier


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI(title="AI Accident Detection MVP")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000", "http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

notifier = TelegramNotifier()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")   # model path
detector = AccidentDetector(MODEL_PATH)

# Folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "post_accident_output"   # it stores both clip + best frame
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Mount static files directory to serve output files
app.mount("/static", StaticFiles(directory=OUTPUT_FOLDER), name="static")

MAX_VIDEO_SIZE_MB = 50

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        logger.info(f"Received video upload request: {file.filename}")
        
        # Validating file extension
        if not file.filename.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            raise HTTPException(status_code=400, detail="Invalid file format. Upload video files only.")

        # Saving uploaded file
        video_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Video saved to: {video_path}")

        # Validating size
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        if file_size_mb > MAX_VIDEO_SIZE_MB:
            os.remove(video_path)
            raise HTTPException(status_code=400, detail=f"File too large. Must be under {MAX_VIDEO_SIZE_MB} MB.")

        logger.info(f"File size: {file_size_mb:.2f} MB - Starting accident detection...")

        # Running accident detection
        accident_info, clip_path, best_frame_path = detector.detect_and_save_clip(
            video_source=video_path,
            save_folder=OUTPUT_FOLDER,
            streak_threshold=4,
            conf_threshold=0.55,
            clip_duration=10
        )

        if accident_info is None:
            logger.info("No accident detected in video")
            return JSONResponse(content={"message": "No accident detected."})

        logger.info(f"Accident detected! Confidence: {accident_info.get('confidence', 'N/A')}")

        # Generate SOS message
        try:
            logger.info("Generating SOS message...")
            # sos_text = SOSGenerator().generate_sos(accident_info, best_frame_path)
            sos_text = (
                "SOS Alert: An accident has been detected. Immediate medical and emergency assistance is required. "
                "Please dispatch responders urgently and proceed with caution. Video evidence of the incident is attached."
            )
        except Exception as e:
            logger.error(f"SOS text generation failed: {e}")
            sos_text = (
                "SOS Alert: An accident has been detected. Immediate medical and emergency assistance is required. "
                "Please dispatch responders urgently and proceed with caution. Video evidence of the incident is attached."
            )

        # Send Telegram notification
        notifier_response = ""
        try:
            logger.info("Sending SOS to Telegram...")
            notifier.send_sos(sos_text, clip_path)
            notifier_response = "SOS sent to emergency group"
            logger.info("Telegram notification sent successfully")
        except Exception as e:
            notifier_response = f"[ERROR] Telegram SOS sending failed: {str(e)}"
            logger.error(notifier_response)

        # Convert file paths to URLs for frontend access
        clip_filename = os.path.basename(clip_path) if clip_path else None
        frame_filename = os.path.basename(best_frame_path) if best_frame_path else None
        
        clip_url = f"/static/{clip_filename}" if clip_filename else None
        frame_url = f"/static/{frame_filename}" if frame_filename else None

        response_data = {
            "accident_info": accident_info,
            "clip_path": clip_path,
            "clip_url": clip_url,
            "best_frame": best_frame_path,
            "frame_url": frame_url,
            "sos_message": sos_text,
            "telegram": notifier_response
        }

        logger.info("Video processing completed successfully")
        return JSONResponse(content=response_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
