import base64
import os
from pyrogram import Client
from decouple import config

# Создаём сессию клиента
api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')

app = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


def download_avatar_to_base64(tg_channel_name, app=app):
    chat = app.get_chat(tg_channel_name)

    if chat.photo:
        # Шаг 1: Скачиваем фото на диск
        file_path = app.download_media(chat.photo.big_file_id, file_name="temp_avatar.jpg")

        # Шаг 2: Читаем содержимое и кодируем в base64
        with open(file_path, "rb") as f:
            base64_str = base64.b64encode(f.read()).decode("utf-8")

        # Шаг 3: Удаляем временный файл
        os.remove(file_path)
        # print(f'{base64_str[:20]=}', chat.title if chat.title else None)
        return base64_str, chat.title if chat.title else None
    else:
        print("❌ У этого чата нет фото.")
        return None, chat.title if chat.title else None
