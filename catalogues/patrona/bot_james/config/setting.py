import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
STATIC_DIR = os.path.join(BASE_DIR, "static")

STORAGE_DIRS = {
    "STORAGE_DIR": os.path.join(BASE_DIR, "storage"),
    "MEDIA_DIR": os.path.join(STATIC_DIR, "media"),
    "IMAGES_DIR": os.path.join(STATIC_DIR, "img")
}

DEFAULT_USER_MODEL = {
    "last_received_message_id": None,
    "active": 0,
    "registered_answers": [{"text": "/start", "next_id": "0", "on_choice": None}],
}
