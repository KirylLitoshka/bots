from aiogram.dispatcher.filters.state import State, StatesGroup


class Profile(StatesGroup):
    catalogue_type = State()
    platform_type = State()
    template_type = State()
    card_page = State()
