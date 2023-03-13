import os

APP_HOST = os.environ.get("APP_HOST", "localhost")  # localhost by default
APP_PORT = os.environ.get("APP_PORT", 3001)

BASE_URL = ''  # Webhook domain or ngrok public url
WEBHOOK_PATH = '/tg/webhook'
