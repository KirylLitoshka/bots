from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage

from catalogues.diagnosis.dispatcher import register_handlers
from catalogues.diagnosis.settings import STORAGE


async def diagnosis_bot(token: str):
    bot = Bot(token=token)
    dispatcher = Dispatcher(bot, storage=JSONStorage(STORAGE))
    await register_handlers(dispatcher)
    return dispatcher
