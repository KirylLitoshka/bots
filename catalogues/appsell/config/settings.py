import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
STORAGE_PATH = os.path.join(STORAGE_DIR, "storage.json")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
IMG_DIR = os.path.join(MEDIA_DIR, "img")

CATALOGUE_TYPES = ["Каталог шаблонов", "Каталог приложений"]
PLATFORM_TYPES = ["OS", "Android"]
TEMPLATE_TYPES = ["Утилиты", "Игры", "Остальное"]
