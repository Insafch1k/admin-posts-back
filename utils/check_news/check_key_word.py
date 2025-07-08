

def is_news_relevant(news_text, keywords, min_keyword_matches=1):
    """
    Проверяет, подходит ли новость для публикации на основе ключевых слов.

    Args:
        news_text (str): Текст новости из источника.
        keywords (list): Список ключевых слов для проверки релевантности.
        min_keyword_matches (int): Минимальное количество совпадений ключевых слов для признания новости подходящей.

    Returns:
        bool: True, если новость релевантна, False в противном случае.
    """
    # Приведение текста новости и ключевых слов к нижнему регистру для регистронезависимого поиска
    news_text = news_text.lower()
    keywords = [keyword.lower() for keyword in keywords]

    # Подсчет совпадений ключевых слов
    match_count = sum(1 for keyword in keywords if keyword in news_text)

    # Проверка, достаточно ли совпадений
    return match_count >= min_keyword_matches