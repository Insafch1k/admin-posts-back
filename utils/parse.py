import base64
import os
import schedule
import time

from domain.last_news.dal import LastNewsDAL

from utils.connection_db import connection_db
from utils.data_state import DataFailedMessage
from domain.sources.dal import SourceDAL
from utils.downloads.work_with_photo import tg_app, download_avatar_to_base64, get_history_of_chat

# Создаём папку для медиа, если не существует
MEDIA_FOLDER = os.path.join('downloads', 'media')
if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER, exist_ok=True)


def get_text_media(limit=10, channel_id=6):
    from domain.sources.bl import SourceBL
    Session = connection_db()
    if Session is None:
        return DataFailedMessage(error_message='Ошибка в работе базы данных!')

    sources = SourceBL.get_sources_by_channel_id(channel_id)
    result = []
    try:
        for src in sources:
            tg_channel_name = src['source_name']
            new_post = {tg_channel_name: []}
            print(f"📡 Парсинг канала: {tg_channel_name}")

            # Загрузка фото канала
            tg_channel_avatar, tg_channel_title = download_avatar_to_base64(tg_channel_name)

            query_for_avatar = SourceDAL.get_source_by_source_name(tg_channel_name)

            if query_for_avatar and tg_channel_avatar and (
                    query_for_avatar['source_photo'] is None or query_for_avatar[
                'source_photo'] != tg_channel_avatar):
                SourceDAL.update_sources_values(source_id=src['source_id'],
                                                updates={'source_photo': tg_channel_avatar})

            if query_for_avatar and tg_channel_title and (
                    query_for_avatar['source_title'] is None or query_for_avatar[
                'source_title'] != tg_channel_title):
                SourceDAL.update_sources_values(source_id=src['source_id'],
                                                updates={'source_title': tg_channel_title})

            messages = get_history_of_chat(tg_channel_name, limit=limit)

            last_saved_news = LastNewsDAL.get_last_news_by_source_id(src['source_id'])

            last_message_id = last_saved_news['message_id'] if last_saved_news else 0
            print(f"🧾 Последний сохранённый message_id: {last_message_id}")

            newest_message = None

            for message in reversed(messages):
                temp_post_photo_base64_str = None
                if not message.text:
                    continue
                if int(message.id) <= int(last_message_id):
                    continue

                if message.photo:
                    temp_post_photo_base64_str = get_history_of_chat(message)

                new_post[tg_channel_name].append({
                    'message_id': message.id,
                    'message_date': message.date,
                    'message_text': message.text,
                    'message_photo': temp_post_photo_base64_str[:20] if temp_post_photo_base64_str else None
                })

                newest_message = message

            if newest_message:
                if last_saved_news:
                    new_news = LastNewsDAL.update_last_news_by_id(last_news_id=last_saved_news['last_news_id'],
                                                                  updates={
                                                                      'message_id': newest_message.id,
                                                                      'description': newest_message.text,
                                                                      'pub_date': newest_message.date,
                                                                      'title': newest_message.text,
                                                                      'last_news_photo': temp_post_photo_base64_str,
                                                                      'url': newest_message.id
                                                                  })
                else:
                    new_news = LastNewsDAL.insert_last_news(values={
                        'message_id': newest_message.id,
                        'source_id': src['source_id'],
                        'description': newest_message.text,
                        'pub_date': newest_message.date,
                        'title': newest_message.text,
                        'last_news_photo': temp_post_photo_base64_str,
                        'url': newest_message.id
                    })
                print(f"\n💾 Сохранено новое сообщение с ID {newest_message.id}")
            else:
                print("📭 Нет новых сообщений")
            result.append(new_post)

        return result

    except Exception as e:
        print("❌ Ошибка при получении сообщений:", e)


# print(get_text_media(channel_id=6))

#
# Планируем выполнение функции каждые 5 минут
# schedule.every(5).minutes.do(get_text_media)
#
# print("⏳ Сервис парсинга запущен. Каждые 5 минут будет проверка канала.")
#
# # Запуск цикла
# while True:
#     schedule.run_pending()
#     time.sleep(1)
