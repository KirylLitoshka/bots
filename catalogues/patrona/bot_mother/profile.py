from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    language = State()
    gender = State()
    bot_type = State()
