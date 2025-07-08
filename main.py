import threading
import signal
import atexit
from application.api import app
from utils.downloads.telegram_client_runner import start_client, stop_client


def shutdown_handler(*args):
    print("🔁 Завершение... Останавливаем Telegram клиент")
    stop_client()


if __name__ == "__main__":
    # Обработчики завершения
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    atexit.register(shutdown_handler)

    # Запуск Telegram клиента в отдельном потоке
    tg_thread = threading.Thread(target=start_client, daemon=True)
    tg_thread.start()

    # Запуск Flask-сервера
    app.run(host="0.0.0.0", port=5000, debug=False)
