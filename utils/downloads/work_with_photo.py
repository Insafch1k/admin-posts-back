import asyncio
import base64
import os
from utils.downloads.telegram_client_runner import tg_app, loop

def download_avatar_to_base64(tg_channel_name):

    async def _inner():
        chat = await tg_app.get_chat(tg_channel_name)

        # Получаем количество подписчиков
        members_count = getattr(chat, 'members_count', None)

        result = {
            "avatar": None,
            "title": chat.title or None,
            "subscribers": members_count
        }

        # Если есть фото — загружаем и конвертируем в base64
        if chat.photo:
            file_path = await tg_app.download_media(chat.photo.big_file_id, file_name="temp_avatar.jpg")
            with open(file_path, "rb") as f:
                base64_str = base64.b64encode(f.read()).decode("utf-8")
            os.remove(file_path)
            result["avatar"] = base64_str

        return result

    future = asyncio.run_coroutine_threadsafe(_inner(), loop)
    return future.result()


def get_history_of_chat(tg_channel_name, limit):
    async def _inner():
        messages = []
        async for message in tg_app.get_chat_history(tg_channel_name, limit=limit):
            messages.append(message)
        return messages

    future = asyncio.run_coroutine_threadsafe(_inner(), loop)
    return future.result()

def media_download(message):
    async def _inner():
        file_path = await tg_app.download_media(message.photo.file_id, file_name="temp_post_photo.jpg")
        with open(file_path, "rb") as f:
            base64_str = base64.b64encode(f.read()).decode("utf-8")
        os.remove(file_path)
        return base64_str

    future = asyncio.run_coroutine_threadsafe(_inner(), loop)
    return future.result()
