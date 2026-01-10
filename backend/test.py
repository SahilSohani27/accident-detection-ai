import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Must be before os.getenv
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("BOT_TOKEN:", BOT_TOKEN)
print("CHAT_ID:", CHAT_ID)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": "🚨 Test SOS: Bot can send messages!"
}

response = requests.post(url, data=payload)
print(response.json())
