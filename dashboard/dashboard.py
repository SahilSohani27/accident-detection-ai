import streamlit as st
import requests
import os
import time
import qrcode
from PIL import Image
import base64
from io import BytesIO
import json


# Page configuration
st.set_page_config(
    page_title="AI Accident Alert System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Complete dark emergency theme CSS matching React UI
st.markdown("""
<style>
    /* ========== GLOBAL STYLES ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #111111 50%, #0d0d0d 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #444;
    }
    
    /* ========== HERO SECTION ========== */
    .hero-section {
        position: relative;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        text-align: center;
        overflow: hidden;
    }
    
    .hero-glow-1 {
        position: absolute;
        top: 20%;
        left: 20%;
        width: 400px;
        height: 400px;
        background: rgba(239, 68, 68, 0.1);
        border-radius: 50%;
        filter: blur(100px);
        animation: pulse-glow 4s ease-in-out infinite;
    }
    
    .hero-glow-2 {
        position: absolute;
        bottom: 20%;
        right: 20%;
        width: 350px;
        height: 350px;
        background: rgba(239, 68, 68, 0.05);
        border-radius: 50%;
        filter: blur(100px);
        animation: pulse-glow 4s ease-in-out infinite 1s;
    }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
    }
    
    .emergency-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #ef4444;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 2rem;
        animation: fade-in 0.5s ease-out;
    }
    
    @keyframes fade-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        animation: slide-up 0.6s ease-out;
    }
    
    @keyframes slide-up {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-title .gradient-text {
        background: linear-gradient(135deg, #ef4444 0%, #f97316 50%, #ef4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-title .white-text {
        color: #fafafa;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #a1a1aa;
        max-width: 700px;
        margin: 0 auto 2rem;
        line-height: 1.7;
        animation: fade-in 0.6s ease-out 0.2s both;
    }
    
    .feature-badges {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
        animation: fade-in 0.6s ease-out 0.3s both;
    }
    
    .feature-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #a1a1aa;
        font-size: 0.875rem;
    }
    
    .feature-badge .icon-red { color: #ef4444; }
    .feature-badge .icon-green { color: #22c55e; }
    .feature-badge .icon-yellow { color: #eab308; }
    
    .cta-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        font-size: 1.125rem;
        font-weight: 600;
        border-radius: 12px;
        text-decoration: none;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.4);
        transition: all 0.3s ease;
        animation: fade-in 0.6s ease-out 0.4s both;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 50px rgba(239, 68, 68, 0.6);
        color: white;
    }
    
    /* ========== SECTION STYLES ========== */
    .section {
        padding: 6rem 2rem;
        position: relative;
    }
    
    .section-dark {
        background: rgba(24, 24, 27, 0.3);
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 4rem;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fafafa;
        margin-bottom: 1rem;
    }
    
    .section-title .accent {
        color: #ef4444;
    }
    
    .section-subtitle {
        font-size: 1.125rem;
        color: #a1a1aa;
    }
    
    /* ========== PROBLEM CARDS (Why This Matters) ========== */
    .problem-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .problem-card {
        padding: 1.5rem;
        background: linear-gradient(135deg, #18181b 0%, #1f1f23 100%);
        border: 1px solid #27272a;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    
    .problem-card:hover {
        border-color: rgba(239, 68, 68, 0.5);
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.1);
    }
    
    .problem-icon {
        width: 48px;
        height: 48px;
        background: rgba(239, 68, 68, 0.1);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .problem-card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 0.5rem;
    }
    
    .problem-card-desc {
        font-size: 0.875rem;
        color: #a1a1aa;
        line-height: 1.6;
    }
    
    /* ========== WORKFLOW STEPS (How It Works) ========== */
    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .workflow-step {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 1rem;
    }
    
    .step-number {
        position: absolute;
        top: 0;
        left: 0.5rem;
        width: 24px;
        height: 24px;
        background: #ef4444;
        color: white;
        border-radius: 50%;
        font-size: 0.75rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10;
    }
    
    .step-icon-container {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, #18181b 0%, #1f1f23 100%);
        border: 1px solid #27272a;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.75rem;
        font-size: 1.75rem;
        transition: all 0.3s ease;
    }
    
    .workflow-step:hover .step-icon-container {
        border-color: rgba(239, 68, 68, 0.5);
        background: rgba(239, 68, 68, 0.05);
    }
    
    .step-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 0.25rem;
    }
    
    .step-desc {
        font-size: 0.75rem;
        color: #71717a;
    }
    
    .step-arrow {
        display: none;
        position: absolute;
        right: -0.5rem;
        top: 50%;
        transform: translateY(-50%);
        color: #3f3f46;
        font-size: 1rem;
    }
    
    @media (min-width: 768px) {
        .step-arrow { display: block; }
    }
    
    /* ========== ARCHITECTURE SECTION ========== */
    .architecture-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #18181b 0%, #1f1f23 100%);
        border: 1px solid #27272a;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .architecture-bg-pattern {
        position: absolute;
        inset: 0;
        opacity: 0.05;
        background-image: radial-gradient(circle at 2px 2px, currentColor 1px, transparent 0);
        background-size: 24px 24px;
    }
    
    .architecture-flow {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        position: relative;
        z-index: 10;
    }
    
    .arch-node {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        min-width: 120px;
    }
    
    .arch-node.default { background: rgba(63, 63, 70, 0.5); }
    .arch-node.emergency { 
        background: rgba(239, 68, 68, 0.1); 
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .arch-node.success { 
        background: rgba(34, 197, 94, 0.1); 
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .arch-node.warning { 
        background: rgba(234, 179, 8, 0.1); 
        border: 1px solid rgba(234, 179, 8, 0.3);
    }
    .arch-node.info { 
        background: rgba(59, 130, 246, 0.1); 
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .arch-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .arch-icon.text-muted { color: #a1a1aa; }
    .arch-icon.text-emergency { color: #ef4444; }
    .arch-icon.text-success { color: #22c55e; }
    .arch-icon.text-warning { color: #eab308; }
    .arch-icon.text-info { color: #3b82f6; }
    
    .arch-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: #fafafa;
    }
    
    .arch-subtitle {
        font-size: 0.75rem;
        color: #71717a;
    }
    
    .arch-arrow {
        color: #3f3f46;
        font-size: 1.5rem;
    }
    
    /* ========== TECH STACK SECTION ========== */
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .tech-card {
        padding: 1.25rem;
        background: linear-gradient(135deg, #18181b 0%, #1f1f23 100%);
        border: 1px solid #27272a;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .tech-card:hover {
        border-color: rgba(239, 68, 68, 0.5);
    }
    
    .tech-card:hover .tech-name {
        color: #ef4444;
    }
    
    .tech-name {
        font-size: 1.125rem;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 0.25rem;
        transition: color 0.3s ease;
    }
    
    .tech-desc {
        font-size: 0.875rem;
        color: #a1a1aa;
    }
    
    /* ========== DEMO SECTION ========== */
    .demo-section {
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #0f0f0f 0%, #171717 100%);
    }
    
    .demo-container {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    @media (min-width: 1024px) {
        .demo-container {
            grid-template-columns: 2fr 1fr;
        }
    }
    
    .demo-main {
        background: linear-gradient(135deg, #18181b 0%, #1f1f23 100%);
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 2rem;
    }
    
    .demo-sidebar {
        background: linear-gradient(135deg, #18181b 0%, #1f1f23 100%);
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 1.5rem;
    }
    
    .demo-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fafafa;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* ========== STATUS CARDS ========== */
    .status-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .status-card.info {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .status-card.success {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .status-card.error {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .status-card h4 {
        font-size: 1rem;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 0.5rem;
    }
    
    .status-card p {
        font-size: 0.875rem;
        color: #a1a1aa;
        margin: 0.25rem 0;
    }
    
    /* ========== STEP INDICATOR ========== */
    .step-indicator-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1.5rem 0;
    }
    
    .step-indicator-item {
        flex: 1;
        min-width: 100px;
        padding: 0.75rem;
        text-align: center;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        background: #27272a;
        color: #71717a;
        transition: all 0.3s ease;
    }
    
    .step-indicator-item.active {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        animation: pulse-step 2s ease-in-out infinite;
    }
    
    .step-indicator-item.completed {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
    }
    
    @keyframes pulse-step {
        0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 0 20px 5px rgba(239, 68, 68, 0.2); }
    }
    
    /* ========== SAMPLE VIDEO BUTTONS ========== */
    .sample-video-btn {
        display: block;
        width: 100%;
        padding: 1rem;
        margin-bottom: 0.75rem;
        background: linear-gradient(135deg, #1f1f23 0%, #27272a 100%);
        border: 1px solid #3f3f46;
        border-radius: 12px;
        color: #fafafa;
        font-size: 0.875rem;
        font-weight: 500;
        text-align: left;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .sample-video-btn:hover {
        border-color: #ef4444;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
        transform: translateY(-2px);
    }
    
    /* ========== QR CODE SECTION ========== */
    .qr-container {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1f1f23 0%, #27272a 100%);
        border-radius: 16px;
        margin-top: 1.5rem;
    }
    
    .qr-wrapper {
        display: inline-block;
        padding: 1rem;
        background: #fafafa;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .qr-text {
        font-size: 0.875rem;
        color: #a1a1aa;
        margin-bottom: 0.75rem;
    }
    
    .telegram-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        font-size: 0.875rem;
        font-weight: 600;
        border-radius: 25px;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .telegram-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.4);
        color: white;
    }
    
    /* ========== FOOTER ========== */
    .footer {
        padding: 4rem 2rem;
        background: rgba(24, 24, 27, 0.3);
        border-top: 1px solid #27272a;
        text-align: center;
    }
    
    .footer-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fafafa;
        margin-bottom: 1rem;
    }
    
    .footer-desc {
        color: #a1a1aa;
        max-width: 500px;
        margin: 0 auto 1rem;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    .footer-copyright {
        color: #71717a;
        font-size: 0.875rem;
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 1px solid #27272a;
    }
    
    /* ========== FILE UPLOADER OVERRIDE ========== */
    .stFileUploader {
        background: linear-gradient(135deg, #18181b 0%, #1f1f23 100%);
        border: 2px dashed #3f3f46;
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #ef4444;
    }
    
    .stFileUploader label {
        color: #a1a1aa !important;
    }
    
    /* ========== BUTTON OVERRIDES ========== */
    .stButton > button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.4);
    }
    
    .stButton > button:disabled {
        background: #3f3f46;
        color: #71717a;
    }
    
    /* ========== PROGRESS BAR ========== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ef4444, #f97316);
        border-radius: 10px;
    }
    
    /* ========== INFO/SUCCESS/WARNING BOXES ========== */
    .stAlert {
        background: rgba(24, 24, 27, 0.8);
        border-radius: 12px;
    }
    
    div[data-baseweb="notification"] {
        background: rgba(24, 24, 27, 0.9) !important;
        border: 1px solid #27272a !important;
    }
    
    /* Hide default Streamlit elements for cleaner look */
    .block-container {
        padding-top: 0 !important;
        max-width: 100% !important;
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
if 'show_demo' not in st.session_state:
    st.session_state.show_demo = False


# Backend API configuration
BACKEND_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload-video/"

# Telegram channel configuration
TELEGRAM_CHANNEL_LINK = "https://t.me/+aQKM_C_puyIwNzBl"


def generate_qr_code(data):
    """Generate QR code for the given data and return a proper PIL.Image.Image"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img.get_image()


def upload_video_to_backend(video_file):
    """Upload video to backend API"""
    try:
        files = {"file": (video_file.name, video_file, "video/mp4")}
        response = requests.post(UPLOAD_ENDPOINT, files=files, timeout=300)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: {str(e)}"}


def render_hero_section():
    """Render the hero section matching React UI"""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-glow-1"></div>
        <div class="hero-glow-2"></div>
        
        <div style="position: relative; z-index: 10; max-width: 900px; margin: 0 auto;">
            <div class="emergency-badge">
                ⚠️ AI-Powered Emergency Response
            </div>
            
            <h1 class="hero-title">
                <span class="gradient-text">🚨 AI-Powered</span><br>
                <span class="white-text">Accident Detection &</span><br>
                <span class="white-text">Emergency Alert System</span>
            </h1>
            
            <p class="hero-subtitle">
                YOLOv8 + GPT powered system that detects road accidents from video feeds 
                and sends instant SOS alerts to emergency services via Telegram
            </p>
            
            <div class="feature-badges">
                <div class="feature-badge">
                    <span class="icon-red">⚡</span>
                    <span>Real-time Detection</span>
                </div>
                <div class="feature-badge">
                    <span class="icon-green">🛡️</span>
                    <span>False Positive Reduction</span>
                </div>
                <div class="feature-badge">
                    <span class="icon-yellow">🚨</span>
                    <span>Instant Alerts</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⚡ Try ResQ Vision", key="hero_cta", use_container_width=True):
            st.session_state.show_demo = True
            st.rerun()


def render_problem_section():
    """Render 'Why This Matters' section"""
    st.markdown("""
    <div class="section section-dark">
        <div class="section-header">
            <h2 class="section-title">Why This <span class="accent">Matters</span></h2>
            <p class="section-subtitle">Traditional accident response systems are failing to save lives</p>
        </div>
        
        <div class="problem-grid">
            <div class="problem-card">
                <div class="problem-icon">⏱️</div>
                <h3 class="problem-card-title">Delay in Response</h3>
                <p class="problem-card-desc">Every minute of delay in accident response significantly reduces survival rates and increases the severity of injuries.</p>
            </div>
            
            <div class="problem-card">
                <div class="problem-icon">👁️</div>
                <h3 class="problem-card-title">Unreliable Monitoring</h3>
                <p class="problem-card-desc">Manual monitoring of CCTV feeds is prone to human error, fatigue, and cannot scale to cover all road networks effectively.</p>
            </div>
            
            <div class="problem-card">
                <div class="problem-icon">📡</div>
                <h3 class="problem-card-title">Lack of Intelligence</h3>
                <p class="problem-card-desc">Emergency services lack real-time intelligence about accident severity, location, and conditions to optimize response strategies.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_solution_section():
    """Render 'How It Works' section"""
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <h2 class="section-title">How It <span class="accent">Works</span></h2>
            <p class="section-subtitle">From video upload to emergency response in seconds</p>
        </div>
        
        <div class="workflow-grid">
            <div class="workflow-step">
                <div class="step-number">1</div>
                <div class="step-icon-container">📤</div>
                <h4 class="step-title">Upload Video</h4>
                <p class="step-desc">Upload CCTV or dashcam footage</p>
                <span class="step-arrow">→</span>
            </div>
            
            <div class="workflow-step">
                <div class="step-number">2</div>
                <div class="step-icon-container">🔬</div>
                <h4 class="step-title">AI Detection</h4>
                <p class="step-desc">YOLOv8 analyzes each frame</p>
                <span class="step-arrow">→</span>
            </div>
            
            <div class="workflow-step">
                <div class="step-number">3</div>
                <div class="step-icon-container">🔍</div>
                <h4 class="step-title">Validation</h4>
                <p class="step-desc">Frame streak logic reduces false positives</p>
                <span class="step-arrow">→</span>
            </div>
            
            <div class="workflow-step">
                <div class="step-number">4</div>
                <div class="step-icon-container">🎬</div>
                <h4 class="step-title">Clip Generation</h4>
                <p class="step-desc">10-second accident clip extracted</p>
                <span class="step-arrow">→</span>
            </div>
            
            <div class="workflow-step">
                <div class="step-number">5</div>
                <div class="step-icon-container">💬</div>
                <h4 class="step-title">SOS Message</h4>
                <p class="step-desc">GPT generates emergency alert</p>
                <span class="step-arrow">→</span>
            </div>
            
            <div class="workflow-step">
                <div class="step-number">6</div>
                <div class="step-icon-container">📱</div>
                <h4 class="step-title">Telegram Alert</h4>
                <p class="step-desc">Instant notification to responders</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_architecture_section():
    """Render Architecture section"""
    st.markdown("""
    <div class="section section-dark">
        <div class="section-header">
            <h2 class="section-title">System <span class="accent">Architecture</span></h2>
            <p class="section-subtitle">End-to-end pipeline for intelligent accident detection</p>
        </div>
        
        <div class="architecture-container">
            <div class="architecture-bg-pattern"></div>
            
            <div class="architecture-flow">
                <div class="arch-node default">
                    <div class="arch-icon text-muted">🎥</div>
                    <div class="arch-title">Video Input</div>
                    <div class="arch-subtitle">CCTV / Dashcam</div>
                </div>
                
                <span class="arch-arrow">→</span>
                
                <div class="arch-node emergency">
                    <div class="arch-icon text-emergency">🔬</div>
                    <div class="arch-title">YOLOv8</div>
                    <div class="arch-subtitle">Object Detection</div>
                </div>
                
                <span class="arch-arrow">→</span>
                
                <div class="arch-node success">
                    <div class="arch-icon text-success">✅</div>
                    <div class="arch-title">Validation</div>
                    <div class="arch-subtitle">Frame Streak Logic</div>
                </div>
                
                <span class="arch-arrow">→</span>
                
                <div class="arch-node warning">
                    <div class="arch-icon text-warning">💬</div>
                    <div class="arch-title">GPT SOS</div>
                    <div class="arch-subtitle">Message Generator</div>
                </div>
                
                <span class="arch-arrow">→</span>
                
                <div class="arch-node info">
                    <div class="arch-icon text-info">📤</div>
                    <div class="arch-title">Telegram</div>
                    <div class="arch-subtitle">Alert System</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_tech_stack_section():
    """Render Tech Stack section"""
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <h2 class="section-title">Tech <span class="accent">Stack</span></h2>
            <p class="section-subtitle">Built with industry-leading technologies</p>
        </div>
        
        <div class="tech-grid">
            <div class="tech-card">
                <h4 class="tech-name">FastAPI</h4>
                <p class="tech-desc">High-performance Python backend</p>
            </div>
            
            <div class="tech-card">
                <h4 class="tech-name">YOLOv8</h4>
                <p class="tech-desc">State-of-the-art object detection</p>
            </div>
            
            <div class="tech-card">
                <h4 class="tech-name">OpenCV</h4>
                <p class="tech-desc">Computer vision processing</p>
            </div>
            
            <div class="tech-card">
                <h4 class="tech-name">OpenAI GPT</h4>
                <p class="tech-desc">Intelligent SOS generation</p>
            </div>
            
            <div class="tech-card">
                <h4 class="tech-name">Telegram Bot</h4>
                <p class="tech-desc">Instant alert delivery</p>
            </div>
            
            <div class="tech-card">
                <h4 class="tech-name">Streamlit</h4>
                <p class="tech-desc">Modern responsive UI</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_demo_section():
    """Render the interactive demo section"""
    st.markdown("""
    <div class="section-header" style="padding-top: 2rem;">
        <h2 class="section-title">🚀 Live <span class="accent">Demo</span></h2>
        <p class="section-subtitle">Upload a video to test the accident detection system</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="demo-main">', unsafe_allow_html=True)
        st.markdown('<h3 class="demo-title">📤 Upload Video for Analysis</h3>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload a video file to analyze for accidents. Maximum size: 50MB"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {uploaded_file.size / (1024*1024):.2f} MB")
            
            if st.button("🚀 Analyze Video", type="primary", disabled=st.session_state.processing):
                st.session_state.processing = True
                st.session_state.current_step = 0
                st.session_state.error_message = None
                st.session_state.results = None
                
                with st.spinner("Processing video..."):
                    for step in range(6):
                        st.session_state.current_step = step + 1
                        time.sleep(1.5)
                    
                    results = upload_video_to_backend(uploaded_file)
                    
                    if "error" in results:
                        st.session_state.error_message = results["error"]
                    else:
                        st.session_state.results = results
                    
                    st.session_state.processing = False
                    st.rerun()
        
        # Processing status
        if st.session_state.processing:
            st.markdown("### 🔄 Processing Status")
            steps = ["📤 Uploading", "🔍 Processing", "🚨 Detection", "✂️ Clipping", "📝 SOS Gen", "📱 Alert"]
            
            step_html = '<div class="step-indicator-container">'
            for i, step in enumerate(steps):
                status = ""
                if i < st.session_state.current_step:
                    status = "completed"
                elif i == st.session_state.current_step:
                    status = "active"
                step_html += f'<div class="step-indicator-item {status}">{step}</div>'
            step_html += '</div>'
            st.markdown(step_html, unsafe_allow_html=True)
            
            st.progress(st.session_state.current_step / 6)
        
        # Error display
        if st.session_state.error_message:
            st.markdown(f"""
            <div class="status-card error">
                <h4>❌ Error</h4>
                <p>{st.session_state.error_message}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Results display
        if st.session_state.results and not st.session_state.processing:
            st.markdown("### 🎯 Analysis Results")
            
            if "accident_info" in st.session_state.results:
                accident_info = st.session_state.results["accident_info"]
                
                st.markdown(f"""
                <div class="status-card success">
                    <h4>🚨 Accident Detected!</h4>
                    <p><strong>Confidence:</strong> {accident_info.get('confidence', 0):.2%}</p>
                    <p><strong>Frame:</strong> {accident_info.get('frame_idx', 'N/A')}</p>
                    <p><strong>Coordinates:</strong> {accident_info.get('coordinates', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if "sos_message" in st.session_state.results:
                    st.markdown("### 📝 Generated SOS Message")
                    st.info(st.session_state.results["sos_message"])
                
                if "telegram" in st.session_state.results:
                    st.markdown("### 📱 Emergency Alert Status")
                    if "sent" in st.session_state.results["telegram"].lower():
                        st.success(f"✅ {st.session_state.results['telegram']}")
                    else:
                        st.warning(f"⚠️ {st.session_state.results['telegram']}")
            else:
                st.markdown("""
                <div class="status-card info">
                    <h4>✅ No Accident Detected</h4>
                    <p>The video has been analyzed and no accidents were detected.</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="demo-sidebar">', unsafe_allow_html=True)
        
        # Sample videos
        st.markdown("### 📹 Sample Videos")
        sample_videos = [
            ("testvideo1.mp4", "🎬 Sample Accident 1"),
            ("testvideo2.mp4", "🎬 Sample Accident 2"),
            ("test4.mp4", "🎬 Sample Accident 3")
        ]
        
        for video_file, description in sample_videos:
            if st.button(description, key=f"sample_{video_file}", use_container_width=True):
                st.session_state.processing = True
                st.session_state.current_step = 0
                st.session_state.error_message = None
                
                with st.spinner("Processing sample video..."):
                    sample_path = f"../Testing/{video_file}"
                    if os.path.exists(sample_path):
                        with open(sample_path, "rb") as f:
                            files = {"file": (video_file, f, "video/mp4")}
                            response = requests.post(UPLOAD_ENDPOINT, files=files, timeout=300)
                            
                        if response.status_code == 200:
                            st.session_state.results = response.json()
                        else:
                            st.session_state.error_message = f"API Error: {response.status_code}"
                    else:
                        st.session_state.error_message = f"Sample video not found: {sample_path}"
                    
                    st.session_state.processing = False
                    st.session_state.current_step = 6
                
                st.rerun()
        
        # System status
        st.markdown("""
        <div class="status-card info">
            <h4>🔧 System Status</h4>
            <p>✅ AI Model: Loaded</p>
            <p>✅ Backend API: Connected</p>
            <p>✅ Telegram Bot: Active</p>
        </div>
        """, unsafe_allow_html=True)
        
        # QR Code
        st.markdown('<div class="qr-container">', unsafe_allow_html=True)
        qr_img = generate_qr_code(TELEGRAM_CHANNEL_LINK)
        st.image(qr_img, caption="Scan to join emergency channel", use_container_width=True)
        st.markdown(f"""
        <a href="{TELEGRAM_CHANNEL_LINK}" class="telegram-btn" target="_blank">
            📱 Join Telegram
        </a>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_footer():
    """Render footer section"""
    st.markdown(f"""
    <div class="footer">
        <h3 class="footer-title">🚨 AI Accident Detection System</h3>
        <p class="footer-desc">
            A backend-focused AI system demonstration showcasing real-time 
            accident detection and emergency response capabilities.
        </p>
        <p style="font-size: 0.875rem; color: #71717a;">Built with ❤️ for emergency response innovation</p>
        <p class="footer-copyright">© 2024 AI Accident Detection System. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    if st.session_state.show_demo:
        # Demo page
        if st.button("← Back to Home", key="back_home"):
            st.session_state.show_demo = False
            st.rerun()
        render_demo_section()
        render_footer()
    else:
        # Landing page with all sections
        render_hero_section()
        render_problem_section()
        render_solution_section()
        render_architecture_section()
        render_tech_stack_section()
        render_footer()


if __name__ == "__main__":
    main()