from aiogram import Dispatcher
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from handlers.patrona.choices import check_args


def reply_keyboard(user, message_args):
    dialogs = Dispatcher.get_current().data["dialogs"]
    user_language = user["language"]
    if not message_args["choices"]:
        return ReplyKeyboardRemove()
    else:
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        )
        user_answers = []
        for index, choice in enumerate(message_args["choices"]):
            if message_args["choices_param"]:
                args_for_checking = message_args["choices_param"][index]["check_args"]
                if not check_args(user, args_for_checking):
                    continue
            choice_message = dialogs[choice]
            msg = choice_message[user_language]
            if "*" in msg:
                msg = msg.replace("*", user["username"])
            keyboard.add(KeyboardButton(msg))
            next_id = choice_message.get("jump_id") or str(int(choice) + 1)
            on_choice = None
            if choice_message["choices"]:
                for choice_index, answer_choice in enumerate(choice_message["choices"]):
                    if choice_message["choices_param"]:
                        args_for_checking = choice_message["choices_param"][choice_index]["check_args"]
                        if not check_args(user, args_for_checking):
                            continue
                        next_id = choice_message["choices"][choice_index]
            if message_args["choices_param"]:
                on_choice = message_args["choices_param"][index]["on_choice"]
            user_answers.append({
                "text": msg.strip(),
                "next_id": next_id,
                "on_choice": on_choice,
            })
        user["registered_answers"] = user_answers
        return keyboard
