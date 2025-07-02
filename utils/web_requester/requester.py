import requests
# from pydantic_core import ValidationError
# from utils.validators.validators import validate_url


# def requester(url):
#     try:
#         valid_url = validate_url(url)
#     except ValidationError as e:
#         raise ValueError(f"Invalid URL {url}", e)
#     headers = {
#         "User-Agent": "RSSFetcher/1.0 (+https://yourapp.com)" # когда-то здесь будет ссылка на наш сайт
#     }
#     try:
#         response = requests.get(
#             url=valid_url,
#             headers=headers,
#             timeout=10
#         )
#         response.raise_for_status()
#         return response.text
#     except requests.exceptions.RequestException as e:
#         raise ValueError(f"Failed to fetch feed from {url}", e)


from newspaper import Article


def parse_article(url):
    try:
        article = Article(url, request_timeout=10)  # Увеличиваем таймаут до 10 секунд
        article.download()
        article.parse()

        return {
            'title': article.title,
            'text': article.text,
            'authors': article.authors,
            'publish_date': article.publish_date,
            'top_image': article.top_image,
            'summary': article.summary
        }
    except Exception as e:
        print(f"Error parsing article: {e}")
        return None


# Пример использования
article_info = parse_article("https://www.rbc.ru/rbcfreenews/685bfdda9a7947be71ff98cc")
print(article_info)

