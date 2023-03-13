from aiogram import Dispatcher
from aiogram.types import BotCommand

from handlers.readdly.handlers import back_to_root_bot, echo, restart, choose_language, switch_language
from utils.loaders import load_dialogs, load_users


async def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(restart, lambda cmd: cmd.data == "restart")
    dispatcher.register_message_handler(restart, commands=["restart"])
    dispatcher.register_message_handler(choose_language, commands=['language'])
    dispatcher.register_callback_query_handler(switch_language, lambda msg: msg.data.lower() in ["ru", "en", "es"])
    dispatcher.register_message_handler(back_to_root_bot, commands=["back"])
    dispatcher.register_message_handler(echo)


async def register_commands(dispatcher: Dispatcher):
    await dispatcher.bot.set_my_commands(
        [
            BotCommand("back", "Choose another story"),
            BotCommand("restart", "Restart bot"),
            BotCommand("language", "Choose language"),
        ]
    )


def prepare_dispatcher_data(dispatcher: Dispatcher, bot_dirs, default_user_model):
    dispatcher.data["dirs"] = bot_dirs
    dispatcher.data["dialogs"] = load_dialogs(dispatcher.data["dirs"]["STORAGE_DIR"], "dialogs")
    dispatcher.data["users"] = load_users(dispatcher.data["dirs"]["STORAGE_DIR"])
    dispatcher.data["default_user_model"] = default_user_model
