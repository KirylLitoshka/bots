from aiogram import Bot, Dispatcher
from handlers.readdly.utils import register_handlers, register_commands, prepare_dispatcher_data
from catalogues.readdly.bot_reina.config.setting import DEFAULT_USER_MODEL, STORAGE_DIRS


async def reina_bot(api_token):
    bot = Bot(api_token)
    dispatcher = Dispatcher(bot)
    await register_handlers(dispatcher)
    await register_commands(dispatcher)
    prepare_dispatcher_data(dispatcher, STORAGE_DIRS, DEFAULT_USER_MODEL)
    return dispatcher
