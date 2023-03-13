import os
import pathlib


STORAGE_DIR = os.path.join(pathlib.Path(__file__).parent, "storage")
USERS_DIR = os.path.join(STORAGE_DIR, "users.json")

GENDER_CHOICES = {
    "ru": {
        "text": "С кем ты хочешь начать свой диалог?",
        "buttons": ["💁‍♂️ Парни", "💁‍♀️ Девушки"]
    },
    "en": {
        "text": "Who do you want to start your dialogue with?",
        "buttons": ["💁‍♂️ Men", "💁‍♀️ Women"]
    }
}

BOT_TYPES = {
    "ru": {
        "text": "Выберите визуальный стиль изображений в истории.\n\n<i>В наших историях Вы можете увидеть арты и фотографии с контентом сексуального характера 🔞</i>",
        "buttons": ["💋 Реалистичные 2D арты", "📸 Фотографии", "🍭 Аниме 2D арты"]
    },
    "en": {
        "text": "Choose the visual style of the images in the story.\n\n<i>In our stories you can see art and photos with sexual content 🔞</i>",
        "buttons": ["💋 Realistic 2D art", "📸 Pictures", "🍭 2D anime art"]
    }
}

NOVELS_TEXT = {
    "ru": {
        "pre_text": "Ищем собеседника. Пожалуйста, подождите...",
        "text": """
Твой собеседник уже ждет тебя в чате.
Переходи по ссылке
        """,
        "link_text": "Начать общение",
        "setting_text": "Изменить настройки подбора"
    },
    "en": {
        "pre_text": "Looking for a chat partner. Please hold on...",
        "text": """
Your chatting partner is already waiting for you in the chat room.
Follow this link
        """,
        "link_text": "Start chatting",
        "setting_text": "Change search settings"
    }
}


NOVELS_LINK = {
    "ru": {
        "💁‍♂️ Парни": {
            "💋 Реалистичные 2D арты": "https://t.me/danielle_el_patrona_bot?start=user_from_motherbot",
            "📸 Фотографии": "https://t.me/James_el_patrona_bot?start=user_from_motherbot",
            "🍭 Аниме 2D арты": "https://t.me/Minho_el_patrona_bot?start=user_from_motherbot"
        },
        "💁‍♀️ Девушки": {
            "💋 Реалистичные 2D арты": "https://t.me/denise_el_patrona_bot?start=user_from_motherbot",
            "📸 Фотографии": "https://t.me/bruna_el_patrona_bot?start=user_from_motherbot",
            "🍭 Аниме 2D арты": "https://t.me/rena_el_patrona_bot?start=user_from_motherbot"
        }
    },
    "en": {
        "💁‍♂️ Men": {
            "💋 Realistic 2D art":"https://t.me/danielle_el_patrona_bot?start=user_from_motherbot",
            "📸 Pictures": "https://t.me/James_el_patrona_bot?start=user_from_motherbot",
            "🍭 2D anime art": "https://t.me/Minho_el_patrona_bot?start=user_from_motherbot"
        },
        "💁‍♀️ Women": {
            "💋 Realistic 2D art":"https://t.me/denise_el_patrona_bot?start=user_from_motherbot",
            "📸 Pictures": "https://t.me/bruna_el_patrona_bot?start=user_from_motherbot",
            "🍭 2D anime art": "https://t.me/rena_el_patrona_bot?start=user_from_motherbot"
        }
    }
}
