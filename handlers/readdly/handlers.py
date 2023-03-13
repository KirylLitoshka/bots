from aiogram import Dispatcher, types
from handlers.readdly.choices import on_choice_action
from handlers.readdly.messages import sending_messages_till_answer, get_message_referral_type, get_user_language, \
    FINAL_MESSAGE
import typing


async def create_new_user(dp_data, user_id, username):
    dp_data["users"][user_id] = dp_data["default_user_model"].copy()
    dp_data["users"][user_id].update({
        "id": user_id,
        "username": username.title(),
    })


async def echo(message: types.Message):
    dispatcher = Dispatcher.get_current()
    user_id = str(message.from_user.id)
    if user_id not in dispatcher.data["users"]:
        await create_new_user(dispatcher.data, user_id, message.from_user.first_name)
        dispatcher.data["users"][user_id]["referral_type"] = get_message_referral_type(message)
        dispatcher.data["users"][user_id]["language"] = get_user_language(message)
    current_user = dispatcher.data["users"][user_id]
    possible_answers = current_user["registered_answers"]
    answer_texts = [item["text"] for item in possible_answers]
    if message.text not in answer_texts:
        return await dispatcher.bot.delete_message(message.chat.id, message.message_id)
    current_user["registered_answers"] = []
    choice_index = answer_texts.index(message.text)
    if possible_answers[choice_index]["on_choice"]:
        on_choice_expression = possible_answers[choice_index]["on_choice"]
        on_choice_action(current_user, on_choice_expression)
    next_dialog_id = possible_answers[choice_index]["next_id"]
    current_user["last_received_message_id"] = next_dialog_id
    try:
        await sending_messages_till_answer(dispatcher, current_user, user_id, next_dialog_id)
    except KeyError:
        return await back_to_root_bot(message)


async def back_to_root_bot(message: types.Message):
    user_id = str(message.from_user.id)
    current_user = Dispatcher.get_current().data["users"][user_id]
    user_language = current_user['language']
    output_message = FINAL_MESSAGE[user_language]
    inline_keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=output_message["url_button"]["label"],
                    url=output_message["url_button"]["link"],
                )
            ],
            [
                types.InlineKeyboardButton(
                    text=output_message["callback_button"]["label"],
                    callback_data=output_message["callback_button"]["callback_data"],
                )
            ]
        ]
    )
    await message.answer(
        text=output_message["msg"],
        reply_markup=inline_keyboard,
    )


async def choose_language(message: types.Message):
    await message.answer(
        text="Choose your language",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton("RU", callback_data="ru"),
                types.InlineKeyboardButton("EN", callback_data="en"),
                types.InlineKeyboardButton("ES", callback_data="es")
            ]]
        )
    )


async def switch_language(query: types.CallbackQuery):
    user_id = str(query.from_user.id)
    current_user = Dispatcher.get_current().data["users"][user_id]
    current_user["language"] = query.data
    await query.message.answer("Success!")
    await restart(query)


async def restart(query: typing.Union[types.CallbackQuery, types.Message]):
    if isinstance(query, types.CallbackQuery):
        message = query.message
        user_id = str(message.chat.id)
    else:
        message = query
        user_id = str(message.from_user.id)
    dispatcher = Dispatcher.get_current()
    referral_type = dispatcher["users"][user_id].get("referral_type")
    language = dispatcher["users"][user_id].get("language", "en")
    await create_new_user(dispatcher.data, user_id, dispatcher.data["users"][user_id]["username"])
    current_user = dispatcher.data["users"][user_id]
    current_user["referral_type"] = referral_type
    current_user["language"] = language
    await sending_messages_till_answer(dispatcher, current_user, user_id, "0")
