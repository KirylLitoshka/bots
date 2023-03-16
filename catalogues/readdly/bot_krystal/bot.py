from aiogram import Bot, Dispatcher

from catalogues.readdly.bot_krystal.config.setting import (DEFAULT_USER_MODEL,
                                                           STORAGE_DIRS)
from handlers.readdly.utils import (prepare_dispatcher_data, register_commands,
                                    register_handlers)


async def krystal_bot(api_token):
    bot = Bot(api_token)
    dispatcher = Dispatcher(bot)
    await register_handlers(dispatcher)
    await register_commands(dispatcher)
    prepare_dispatcher_data(dispatcher, STORAGE_DIRS, DEFAULT_USER_MODEL)
    return dispatcher
