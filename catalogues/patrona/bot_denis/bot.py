from aiogram import Bot, Dispatcher
from catalogues.patrona.bot_denis.config import setting
from handlers.patrona.registrars import register_handlers, register_commands
from utils.loaders import load_users, load_dialogs


async def denis_bot(api_token):
    bot = Bot(api_token)
    dp = Dispatcher(bot)
    dp.data["dirs"] = setting.STORAGE_DIRS
    dp.data["default_user_model"] = setting.DEFAULT_USER_MODEL
    dp.data["dialogs"] = load_dialogs(dp.data["dirs"]["STORAGE_DIR"], "dialogs")
    dp.data["users"] = load_users(dp.data["dirs"]["STORAGE_DIR"])
    await register_handlers(dp)
    await register_commands(dp)
    return dp

