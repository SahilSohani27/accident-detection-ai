import requests
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Must be before os.getenv
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")     

class TelegramNotifier:
    def __init__(self, bot_token: str = BOT_TOKEN, chat_id: str = CHAT_ID):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, message: str):
        """Send a text message to the Telegram group"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                # temporarily remove MarkdownV2 for testing plain text
                # "parse_mode": "MarkdownV2"
            }
            r = requests.post(url, data=payload)
            response_json = r.json()
            logger.info(f"send_message response: {response_json}")
            return response_json
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return None

    def send_video(self, video_path: str, caption: str = None):
        """Send a video file to the Telegram group"""
        try:
            url = f"{self.base_url}/sendVideo"
            with open(video_path, "rb") as video:
                r = requests.post(
                    url,
                    data={"chat_id": self.chat_id, "caption": caption or ""},
                    files={"video": video},
                )
            response_json = r.json()
            logger.info(f"send_video response: {response_json}")
            return response_json
        except Exception as e:
            logger.error(f"Failed to send video: {e}")
            return None

    def send_sos(self, message: str, video_path: str = None):
        """Send SOS alert with text + optional video"""
        logger.info("Sending SOS message...")
        msg_resp = self.send_message(message)
        if msg_resp and msg_resp.get("ok"):
            logger.info("SOS text message sent successfully")
        else:
            logger.error("Failed to send SOS text message")
    
        if video_path:
            logger.info(f"Sending SOS video: {video_path}")
            vid_resp = self.send_video(video_path, caption="🚨 Accident footage attached")
            if vid_resp and vid_resp.get("ok"):
                logger.info("SOS video sent successfully")
            else:
                logger.error("Failed to send SOS video")
