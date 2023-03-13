from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from catalogues.patrona.bot_mother.commands import set_bot_commands
from catalogues.patrona.bot_mother.handlers import *
from catalogues.patrona.bot_mother.profile import User
from catalogues.patrona.bot_mother.settings import STORAGE_DIR, USERS_DIR
from utils.loaders import load_users


async def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(restart, commands=["restart"])
    dp.register_callback_query_handler(restart, lambda msg: msg.data == "restart")
    dp.register_message_handler(change_language, commands=["language"])
    dp.register_callback_query_handler(
        change_user_language, lambda msg: msg.data == "ru" or msg.data == "en", state="*")
    dp.register_message_handler(process_gender, state=User.gender)
    dp.register_message_handler(process_novel_link, state=User.bot_type)


async def patrona_mother_bot(api_token):
    bot = Bot(api_token)
    dp = Dispatcher(bot, storage=JSONStorage(USERS_DIR))
    dp.data['users'] = load_users(STORAGE_DIR)
    await register_handlers(dp)
    await set_bot_commands(dp)
    return dp
