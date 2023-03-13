from aiogram.types import BotCommand


async def set_bot_commands(dispatcher):  # dispatcher: Dispatcher
    await dispatcher.bot.set_my_commands(
        [
            BotCommand("back", "Choose another story"),
            BotCommand("language", "Choose language"),
        ]
    )
