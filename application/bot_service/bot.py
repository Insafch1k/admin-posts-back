import asyncio
import logging
from aiogram import Bot, Dispatcher
from application.bot_service.scheduler import setup_scheduler
from utils.connection_db import connection_db
from utils.config import settings
from utils.database_manager import DatabaseManager
#from application.bot_service.parser_integration import parser_integration

async def main():
    """
    Главная функция для запуска бота.
    """
    logging.basicConfig(level=logging.INFO)

    # Инициализация подключения к БД
    try:
        DatabaseManager.initialize(settings)
        logging.info("Database connection pool initialized.")

    except Exception as e:
        logging.error(f"Could not initialize database connection pool: {e}")
        return

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Настройка и запуск планировщика
    try:
        setup_scheduler(bot)
    except Exception as e:
        logging.error(f"Failed to setup scheduler: {e}")
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