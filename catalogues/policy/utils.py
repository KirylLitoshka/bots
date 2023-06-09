import gzip
import hashlib
import os
from datetime import datetime, timezone

import aiofiles
from aiogram import Dispatcher
from firebase_admin import credentials, initialize_app

from catalogues.policy.client import create_page
from catalogues.policy.settings import FILES_DIR, STORAGE_DIR


def get_referral_type(message: str):
    sequence = message.split()
    if len(sequence) > 1:
        return sequence[1]
    return None


async def prepare_text_data(user, file_name):
    file_path = os.path.join(FILES_DIR, file_name)
    async with aiofiles.open(file_path) as file:
        text = await file.read()
        if not text:
            return None
    text = text.replace("<<NAME DEVELOPER>>", user["name"])
    text = text.replace("<<NAME APPLICATIONS>>", user["application_name"])
    text = text.replace("<<E-MAIL>>", user["mail"])
    return text


async def get_file_hash(user_data: dict, file_name: str):
    markup_text = await prepare_text_data(user_data, file_name)
    return gzip.compress(markup_text.encode())


def get_google_credentials():
    cred = credentials.Certificate(f"{STORAGE_DIR}/service_account.json")
    default_app = initialize_app(credential=cred)
    return default_app.credential


def is_token_expired(google_token):
    current_time = datetime.now(tz=timezone.utc).replace(tzinfo=None)
    token_expiry = google_token.expiry
    if current_time > token_expiry:
        return True
    return False


async def build_link(user_data: dict, file_name: str):
    gzip_data = await get_file_hash(user_data, file_name)
    hash_data = hashlib.sha256(gzip_data).hexdigest()
    dispatcher = Dispatcher.get_current()
    google_credentials = dispatcher.data["google_api_cred"]
    api_token = dispatcher.data.get("google_api_key", None)
    if api_token is None or is_token_expired(api_token):
        api_token = google_credentials.get_access_token()
        dispatcher.data["google_api_key"] = api_token
    return await create_page(api_token.access_token, hash_data, gzip_data, user_data)


async def build_policy(user_data: dict):
    policy_file_name = "policy.txt"
    return await build_link(user_data, policy_file_name)


async def build_terms_of_use(user_data: dict):
    terms_file_name = "terms.txt"
    return await build_link(user_data, terms_file_name)
