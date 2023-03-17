from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from catalogues.appsell.config.settings import CATALOGUE_TYPES, PLATFORM_TYPES, TEMPLATE_TYPES
from catalogues.appsell.profiles import Profile
from catalogues.appsell.storage import create_new_user


async def main_menu(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in Dispatcher.get_current().data["users"]:
        await create_new_user(user_id)
    current_state = await state.get_state()
    if current_state:
        await state.finish()

    await message.answer(
        text="Текст главного меню",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                *[[types.KeyboardButton(catalogue)] for catalogue in CATALOGUE_TYPES],
                [types.KeyboardButton("О боте")]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )


async def catalogues_process_selection(message: types.Message, state: FSMContext):
    await Profile.catalogue_type.set()
    async with state.proxy() as data:
        if message.text == "Каталог шаблонов":
            data["catalogue_type"] = "template"
        elif message.text == "Каталог приложений":
            data["catalogue_type"] = "application"
    await Profile.next()
    await message.answer(
        text="Укажите платформу",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(platform)] for platform in PLATFORM_TYPES],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )


async def platform_process_selection(message: types.Message, state: FSMContext):
    if message.text not in PLATFORM_TYPES:
        return await message.delete()
    async with state.proxy() as data:
        data["platform_type"] = message.text
        chosen_catalogue_type = data["catalogue_type"]
        if chosen_catalogue_type == "application":
            await Profile.next()
            data["template_type"] = None
    await Profile.next()
    if chosen_catalogue_type == "template":
        return await message.answer(
            text="Укажите тип шаблона",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[[types.KeyboardButton(template)] for template in TEMPLATE_TYPES],
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )
    else:
        return await process_catalogue_preview(message, state)


async def template_process_selection(message: types.Message, state: FSMContext):
    if message.text not in TEMPLATE_TYPES:
        return await message.delete()
    async with state.proxy() as data:
        data["template_type"] = message.text
    return await process_catalogue_preview(message, state)


async def process_catalogue_preview(message: types.Message, state: FSMContext):
    page_step = 4
    async with state.proxy() as data:
        current_page = data.get("card_page", 1)
        data["card_page"] = current_page + 1
        current_data = data.as_dict()
    await message.answer(str(current_data))
    await state.finish()


async def about(message: types.Message):
    await message.answer(
        text="Информация о боте (возможно добавить кнопку с возвратом в главное меню?)"
    )
