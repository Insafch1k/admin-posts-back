import feedparser
from itertools import islice

from domain.last_news.dal import LastNewsDAL
from utils.rss.requester import parse_article
from utils.rss.validators import validate_url
from email.utils import parsedate_to_datetime

# rss_url = "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
# rss_url = "https://subscribe.ru/digest/index.rss"
# rss_url = "https://lenta.ru/rss"


# rss_url = "https://ria.ru/export/rss2/archive/index.xml"
# rss_url = "https://www.vedomosti.ru/rss/news"
# rss_url = "https://www.rt.com/rss/"
rss_url = "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"

def parse_entry(entry: dict) -> dict:
    def get_main_link(entry):
        return next(
            (link.get('href') for link in entry.get('links', []) if link.get('rel') == 'alternate'),
            entry.get('link', '')
        )

    def get_image(entry):
        return next(
            (link.get('href') for link in entry.get('links', []) if
             link.get('rel') == 'enclosure' and 'image' in link.get('type', '')),
            None
        )

    parsed = {
        'id': entry.get('id') or entry.get('guid') or '',

        'title': entry.get('title', 'Без названия'),

        'link': get_main_link(entry),

        'summary': entry.get('summary') or entry.get('summary_detail', {}).get('value', ''),

        'published': entry.get('published') or entry.get('updated') or '',

        'author': entry.get('author') or entry.get('author_detail', {}).get('name', 'Не указан'),

        'tags': [tag.get('term', '') for tag in entry.get('tags', [])] if 'tags' in entry else [],

        'image': get_image(entry),  # URL изображения, если есть

        'source': entry.get('source', {}).get('title', '')  # если используется
    }

    return parsed


def parse_rss_feed(channel_id: int = 6, limit: int = 20):
    from domain.sources.bl import SourceBL
    sources = SourceBL.get_sources_by_channel_id(channel_id, type_name='RSS лента')
    result = []
    try:
        for src in sources:
            validated_url = validate_url(src['rss_url'])
            tape_name = src['source_name']
            source_id = int(src['source_id'])
            new_article = {tape_name: []}
            print(f"📡 Парсинг ленты: {tape_name}")
            feed = feedparser.parse(validated_url)
            articles = [entry for entry in islice(feed.entries, limit)]

            last_saved_news = LastNewsDAL.get_last_news_by_source_id(source_id)
            last_article_pub_date = last_saved_news['pub_date'] if last_saved_news else 0
            print(f"🧾 Последний сохранённый pub_date: {last_article_pub_date}")

            newest_article = None

            for a in reversed(articles):
                data = parse_entry(a)
                # print(f"{data['published']}: {data['title']} ({data['link']})")
                if data['published']:
                    dt = parsedate_to_datetime(data['published']).replace(tzinfo=None)
                if dt and dt <= last_article_pub_date:
                    print('2')
                    continue

                full_article = parse_article(data['link'])
                if full_article:
                    data.update(full_article)

                new_article[tape_name].append(data)

                newest_article = data

            if newest_article:
                if last_saved_news:
                    new_news = LastNewsDAL.update_last_news_by_id(last_news_id=last_saved_news['last_news_id'],
                                                                  updates={
                                                                      'description': newest_article['summary'],
                                                                      'pub_date': dt,
                                                                      'title': newest_article['title'],
                                                                      'last_news_photo': newest_article['image'],
                                                                      'url': newest_article['link']
                                                                  })
                else:
                    new_news = LastNewsDAL.insert_last_news(updates={
                        'source_id': source_id,
                        'description': newest_article['summary'],
                        'pub_date': dt,
                        'title': newest_article['title'],
                        'last_news_photo': newest_article['image'],
                        'url': newest_article['link']
                    })
                print(f"\n💾 Сохранено новое сообщение с ID {newest_article['id']}")
            else:
                print("📭 Нет новых сообщений")
            result.append(new_article)

        return result

    except Exception as e:
        print("❌ Ошибка при получении сообщений:", e)


print(parse_rss_feed(6,20))


# def parse_rss_feed(rss_url, limit: int = 10):
#     validated_url = validate_url(rss_url)
#     feed = feedparser.parse(validated_url)
#     print(feed.keys())
#     print()
#     print(feed['feed'])
#     articles = []
#
#     for entry in islice(feed.entries, limit):
#         data = parse_entry(entry)
#         # print(f"{data['published']}: {data['title']} ({data['link']})")
#         if data['published']:
#             dt = parsedate_to_datetime(data['published'])
#         #     print(dt, type(dt))
#         full_article = parse_article(data['link'])
#         if full_article:
#             data.update(full_article)
#
#         articles.append(data)

    # return articles
# parse_rss_feed(rss_url, limit=1)