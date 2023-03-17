from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage

from catalogues.appsell.config import settings
from catalogues.appsell.registrars import register_dispatcher_handlers, register_bot_commands, register_dispatcher_tasks


async def send_test_message(dp):
    await dp.bot.send_message("", "test")


async def app_sell_bot(token):
    print(token)
    bot = Bot(token)
    dp = Dispatcher(bot, storage=JSONStorage(settings.STORAGE_PATH))
    await register_dispatcher_handlers(dp)
    await register_dispatcher_tasks(dp)
    await register_bot_commands(dp)
    return dp
