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

# пример применения
# from utils.is_fit_post import compare_news_with_posts
#
# news_text = "ХАМАС провело консультации для достижения соглашения о прекращении огня ХАМАС провело консультации для обсуждения предложений посредников по перемирию Бойцы ХАМАС  - РИА Новости, 1920, 02.07.2025КАИР, 2 июл - РИА Новости. Палестинское движение ХАМАС заявило, что проводит консультации для обсуждения предложений от посредников для достижения соглашения о прекращении огня в секторе Газа.Движение отметило, что посредники прилагают усилия для достижения рамочного соглашения и начала серьёзных переговоров.Мы действуем с высокой ответственностью и проводим национальные консультации для обсуждения предложений от братьев-посредников ради достижения соглашения, гарантирующего прекращение агрессии и вывод (израильских войск - ред.), - говорится в заявлении ХАМАС."
# posts = ["Программы USAID по Украине в ведении госдепа могут быть прекращены в этом году, пишет Kyiv Post. Рубио накануне заявил, что USAID официально прекращает администрирование программ иностранной помощи, при этом часть из них перейдут как раз в ведение госдепа. Как утверждает издание, у госдепа нет правовых механизмов для управления программами, связанными с Украиной, равно как и плана по их легальной реализации. Речь идет о программах в сферах здравоохранения, энергетики и кибербезопасности.Многие реализаторы этих программ обанкротились... Я очень удивлюсь, если эти контракты доживут до конца года, - полагает экс-чиновник USAID."]
#
# print(compare_news_with_posts(news_text, posts, threshold=0.4))


