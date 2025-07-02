from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def check_duplicate(new_text, existing_posts, threshold=0.85):
    """
    Проверяет дубликаты через косинусную схожесть TF-IDF векторов
    threshold: 0.85 = 85% схожести считается дублем
    """
    texts = existing_posts + [new_text]
    vectorizer = TfidfVectorizer(stop_words='russian')
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Сравниваем последний текст со всеми предыдущими
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    return any(sim > threshold for sim in similarity[0])