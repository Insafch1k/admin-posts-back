import asyncio
from pyrogram import Client
from utils.config import settings

api_id = settings.API_ID
api_hash = settings.API_HASH
phone = settings.PHONE
login = settings.LOGIN

# Telegram client
tg_app = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)
loop = asyncio.new_event_loop()

def start_client():
    asyncio.set_event_loop(loop)

    async def runner():
        await tg_app.start()
        print("✅ Telegram клиент запущен")
        await asyncio.Event().wait()  # Чтобы клиент не остановился

    loop.run_until_complete(runner())

def stop_client():
    async def stopper():
        await tg_app.stop()
        print("❌ Telegram клиент остановлен")

    loop.call_soon_threadsafe(asyncio.create_task, stopper())
    loop.call_soon_threadsafe(loop.stop)



