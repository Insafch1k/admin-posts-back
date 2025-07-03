import os
import schedule
import time
import io
import base64
from pyrogram import Client
from decouple import config

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


# def get_text_media(limit=10, channel_id=1):
#     db_manager.init_db()
#     with db_manager.session() as session:
#         if session is None:
#             print("❌ Не удалось получить сессию БД")
#             return
#
#         with app:  # ✅ Только один раз
#             sources = get_sources_by_channel_id(channel_id)
#             result = []
#             try:
#                 for src in sources:
#                     tg_channel_name = src['name']
#                     new_post = {tg_channel_name: []}
#                     print(f"📡 Парсинг канала: {tg_channel_name}")
#
#                     # Загрузка фото канала
#                     tg_channel_avatar, tg_channel_title = download_avatar_to_base64(app, tg_channel_name)
#
#                     query_for_avatar = session.execute(
#                         select(Source).filter(Source.source_name == tg_channel_name)
#                     ).scalars().first()
#
#                     if query_for_avatar and tg_channel_avatar and (
#                             query_for_avatar.source_photo is None or query_for_avatar.source_photo != tg_channel_avatar):
#                         print('1')
#                         query_for_avatar.source_photo = tg_channel_avatar
#                         session.add(query_for_avatar)
#                         session.commit()
#
#                     if query_for_avatar and tg_channel_title and (
#                             query_for_avatar.source_title is None or query_for_avatar.source_title != tg_channel_title):
#                         print('2')
#                         query_for_avatar.source_title = tg_channel_title
#                         session.add(query_for_avatar)
#                         session.commit()
#
#                     messages = list(app.get_chat_history(tg_channel_name, limit=limit))
#
#                     last_saved_news: LastNews = session.execute(
#                         select(LastNews).filter(LastNews.source_id == src['id']).order_by(LastNews.message_id.desc())
#                     ).scalars().first()
#
#                     last_message_id = last_saved_news.message_id if last_saved_news else 0
#                     print(f"🧾 Последний сохранённый message_id: {last_message_id}")
#
#                     newest_message = None
#
#                     for message in reversed(messages):
#                         temp_post_photo_base64_str = None
#                         if not message.text:
#                             continue
#                         if int(message.id) <= int(last_message_id):
#                             continue
#
#                         if message.photo:
#                             file_path = app.download_media(message.photo.file_id, file_name="temp_post_photo.jpg")
#                             with open(file_path, "rb") as f:
#                                 temp_post_photo_base64_str = base64.b64encode(f.read()).decode("utf-8")
#                             os.remove(file_path)
#
#                         new_post[tg_channel_name].append({
#                             'message_id': message.id,
#                             'message_date': message.date,
#                             'message_text': message.text,
#                             'message_photo': temp_post_photo_base64_str[:20] if temp_post_photo_base64_str else None
#                         })
#
#                         newest_message = message
#
#                     if newest_message:
#                         new_news = LastNews(
#                             message_id=newest_message.id,
#                             source_id=src['id'],
#                             description=newest_message.text,
#                             pub_date=newest_message.date,
#                             title=newest_message.text,
#                             photo=temp_post_photo_base64_str
#                         )
#                         session.add(new_news)
#                         session.commit()
#                         print(f"\n💾 Сохранено новое сообщение с ID {newest_message.id}")
#                     else:
#                         print("📭 Нет новых сообщений")
#                     result.append(new_post)
#
#                 return result
#
#             except Exception as e:
#                 session.rollback()
#                 print("❌ Ошибка при получении сообщений:", e)
#             finally:
#                 session.close()


# print('Общий результат: ', get_text_media())


# def get_extension(message):
#     if message.photo:
#         return ".jpg"
#     elif message.video:
#         return ".mp4"
#     elif message.audio:
#         return ".mp3"
#     elif message.voice:
#         return ".ogg"
#     elif message.document:
#         return ".pdf" if "pdf" in message.document.mime_type else ".doc"
#     elif message.animation:
#         return ".gif"
#     elif message.sticker:
#         return ".webp"
#     elif message.video_note:
#         return ".mp4"
#     else:
#         return ".bin"  # по умолчанию

# if message.photo or message.video:
#     print(f"📥 B сообщении найдено медиа")
#     #Удаляем старый media.temp, если он остался
#     temp_path = os.path.join(MEDIA_FOLDER, "media.temp")
#     if os.path.exists(temp_path):
#         try:
#             os.remove(temp_path)
#             print("🧹 Удалён старый временный файл media.temp")
#         except Exception as e:
#             print(f"⚠️ Ошибка при удалении media.temp: {e}")
#
#     try:
#         # Генерируем уникальное имя файла по ID сообщения
#         ext = get_extension(message)
#         filename = f"{message.id}{ext}"
#         file_path = os.path.join(MEDIA_FOLDER, filename)
#
#         if not os.path.exists(file_path):
#             saved_path = app.download_media(message, file_name=file_path)
#             print(f"✅ Сохранено в: {saved_path}")
#         else:
#             print(f"ℹ️ Файл уже существует: {file_path}, скачивание пропущено")
#     except Exception as e:
#         print(f"❌ Ошибка при скачивании: {e}")


# Работа с тг-каналом
#
CHANNEL = "artemshumeiko"


def get_text_media1(channel=CHANNEL, limit=3, channel_id=1):
    with app:
        print(f"Парсинг канала: {channel}")
        for message in app.get_chat_history(channel, limit):
            print(message)
            if message.text:
                print(f"\n🧾 ID сообщения: {message.id}")
                print(f"[{message.date}] \ntext: {message.text}")
        # chat = app.get_chat(channel)
        # print(chat.title)


# get_text_media1()

# from domain.last_news.dal import LastNewsDAL
#
# lsd = LastNewsDAL()
# lsd.get_last_news_by_source_id(1)

# Работа с БД


# def create_tables():
#     import domain
#     Session, engine = connection_db()
#     Base.metadata.drop_all(engine)
#     engine.echo = True
#     Base.metadata.create_all(engine)
#     engine.echo = True
#
#
# create_tables()

# def add_values_into_tables():
#     import domain
#     Session, engine = connection_db()
#     with Session() as session:
#         user1 = User(tg_id=1, name='Asadbek', login='qwerty', password='qwerty')
#         bot1 = BotStorage(bot_key=1234)
#         channel1 = Channel(channel_username='channel_with_autoposting', bot_id=1, user_id=1)
#         source_type_1 = SourceType(type_name='Тг канал')
#         source_type_2 = SourceType(type_name='RSS лента')
#         source1 = Source(source_name='LCG_KZN', type_id=1, channel_id=1)
#         source2 = Source(source_name='english2020easy', type_id=1, channel_id=1)
#         session.add_all([user1, bot1, channel1, source_type_1, source_type_2, source1, source2])
#         # flush отправляет запрос в базу данных
#         # После flush каждый из работников получает первичный ключ id, который отдала БД
#         # session.flush()
#         session.commit()
#
#
# add_values_into_tables()

# def get_channel_of_source():
#     db_manager.init_db()
#     with db_manager.session() as session:
#         query = (
#             select(Source)
#             .options(joinedload(Source.source_channel))
#         )
#         res = session.execute(query)
#         result = res.unique().scalars().all()
#         print(result[0].source_channel)
#
#
# # get_channel_of_source()
#
# def queries():
#     db_manager.init_db()
#     with db_manager.session() as session:
#         query_for_avatar = session.execute(
#             select(Source).filter(Source.source_name == 'english2020easy')).scalars().first()
#
#         print(query_for_avatar.source_photo)
#
# # queries()
