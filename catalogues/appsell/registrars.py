import asyncio

from aiogram import Dispatcher, types

from catalogues.appsell.config.settings import CATALOGUE_TYPES, PLATFORM_TYPES
from catalogues.appsell.handlers import main_menu, about, catalogues_process_selection, platform_process_selection, \
    template_process_selection
from catalogues.appsell.profiles import Profile
from catalogues.appsell.tasks import test_task


async def register_dispatcher_handlers(dp: Dispatcher):
    dp.register_message_handler(main_menu, commands=['start', 'menu'], state="*")
    dp.register_message_handler(about, commands=['about'], state="*")
    dp.register_message_handler(about, lambda msg: msg.text == "О боте", state="*")
    dp.register_message_handler(catalogues_process_selection, lambda msg: msg.text in CATALOGUE_TYPES)
    dp.register_message_handler(platform_process_selection, state=Profile.platform_type)
    dp.register_message_handler(template_process_selection, state=Profile.template_type)


async def register_dispatcher_tasks(dp: Dispatcher):
    asyncio.create_task(test_task(dp))


async def register_bot_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("menu", "Возврат в главное меню"),
        types.BotCommand("about", "О боте")
    ])
