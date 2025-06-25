from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
import gigachat.context
from ai_api import system_prompt
from dotenv import load_dotenv, find_dotenv
import os
from typing import Optional, Dict
import logging
import json
import requests
from readability import Document
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv(find_dotenv())

class GigaChatManager:
    def __init__(self, temperature: float = 0.7, max_tokens: int = 2000):
        """
        Инициализация менеджера GigaChat

        :param temperature: Температура генерации (0.0 - 1.0)
        :param max_tokens: Максимальное количество токенов в ответе
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        try:
            auth_token = os.getenv('AUTH')
            if not auth_token:
                raise ValueError("AUTH token not found in environment variables")
            
            self.giga = GigaChat(
                credentials=auth_token,
                verify_ssl_certs=False,
                temperature=temperature,
                max_tokens=max_tokens
            )
            logger.info("GigaChat client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GigaChat client: {str(e)}")
            raise

    def _extract_content(self, url: str) -> str:
        """
        Извлечение основного контента из веб-страницы

        :param url: URL страницы
        :return: Извлеченный текст
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            doc = Document(response.text)
            return doc.summary()
        except Exception as e:
            logger.error(f"Error extracting content from URL: {str(e)}")
            raise

    def send_message(self, user_message: str, is_first_msg: bool = False) -> AIMessage:
        """
        Отправка сообщения

        :param user_message: Текст сообщения пользователя
        :param is_first_msg: Флаг первого сообщения в диалоге
        :return: Ответ модели (AIMessage)
        """
        try:
            messages = []
            if is_first_msg:
                messages.append(SystemMessage(content=system_prompt))
            
            messages.append(HumanMessage(content=user_message))
            response = self.giga.invoke(messages)
            return response
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise

    def rewrite_post(self, title: str, link: str, pubdate: str) -> Dict[str, str]:
        """
        Переписывает пост в заданном стиле

        :param title: Заголовок поста
        :param link: Ссылка на пост
        :param pubdate: Дата публикации
        :return: Словарь с переработанным заголовком и описанием
        """
        try:
            # Извлекаем контент из URL
            content = self._extract_content(link)
            
            # Формируем промпт для рерайта
            prompt = f"""Перепиши следующий текст в ярком новостном стиле.
            
Заголовок: {title}
Дата публикации: {pubdate}
Текст: {content}

Верни ответ в формате JSON с полями:
- title: переработанный заголовок
- description: переработанный текст"""
            
            response = self.send_message(prompt, is_first_msg=True)
            
            # Парсим JSON из ответа
            try:
                result = json.loads(response.content)
                return {
                    "title": result.get("title", ""),
                    "description": result.get("description", "")
                }
            except json.JSONDecodeError:
                # Если не удалось распарсить JSON, возвращаем как есть
                return {
                    "title": title,
                    "description": response.content
                }
                
        except Exception as e:
            logger.error(f"Error rewriting post: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        giga_manager = GigaChatManager(temperature=0.7, max_tokens=2000)
        test_data = {
            "title": "",
            "link": "https://thebell.io/chto-izvestno-i-chego-my-ne-znaem-o-terakte-v-krokuse",
            "pubdate": "2024-03-20T10:00:00"
        }
        result = giga_manager.rewrite_post(
            title=test_data["title"],
            link=test_data["link"],
            pubdate=test_data["pubdate"]
        )
        print("Result:", json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")