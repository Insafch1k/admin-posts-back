import re
import pymorphy3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Инициализация pymorphy3 и NLTK
morph = pymorphy3.MorphAnalyzer()
stop_words = set(stopwords.words("russian"))


def preprocess_text(text):
    """Предобработка текста: приведение к нижнему регистру, токенизация, лемматизация, удаление стоп-слов."""
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [morph.parse(word)[0].normal_form for word in tokens if word.isalnum() and word not in stop_words]
    return " ".join(tokens)


def compare_news_with_posts(news_text, posts, threshold=0.1):
    """
    Сравнивает текст новости с постами. Возвращает True, если новость можно использовать
    (нет совпадений выше порога), и False, если есть совпадение выше порога.

    Args:
        news_text (str): Текст новости.
        posts (list): Список текстов постов.
        threshold (float): Порог схожести (по умолчанию 0.4, т.е. 40%).

    Returns:
        bool: True, если новость уникальна, False, если есть совпадение выше порога.
        list: Список кортежей (пост, сходство) для постов с наибольшим сходством.
    """
    # Предобработка
    processed_news = preprocess_text(news_text)
    processed_posts = [preprocess_text(post) for post in posts]

    # Векторизация
    all_texts = [processed_news] + processed_posts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Сравнение
    news_vector = tfidf_matrix[0]
    post_vectors = tfidf_matrix[1:]
    similarities = cosine_similarity(news_vector, post_vectors)[0]

    # Составляем результаты
    results = sorted(zip(posts, similarities), key=lambda x: x[1], reverse=True)
    print(results)
    # Проверяем, есть ли посты с сходством выше порога
    max_similarity = max(similarities) if similarities.size > 0 else 0
    can_use_news = max_similarity < threshold

    return can_use_news


