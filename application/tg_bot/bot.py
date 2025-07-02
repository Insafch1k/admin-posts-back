import asyncio
import logging
from aiogram import Bot, Dispatcher
from utils.config import settings
from application.tg_bot.scheduler import setup_scheduler
from domain.database import db_manager

async def main():
    """
    Главная функция для запуска бота.
    """
    logging.basicConfig(level=logging.INFO)
    
    # Инициализация подключения к БД
    try:
        db_manager.init_db()
        logging.info("Database connection initialized.")
    except Exception as e:
        logging.error(f"Could not initialize database connection: {e}")
        return

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Настройка и запуск планировщика
    try:
        setup_scheduler(bot)
    except Exception as e:
        logging.error(f"Failed to setup scheduler: {e}")
        # Decide if you want to continue without the scheduler
        # For this use case, probably not.
        return

    # Перед запуском polling'а удаляем вебхук, чтобы избежать конфликтов
    await bot.delete_webhook(drop_pending_updates=True)
    
    logging.info("Starting bot polling...")
    await dp.start_polling(bot)

def run_bot():
    """
    Запускает бота.
    """
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")


if __name__ == "__main__":
    run_bot()
