from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage

from catalogues.policy.dispatcher import register_handlers
from catalogues.policy.settings import BOT_STORAGE


async def policy_bot(token):
    bot = Bot(token)
    dispatcher = Dispatcher(bot, storage=JSONStorage(BOT_STORAGE))
    await register_handlers(dispatcher)
    return dispatcher
