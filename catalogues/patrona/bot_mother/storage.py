import json
import aiofiles
from aiogram import Dispatcher
from catalogues.patrona.bot_mother.settings import STORAGE_DIR


def set_users(dispatcher):
    with open(f"{STORAGE_DIR}/users.json", mode="r", encoding="utf8") as user_storage:
        users_data = json.loads(user_storage.read())
    dispatcher.data['users'] = users_data


async def save_user(dp: Dispatcher, user: dict):
    user_id = user["id"]
    dp.data['users'][user_id] = user
    async with aiofiles.open(f'{STORAGE_DIR}/users/{user_id}.json', mode="w") as fp:
        await fp.write(json.dumps(user, indent=4, ensure_ascii=False))
