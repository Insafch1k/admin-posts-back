import os
from pyrogram import Client
from decouple import config

CHANNEL = "english2020easy"

# Создаём папку для медиа, если не существует
MEDIA_FOLDER = "media"
os.makedirs(MEDIA_FOLDER, exist_ok=True)

# Создаём сессию клиента
api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')

app = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


def get_text_media(channel=CHANNEL, limit=10):
    with app:
        print(f"Парсинг канала: {channel}")

        for message in app.get_chat_history(channel, limit):
            # Проверяем: есть ли медиа и можно ли её скачать
            print(f'ID сообщения: {message.id}')

            if message.photo or message.video:
                print(f"\n📥 Медиа найдено в сообщении {message.id}")
                try:
                    saved_path = app.download_media(message, file_name="downloads/media/")
                    print(f"✅ Сохранено в: {saved_path}")
                except Exception as e:
                    print(f"❌ Ошибка при скачивании: {e}")

            elif message.text:
                print(f"[{message.date}] {message.text}")
