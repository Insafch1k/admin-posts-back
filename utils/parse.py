import base64
import os
import schedule
import time
from pyrogram import Client
from decouple import config
from sqlalchemy import text, select, and_

from utils.connection_db import connection_db
from utils.data_state import DataFailedMessage
from domain.sources.dal import SourecDAL

# Создаём папку для медиа, если не существует
MEDIA_FOLDER = os.path.join('downloads', 'media')
if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER, exist_ok=True)

# Создаём сессию клиента
api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')

app = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


def download_avatar_to_base64(app, tg_channel_name):
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


# download_avatar_to_base64()


def get_text_media(limit=10, channel_id=1):
    Session = connection_db()
    if Session is None:
        return DataFailedMessage(error_message='Ошибка в работе базы данных!')

    with Session() as session:
        if session is None:
            print("❌ Не удалось получить сессию БД")
            return

        with app:  # ✅ Только один раз
            sources = SourecDAL.get_sources_by_channel_id(channel_id)
            result = []
            try:
                for src in sources:
                    tg_channel_name = src['name']
                    new_post = {tg_channel_name: []}
                    print(f"📡 Парсинг канала: {tg_channel_name}")

                    # Загрузка фото канала
                    tg_channel_avatar, tg_channel_title = download_avatar_to_base64(app, tg_channel_name)

                    query_for_avatar = SourecDAL.get_source_by_source_name(tg_channel_name)

                    if query_for_avatar and tg_channel_avatar and (
                            query_for_avatar.source_photo is None or query_for_avatar.source_photo != tg_channel_avatar):
                        query_for_avatar.source_photo = tg_channel_avatar
                        session.add(query_for_avatar)
                        session.commit()

                    if query_for_avatar and tg_channel_title and (
                            query_for_avatar.source_title is None or query_for_avatar.source_title != tg_channel_title):
                        query_for_avatar.source_title = tg_channel_title
                        session.add(query_for_avatar)
                        session.commit()

                    messages = list(app.get_chat_history(tg_channel_name, limit=limit))

                    last_saved_news: LastNews = session.execute(
                        select(LastNews).filter(LastNews.source_id == src['id']).order_by(LastNews.message_id.desc())
                    ).scalars().first()

                    last_message_id = last_saved_news.message_id if last_saved_news else 0
                    print(f"🧾 Последний сохранённый message_id: {last_message_id}")

                    newest_message = None

                    for message in reversed(messages):
                        temp_post_photo_base64_str = None
                        if not message.text:
                            continue
                        if int(message.id) <= int(last_message_id):
                            continue

                        if message.photo:
                            file_path = app.download_media(message.photo.file_id, file_name="temp_post_photo.jpg")
                            with open(file_path, "rb") as f:
                                temp_post_photo_base64_str = base64.b64encode(f.read()).decode("utf-8")
                            os.remove(file_path)

                        new_post[tg_channel_name].append({
                            'message_id': message.id,
                            'message_date': message.date,
                            'message_text': message.text,
                            'message_photo': temp_post_photo_base64_str[:20] if temp_post_photo_base64_str else None
                        })

                        newest_message = message

                    if newest_message:
                        new_news = LastNews(
                            message_id=newest_message.id,
                            source_id=src['id'],
                            description=newest_message.text,
                            pub_date=newest_message.date,
                            title=newest_message.text,
                            photo=temp_post_photo_base64_str
                        )
                        session.add(new_news)
                        session.commit()
                        print(f"\n💾 Сохранено новое сообщение с ID {newest_message.id}")
                    else:
                        print("📭 Нет новых сообщений")
                    result.append(new_post)

                return result

            except Exception as e:
                session.rollback()
                print("❌ Ошибка при получении сообщений:", e)
            finally:
                session.close()

#
# # Планируем выполнение функции каждые 5 минут
schedule.every(1).minutes.do(get_text_media)

print("⏳ Сервис парсинга запущен. Каждые 5 минут будет проверка канала.")

# Запуск цикла
while True:
    schedule.run_pending()
    time.sleep(1)
