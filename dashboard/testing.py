import os
import io
import requests
import streamlit as st
from PIL import Image
import qrcode

# -----------------------------
# CONFIG
# -----------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")  # backend FastAPI base url
UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload-video/"

# Sample videos in the testing/ folder (relative to where this Streamlit app runs)
SAMPLES = [
    {"title": "Sample 1 - Daylight", "path": "testing/video1.mp4"},
    {"title": "Sample 2 - Busy Road", "path": "testing/video2.mp4"},
    {"title": "Sample 3 - CCTV Night", "path": "testing/video3.mp4"},
]

TELEGRAM_INVITE = os.getenv("TELEGRAM_INVITE_LINK", "https://t.me/joinchat/xxxxxx")
PROJECT_NAME = "Accident Alert AI"

# -----------------------------
# Helpers
# -----------------------------

def make_qr(url: str) -> Image.Image:
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def post_video_file(video_path: str):
    """POST video file to backend /upload-video/ endpoint and stream results."""
    with open(video_path, "rb") as f:
        files = {"file": (os.path.basename(video_path), f, "video/mp4")}
        resp = requests.post(UPLOAD_ENDPOINT, files=files, timeout=120)
    return resp


# -----------------------------
# STREAMLIT UI
# -----------------------------

st.set_page_config(page_title=PROJECT_NAME, layout="wide", page_icon="🚨")

# Header
st.markdown(
    f"<div style='display:flex; align-items:center; gap:16px'>"
    f"<div style='font-size:28px; font-weight:800'>{PROJECT_NAME}</div>"
    f"<div style='color:#666; margin-left:12px; font-size:14px'>Hackathon MVP · Real-time accident detection & SOS</div>"
    f"</div>", unsafe_allow_html=True,
)
st.markdown("---")

# Layout: left column for upload & samples, right column for status & outputs
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload a video")
    st.write("Upload a short clip (≤50 MB) or click a sample to try the system.")

    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

    st.markdown("---")
    st.subheader("Sample videos")
    for sample in SAMPLES:
        st.markdown(f"**{sample['title']}**")
        # show a small video preview if available
        try:
            if os.path.exists(sample["path"]):
                st.video(sample["path"], start_time=0)
            else:
                st.info("Sample missing — place sample files in the testing/ folder with names video1/2/3.mp4")
        except Exception:
            pass

        if st.button(f"Run {sample['title']}", key=sample['title']):
            # write sample to a temp in-memory file so we can POST
            with st.spinner("Sending sample to backend..."):
                try:
                    resp = post_video_file(sample['path'])
                except Exception as e:
                    st.error(f"Failed to contact backend: {e}")
                    resp = None

            if resp is None:
                st.warning("No response from backend")
            else:
                if resp.status_code == 200:
                    st.success("Video processed — response received")
                else:
                    st.error(f"Backend returned {resp.status_code}: {resp.text}")

    st.markdown("---")
    st.markdown("#### Quick links")
    st.write("Join the Telegram group to receive live SOS alerts")
    st.write(f"[Join Telegram]({TELEGRAM_INVITE})")
    qr_img = make_qr(TELEGRAM_INVITE)
    st.image(qr_img, caption="Scan to join Telegram alerts", width=180)

with col2:
    st.subheader("Live processing & results")
    status_box = st.empty()
    status_box.info("Idle — upload a video or run a sample to begin.")

    output_container = st.container()

    def update_status(step_text: str, success: bool = True):
        if success:
            status_box.success(step_text)
        else:
            status_box.error(step_text)

    # If user uploaded a file, send it
    if uploaded_file is not None:
        tmp_path = os.path.join("uploads", uploaded_file.name)
        with open(tmp_path, "wb") as out:
            out.write(uploaded_file.read())

        # Send to backend
        with st.spinner("Uploading and processing video..."):
            update_status("Uploading video to backend...")
            try:
                resp = post_video_file(tmp_path)
            except Exception as e:
                update_status(f"Failed to contact backend: {e}", success=False)
                resp = None

        if resp is None:
            update_status("No response from backend", success=False)
        else:
            if resp.status_code != 200:
                update_status(f"Backend error {resp.status_code}: {resp.text}", success=False)
            else:
                # show progressive steps from JSON response
                try:
                    j = resp.json()
                except Exception:
                    update_status("Backend returned non-JSON response", success=False)
                    j = None

                if j:
                    update_status("Processing complete — showing results")
                    with output_container:
                        st.markdown("### Detection Result")
                        st.json(j)

                        # show clip and frame if returned
                        clip_path = j.get("clip_path")
                        best_frame = j.get("best_frame")
                        sos_message = j.get("sos_message")

                        if sos_message:
                            st.markdown("#### Generated SOS Message")
                            st.markdown(sos_message)

                        if clip_path and os.path.exists(clip_path):
                            st.markdown("#### Saved clip (from backend)")
                            st.video(clip_path)

                        if best_frame and os.path.exists(best_frame):
                            st.markdown("#### Representative frame")
                            st.image(best_frame, caption="Best confidence frame")

                        st.markdown("---")
                        st.success("SOS sent to Telegram group (if configured)")

st.markdown("---")
st.caption("Built with ❤️ — Accident Alert AI | Streamlit dashboard for hackathon demo")
