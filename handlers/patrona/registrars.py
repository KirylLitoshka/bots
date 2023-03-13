from aiogram import Dispatcher, types
from handlers.patrona.handlers import echo, restart, back_to_root_bot, choose_language, switch_language


async def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(restart, lambda cmd: cmd.data == "restart")
    dp.register_message_handler(back_to_root_bot, commands=["back"])
    dp.register_message_handler(choose_language, commands=["language"])
    dp.register_callback_query_handler(switch_language, lambda msg: msg.data == "ru" or msg.data == "en")
    dp.register_message_handler(echo)


async def register_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("back", "Choose another story"),
            types.BotCommand("language", "Choose language"),
        ]
    )
