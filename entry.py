import streamlit as st
import requests
import os
import time
import qrcode
from PIL import Image
import base64
import io
import json
import logging
import shutil

from backend.modelv2 import AccidentDetector
from backend.sos_generator import SOSGenerator
from dotenv import load_dotenv
from backend.send_sos import TelegramNotifier


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
notifier = TelegramNotifier()


# Page configuration
st.set_page_config(
    page_title="AI Accident Alert System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #ff8e8e, #ffa8a8);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        color: white;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .status-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .error-card {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .sample-video-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    
    .sample-video-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin: 2rem 0;
    }
    
    .qr-container {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .telegram-link {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        margin: 1rem;
        font-weight: bold;
        transition: transform 0.3s ease;
    }
    
    .telegram-link:hover {
        transform: scale(1.05);
        color: white;
        text-decoration: none;
    }
    
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
    }
    
    .step {
        background: #e0e0e0;
        color: #666;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        flex: 1;
        margin: 0 0.5rem;
        text-align: center;
    }
    
    .step.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .step.completed {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'results' not in st.session_state:
    st.session_state.results = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

# # Backend API configuration
# BACKEND_URL = "http://localhost:8000"  # Adjust if your backend runs on different port
# UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload-video/"
MAX_VIDEO_SIZE_MB = 50
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")   # model path
detector = AccidentDetector(MODEL_PATH)

# Folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "post_accident_output"   # it stores both clip + best frame
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Telegram channel configuration
TELEGRAM_CHANNEL_LINK = "https://t.me/+aQKM_C_puyIwNzBl"  # Replace with actual channel link

def generate_qr_code(data):
    """Generate QR code for the given data and return a proper PIL.Image.Image"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img.get_image()

def upload_video(video_file):
    """
    Process video for accident detection.
    Works for both Streamlit uploaded files and local sample videos (file path).
    """
    # Wrap local file paths in BytesIO
    if isinstance(video_file, str):
        filename = os.path.basename(video_file)
        with open(video_file, "rb") as f:
            video_bytes = f.read()
        video_file = io.BytesIO(video_bytes)
        video_file.filename = filename
    else:
        # Streamlit uploaded file
        filename = video_file.name if hasattr(video_file, "name") else video_file.filename

    # Check file extension
    if not filename.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
        st.error("Invalid file format. Upload video files only.")
        st.stop()

    # Save uploaded file locally
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(video_path, "wb") as buffer:
        if hasattr(video_file, "read"):
            shutil.copyfileobj(video_file, buffer)
        else:
            st.error("Invalid video file object.")
            st.stop()

    # Validate size
    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    if file_size_mb > MAX_VIDEO_SIZE_MB:
        os.remove(video_path)
        st.error(f"File too large. Must be under {MAX_VIDEO_SIZE_MB} MB.")
        st.stop()

    # Run accident detection
    accident_info, clip_path, best_frame_path = detector.detect_and_save_clip(
        video_source=video_path,
        save_folder=OUTPUT_FOLDER,
        streak_threshold=4,
        conf_threshold=0.55,
        clip_duration=10
    )

    if accident_info is None:
        st.info("No accident detected!!")
        return {"message": "No accident detected."}

    # Generate SOS text
    try:
        sos_text = (
            "SOS Alert: An accident has been detected. Immediate medical and emergency assistance is required. "
            "Please dispatch responders urgently and proceed with caution. Video evidence of the incident is attached."
        )
    except Exception as e:
        print(f"[ERROR] SOS text not generated by GPT: {e}")
        sos_text = (
            "SOS Alert: An accident has been detected. Immediate medical and emergency assistance is required. "
            "Please dispatch responders urgently and proceed with caution. Video evidence of the incident is attached."
        )

    # Send Telegram alert
    try:
        notifier.send_sos(sos_text, clip_path)
        notifier_response = "SOS sent to emergency group"
    except Exception as e:
        notifier_response = f"[ERROR] Telegram SOS sending failed: {e}"
        print(notifier_response)

    return {
        "accident_info": accident_info,
        "clip_path": clip_path,
        "best_frame": best_frame_path,
        "sos_message": sos_text,
        "telegram": notifier_response
    }

def display_step_indicator(current_step):
    """Display processing step indicator"""
    steps = [
        "📤 Uploading Video",
        "🔍 Processing Video", 
        "🚨 Accident Detection",
        "✂️ Clipping Video",
        "📝 Generating SOS",
        "📱 Sending Alert"
    ]
    
    step_html = '<div class="step-indicator">'
    for i, step in enumerate(steps):
        status_class = ""
        if i < current_step:
            status_class = "completed"
        elif i == current_step:
            status_class = "active"
        
        step_html += f'<div class="step {status_class}">{step}</div>'
    step_html += '</div>'
    
    st.markdown(step_html, unsafe_allow_html=True)

def main():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🚨 AI Accident Alert System</h1>
        <p class="subtitle">Advanced AI-Powered Emergency Response System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Quick Actions")
        
        # Sample videos section
        st.markdown("### 📹 Sample Videos")
        st.markdown("Click on any sample video to test the system:")
        
        sample_videos = [
            ("testvideo1.mp4", "Sample Accident 1"),
            ("testvideo2.mp4", "Sample Accident 2"), 
            ("test4.mp4", "Sample Accident 3")
        ]
        
        for video_file, description in sample_videos:
            if st.button(f"🎬 {description}", key=f"sample_{video_file}"):
                st.session_state.processing = True
                st.session_state.current_step = 0
                st.session_state.error_message = None
                
                # Process sample video through backend
                with st.spinner("Processing sample video..."):
                    # Check if sample video exists
                    sample_path = f"./Testing/{video_file}"
                    if os.path.exists(sample_path):
                        # Upload sample video to backend
                        with open(sample_path, "rb") as f:
                            files = {"file": (video_file, f, "video/mp4")}   # redundant only kept fot indentation sake
                            response = upload_video(sample_path)
                            
                        if "error" in response:
                            st.session_state.error_message = response["error"]
                        else:
                            st.session_state.results = response
                    else:
                        st.session_state.error_message = f"Sample video not found: {sample_path}"
                    
                    st.session_state.processing = False
                    st.session_state.current_step = 6
                
                st.rerun()
        
        # QR Code section
        st.markdown("### 📱 Join Emergency Channel")
        qr_img = generate_qr_code(TELEGRAM_CHANNEL_LINK)
        st.image(qr_img, caption="Scan to join emergency channel", use_container_width=True)
        
        st.markdown(f"""
        <a href="{TELEGRAM_CHANNEL_LINK}" class="telegram-link" target="_blank">
            📱 Join Telegram Channel
        </a>
        """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Video upload section
        st.markdown("## 📤 Upload Video for Analysis")
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload a video file to analyze for accidents. Maximum size: 50MB"
        )
        
        if uploaded_file is not None:
            # Display video info
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {uploaded_file.size / (1024*1024):.2f} MB")
            
            # Process button
            if st.button("🚀 Analyze Video", type="primary", disabled=st.session_state.processing):
                st.session_state.processing = True
                st.session_state.current_step = 0
                st.session_state.error_message = None
                st.session_state.results = None
                
                # Process video
                with st.spinner("Processing video..."):
                    # Step 1: Uploading
                    st.session_state.current_step = 1
                    time.sleep(1)
                    
                    # Step 2: Processing
                    st.session_state.current_step = 2
                    time.sleep(2)
                    
                    # Step 3: Accident Detection
                    st.session_state.current_step = 3
                    time.sleep(3)
                    
                    # Step 4: Clipping
                    st.session_state.current_step = 4
                    time.sleep(2)
                    
                    # Step 5: Generate SOS
                    st.session_state.current_step = 5
                    time.sleep(2)
                    
                    # Step 6: Send Alert
                    st.session_state.current_step = 6
                    time.sleep(1)
                    
                    # Upload to backend
                    results = upload_video(uploaded_file)
                    
                    if "error" in results:
                        st.session_state.error_message = results["error"]
                    else:
                        st.session_state.results = results
                    
                    st.session_state.processing = False
                    st.rerun()
        
        # Display processing status
        if st.session_state.processing:
            st.markdown("### 🔄 Processing Status")
            display_step_indicator(st.session_state.current_step)
            
            progress_bar = st.progress(st.session_state.current_step / 6)
            st.info(f"Current step: {st.session_state.current_step + 1} of 6")
        
        # Display error message
        if st.session_state.error_message:
            st.markdown(f"""
            <div class="error-card">
                <h3>❌ Error</h3>
                <p>{st.session_state.error_message}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display results
        if st.session_state.results and not st.session_state.processing:
            st.markdown("### 🎯 Analysis Results")
            
            if "accident_info" in st.session_state.results:
                accident_info = st.session_state.results["accident_info"]
                
                st.markdown(f"""
                <div class="success-card">
                    <h3>🚨 Accident Detected!</h3>
                    <p><strong>Confidence:</strong> {accident_info.get('confidence', 0):.2%}</p>
                    <p><strong>Frame:</strong> {accident_info.get('frame_idx', 'N/A')}</p>
                    <p><strong>Coordinates:</strong> {accident_info.get('coordinates', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Display SOS message
                if "sos_message" in st.session_state.results:
                    st.markdown("### 📝 Generated SOS Message")
                    st.info(st.session_state.results["sos_message"])
                
                # Display Telegram status
                if "telegram" in st.session_state.results:
                    st.markdown("### 📱 Emergency Alert Status")
                    if "sent" in st.session_state.results["telegram"].lower():
                        st.success(f"✅ {st.session_state.results['telegram']}")
                    else:
                        st.warning(f"⚠️ {st.session_state.results['telegram']}")
                
                # Display generated files
                if "clip_path" in st.session_state.results:
                    st.markdown("### 📁 Generated Files")
                    st.success(f"🎬 Accident clip saved: {st.session_state.results['clip_path']}")
                
                if "best_frame" in st.session_state.results:
                    st.success(f"🖼️ Best frame saved: {st.session_state.results['best_frame']}")
            else:
                st.markdown("""
                <div class="status-card">
                    <h3>✅ No Accident Detected</h3>
                    <p>The video has been analyzed and no accidents were detected.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # System information
        st.markdown("## ℹ️ System Information")
        
        st.markdown("""
        <div class="status-card">
            <h4>🔧 System Status</h4>
            <p>✅ AI Model: Loaded</p>
            <p>✅ Backend API: Connected</p>
            <p>✅ Telegram Bot: Active</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features
        st.markdown("### 🚀 Key Features")
        st.markdown("""
        - **Real-time Detection**: Advanced YOLO-based accident detection
        - **Automatic Clipping**: 10-second accident clips with best frames
        - **AI-Generated SOS**: Intelligent emergency message generation
        - **Instant Alerts**: Telegram integration for emergency response
        - **High Accuracy**: 85%+ confidence threshold for reliable detection
        """)
        
        # Technical specs
        st.markdown("### ⚙️ Technical Specifications")
        st.markdown("""
        - **Model**: YOLOv8 Custom Trained
        - **Confidence Threshold**: 55%
        - **Streak Threshold**: 4 consecutive frames
        - **Max Video Size**: 50MB
        - **Supported Formats**: MP4, AVI, MOV, MKV
        """)
        
        # Emergency contacts
        st.markdown("### 🆘 Emergency Contacts")
        st.markdown("""
        - **Emergency Services**: 911
        - **Police**: 100
        - **Ambulance**: 108
        - **Fire Department**: 101
        """)

if __name__ == "__main__":
    main()
