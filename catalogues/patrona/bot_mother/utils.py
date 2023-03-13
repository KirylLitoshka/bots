from datetime import datetime
from aiogram import types, Dispatcher
from catalogues.patrona.bot_mother.storage import save_user


def get_referral_type(message: str):
    sequence = message.split()
    if len(sequence) > 1:
        return sequence[1]
    return None


async def create_new_user(message: types.Message):
    if message.from_user.is_bot:
        return
    user_id = str(message.from_user.id)
    current_time = datetime.now().replace(microsecond=0)
    timestamp = str(int(current_time.timestamp()))
    dp = Dispatcher.get_current()
    user_ref = get_referral_type(message.text)
    if user_id in dp.data["users"]:
        return
    user = {
        "id": user_id,
        "referral_type": user_ref,
        "created": timestamp
    }
    await save_user(dp, user)
