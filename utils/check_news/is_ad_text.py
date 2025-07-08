import re
from typing import List, Optional


def is_advertisement(
        text: str,
        ad_keywords: Optional[List[str]] = None,
        max_link_count: int = 2,
        max_exclamation_ratio: float = 0.1,
        max_caps_ratio: float = 0.3,
) -> bool:
    """
    Определяет, является ли текст рекламным сообщением.

    Параметры:
        text (str): Текст для анализа.
        ad_keywords (List[str], optional): Список ключевых слов, характерных для рекламы.
            Если не указан, используется стандартный набор.
        max_link_count (int): Максимальное количество ссылок, после которого текст считается рекламой.
        max_exclamation_ratio (float): Допустимая доля восклицательных знаков (от общего кол-ва символов).
        max_caps_ratio (float): Допустимая доля заглавных букв (от общего кол-ва символов).

    Возвращает:
        bool: True, если текст похож на рекламу, иначе False.
    """
    if not text.strip():
        return False

    # Стандартные ключевые слова для рекламы
    default_ad_keywords = [
        "купить", "продажа", "акция", "скидка", "распродажа",
        "только сегодня", "специальное предложение", "заказать",
        "бесплатно", "доставка", "гарантия", "оформляйте",
        "подпишитесь", "переходите", "реклама", "промокод",
        "по промокоду", "успейте", "ограниченное количество"
    ]

    ad_keywords = ad_keywords or default_ad_keywords

    # 1. Проверка по ключевым словам
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in ad_keywords):
        return True

    # 2. Проверка на обилие ссылок
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    links = url_pattern.findall(text)
    if len(links) > max_link_count:
        return True

    # 3. Проверка на агрессивное форматирование (много восклицательных знаков и капса)
    total_chars = len(text)

    if total_chars > 0:
        exclamation_count = text.count('!') + text.count('‼')
        exclamation_ratio = exclamation_count / total_chars
        if exclamation_ratio > max_exclamation_ratio:
            return True

        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / total_chars
        if caps_ratio > max_caps_ratio:
            return True

    return False