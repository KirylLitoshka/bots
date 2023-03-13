import os
from config import settings


def get_base_url():
    if not settings.BASE_URL:
        from pyngrok import conf, ngrok
        ngrok.set_auth_token(os.environ.get("NGROK_TOKEN"))  # replace with token from configs
        conf.get_default().region = "eu"
        tunnel = ngrok.connect(settings.APP_PORT)
        settings.BASE_URL = tunnel.public_url.replace("http", "https")
    return settings.BASE_URL
