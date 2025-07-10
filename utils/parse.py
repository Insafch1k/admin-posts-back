import base64
import os
import schedule
import time

from domain.last_news.dal import LastNewsDAL

from utils.connection_db import connection_db
from utils.data_state import DataFailedMessage
from domain.sources.dal import SourceDAL
from utils.downloads.work_with_photo import tg_app, download_avatar_to_base64, get_history_of_chat, media_download

# Создаём папку для медиа, если не существует
MEDIA_FOLDER = os.path.join('downloads', 'media')
if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER, exist_ok=True)


def get_text_media(limit=10, channel_id=6):
    from domain.sources.bl import SourceBL

    sources = SourceBL.get_sources_by_channel_id(channel_id, type_name='Тг канал')
    result = []
    try:
        for src in sources:
            tg_channel_name = src['source_name']
            source_id = int(src['source_id'])
            new_post = {tg_channel_name: []}
            print(f"📡 Парсинг канала: {tg_channel_name}")
            # Загрузка фото канала
            chat_general_info = download_avatar_to_base64(tg_channel_name)
            tg_channel_avatar = chat_general_info['avatar']
            tg_channel_title = chat_general_info['title']
            subscribers_count = chat_general_info['subscribers']

            query_for_avatar = SourceBL.get_source_by_source_name(tg_channel_name)
            if query_for_avatar and tg_channel_avatar and (
                    query_for_avatar['source_photo'] is None or query_for_avatar[
                'source_photo'] != tg_channel_avatar):
                SourceBL.update_sources(source_id=source_id,
                                                updates={'source_photo': tg_channel_avatar})

            if query_for_avatar and tg_channel_title and (
                    query_for_avatar['source_title'] is None or query_for_avatar[
                'source_title'] != tg_channel_title):
                SourceBL.update_sources(source_id=source_id,
                                                updates={'source_title': tg_channel_title})

            if query_for_avatar and subscribers_count and (
                    query_for_avatar['subscribers'] is None or query_for_avatar[
                'subscribers'] != subscribers_count):
                SourceBL.update_sources(source_id=source_id,
                                                updates={'subscribers': subscribers_count})
            messages = get_history_of_chat(tg_channel_name, limit=limit)

            last_saved_news = LastNewsDAL.get_last_news_by_source_id(source_id)
            last_message_id = last_saved_news['message_id'] if last_saved_news else 0
            print(f"🧾 Последний сохранённый message_id: {last_message_id}")

            newest_message = None

            for message in reversed(messages):
                temp_post_photo_base64_str = None
                if not message.text and not message.caption:
                    continue
                if int(message.id) <= int(last_message_id):
                    continue

                if message.photo:
                    temp_post_photo_base64_str = media_download(message)

                new_post[tg_channel_name].append({
                    'message_id': message.id,
                    'message_date': message.date,
                    'message_text': message.text if message.text else message.caption,
                    'message_photo': temp_post_photo_base64_str[:20] if temp_post_photo_base64_str else None
                })

                newest_message = message

            if newest_message:
                if last_saved_news:
                    new_news = LastNewsDAL.update_last_news_by_id(last_news_id=last_saved_news['last_news_id'],
                                                                  updates={
                                                                      'message_id': newest_message.id,
                                                                      'description': newest_message.text if newest_message.text else newest_message.caption,
                                                                      'pub_date': newest_message.date,
                                                                      'title': newest_message.text if newest_message.text else newest_message.caption,
                                                                      'last_news_photo': temp_post_photo_base64_str,
                                                                      'url': newest_message.id
                                                                  })
                else:
                    new_news = LastNewsDAL.insert_last_news(updates={
                        'message_id': newest_message.id,
                        'source_id': source_id,
                        'description': newest_message.text if newest_message.text else newest_message.caption,
                        'pub_date': newest_message.date,
                        'title': newest_message.text if newest_message.text else newest_message.caption,
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
