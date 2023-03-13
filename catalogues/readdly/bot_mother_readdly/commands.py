from aiogram import Dispatcher, types


async def set_bot_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Restart bot"),
            types.BotCommand("language", "Choose language")
        ]
    )
