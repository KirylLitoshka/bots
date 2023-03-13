import pathlib
import os
from aiogram import Bot, Dispatcher
from catalogues.readdly.bot_mother_readdly.commands import set_bot_commands
from catalogues.readdly.bot_mother_readdly.handlers import show_menu, switch_language
from handlers.readdly.utils import choose_language
from utils.loaders import load_users


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    dp.data['storage'] = os.path.join(pathlib.Path(__file__).parent, "storage")
    dp.data['users'] = load_users(dp.data['storage'])
    dp.register_message_handler(choose_language, commands=["language"])
    dp.register_callback_query_handler(switch_language, lambda msg: msg.data.lower() in ["ru", "en", "es"])
    dp.register_message_handler(show_menu, commands=["start"])


async def readdly_mother_bot(api_token):
    bot = Bot(api_token)
    dispatcher = Dispatcher(bot)
    await on_startup(dispatcher)
    return dispatcher
