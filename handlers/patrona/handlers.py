from aiogram import Dispatcher, types

from handlers.patrona.choices import on_choice_action
from handlers.patrona.messages import sending_messages_till_answer


async def create_new_user(dp_data, user_id, username):
    dp_data["users"][user_id] = dp_data["default_user_model"].copy()
    dp_data["users"][user_id].update({"id": user_id, "username": username.title()})


async def echo(message: types.Message):
    dispatcher = Dispatcher.get_current()
    user_id = str(message.from_user.id)
    if user_id not in dispatcher.data["users"]:
        await create_new_user(dispatcher.data, user_id, message.from_user.first_name)
        if len(message.text.split()) != 1:
            if message.text.startswith("/start"):
                dispatcher.data["users"][user_id]["referral_type"] = message.text.split()[1]
                message.text = message.text.split()[0]
        if message.from_user.language_code == "ru":
            dispatcher.data['users'][user_id]["language"] = "ru"
        else:
            dispatcher.data['users'][user_id]["language"] = "en"
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
        print("key error")
        return await back_to_root_bot(message, finish=True)


async def back_to_root_bot(message: types.Message, finish: bool = None):
    user_id = str(message.from_user.id)
    if user_id not in Dispatcher.get_current().data['users']:
        dp_data = Dispatcher.get_current().data
        await create_new_user(dp_data, user_id, message.from_user.username)
    user = Dispatcher.get_current().data['users'][user_id]
    user_language = user.get("language", "en")
    output = {
        "ru": {
            "line": "Больше историй ждет тебя в @el_patrona_bot 💋",
            "line_button": "📚  Перейти в каталог историй",
            "finish_line": "Cпасибо за прочтение!",
            "finish_link_button": "Начать историю сначала"
        },
        "en": {
            "line": "Find more stories in @el_patrona_bot💋",
            "line_button": "📚 Go to the list of stories",
            "finish_line": "Thanks for reading!",
            "finish_link_button": "Start story over"
        }
    }
    msg = output[user_language]["line"]
    inline_keyboard = types.InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=output[user_language]["line_button"],
                    url="https://t.me/el_patrona_bot",
                )
            ]
        ],
    )
    if finish:
        msg = f"{output[user_language]['finish_line']}\n" + msg
        inline_keyboard.add(
            types.InlineKeyboardButton(output[user_language]['finish_line_button'], callback_data="restart")
        )
    await message.answer(text=msg, reply_markup=inline_keyboard)


async def choose_language(message: types.Message):
    await message.answer(
        text="Choose your language",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton("RU", callback_data="ru"),
                types.InlineKeyboardButton("EN", callback_data="en")
            ]]
        )
    )


async def switch_language(query: types.CallbackQuery):
    user_id = str(query.from_user.id)
    if user_id not in Dispatcher.get_current().data['users']:
        dp_data = Dispatcher.get_current().data
        await create_new_user(dp_data, user_id, query.from_user.username)
    current_user = Dispatcher.get_current().data['users'][user_id]
    current_user["language"] = query.data
    await query.message.answer("Success!")
    await restart(query)


async def restart(query: types.CallbackQuery):
    user_id = str(query.from_user.id)
    dispatcher = Dispatcher.get_current()
    complete_reads_counter = dispatcher["users"][user_id].get("complete_reads_counter", 0)
    referral_type = dispatcher["users"][user_id].get("referral_type")
    language = dispatcher["users"][user_id].get("language")
    await create_new_user(dispatcher.data, user_id, dispatcher.data["users"][user_id]["username"])
    if query.data == "restart":
        dispatcher.data["users"][user_id]["complete_reads_counter"] = complete_reads_counter + 1
    current_user = dispatcher.data["users"][user_id]
    current_user["referral_type"] = referral_type
    current_user["language"] = language
    await sending_messages_till_answer(dispatcher, current_user, user_id, "0")
