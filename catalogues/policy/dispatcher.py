from aiogram import Dispatcher

from catalogues.policy.commands import cmd_start, set_bot_commands
from catalogues.policy.handlers import *
from catalogues.policy.settings import STORAGE_DIR
from catalogues.policy.storage import load_users
from catalogues.policy.utils import get_google_credentials


async def register_handlers(dp):
    await set_bot_commands(dp)
    dp.data['google_api_cred'] = get_google_credentials()
    dp.data["users"] = load_users(STORAGE_DIR)
    dp.register_message_handler(main_menu, commands=["start"])  # Начинается сразу с главного меню, без опроса
    dp.register_message_handler(create_terms_of_use, commands=["terms"], state="*")
    dp.register_message_handler(create_privacy_policy, commands=["privacy"], state="*")
    dp.register_message_handler(create_terms_of_use, lambda msg: msg.text == "Создать Terms of Use", state="*")
    dp.register_message_handler(create_privacy_policy, lambda msg: msg.text == "Создать Privacy Policy", state="*")
    dp.register_callback_query_handler(create_privacy_policy, lambda msg: msg.data == "privacy", state="*")
    dp.register_callback_query_handler(create_terms_of_use, lambda msg: msg.data == "terms", state="*")
    dp.register_callback_query_handler(main_menu, lambda msg: msg.data == "menu", state="*")
    dp.register_message_handler(
        process_activity_field, lambda msg: msg.text in ACTIVITY_FIELDS, state=Profile.activity_field
    )
    dp.register_message_handler(
        process_error, lambda msg: msg.text not in ACTIVITY_FIELDS, state=Profile.activity_field
    )
    dp.register_message_handler(
        process_application_type, lambda msg: msg.text in APPLICATION_TYPES, state=Profile.application_types
    )
    dp.register_message_handler(
        process_error, lambda msg: msg.text not in APPLICATION_TYPES, state=Profile.application_types
    )
    dp.register_message_handler(process_username, state=User.name)
    dp.register_message_handler(process_application_name, state=User.application_name)
    dp.register_message_handler(process_email, state=User.mail)
    dp.register_message_handler(process_promo_code, state=Profile.promo_code)


async def on_shutdown(dp: Dispatcher):
    dp.stop_polling()
    await dp.wait_closed()
