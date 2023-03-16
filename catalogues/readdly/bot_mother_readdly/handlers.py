import json
from datetime import datetime

import aiofiles
from aiogram import Dispatcher, types

from catalogues.readdly.bot_mother_readdly.messages import MENU_MESSAGE
from handlers.readdly.messages import get_user_language


def get_referral_type(message: str):
    sequence = message.split()
    if len(sequence) > 1:
        return sequence[1]
    return None


async def save_user(dp: Dispatcher, user: dict):
    user_id = user["id"]
    dp.data['users'][user_id] = user
    async with aiofiles.open(f'{dp.data["storage"]}/users/{user_id}.json', mode="w") as fp:
        await fp.write(json.dumps(user, indent=4, ensure_ascii=False))


async def create_new_user(message: types.Message):
    dp = Dispatcher.get_current()
    user_id = str(message.from_user.id)
    if message.from_user.is_bot:
        user_id = str(message.chat.id)
    if user_id in dp.data["users"]:
        return dp.data['users'][user_id]
    user_language = get_user_language(message)
    current_time = datetime.now().replace(microsecond=0)
    timestamp = str(int(current_time.timestamp()))
    user_ref = get_referral_type(message.text)
    user = {
        "id": user_id,
        "referral_type": user_ref,
        "created": timestamp,
        "language_code": user_language
    }
    await save_user(dp, user)
    return user


async def show_menu(message: types.Message):
    current_user = await create_new_user(message)
    user_language = current_user.get("language_code", None)
    if not user_language:
        user_language = message.from_user.language_code
        current_user["language_code"] = user_language
    output_message = MENU_MESSAGE[user_language]
    await message.answer(
        text=output_message["text"],
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(button["label"], button["url"])] for button in output_message["buttons"]
            ]
        ),
        parse_mode="HTML"
    )


async def switch_language(query: types.CallbackQuery):
    user_id = str(query.from_user.id)
    dispatcher = Dispatcher.get_current()
    current_user = dispatcher.data["users"][user_id]
    current_user["language_code"] = query.data
    await save_user(dispatcher, current_user)
    return await show_menu(query.message)
