import os
import pathlib

ROOT_PATH = pathlib.Path(__file__).parent
STORAGE_DIR = os.path.join(ROOT_PATH, "storage")
STORAGE = os.path.join(STORAGE_DIR, "storage.json")
ADMIN_CHAT_ID = ""  # Optional[int|str]
