import feedparser

# rss_url = "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
# rss_url = "https://subscribe.ru/digest/index.rss"
# rss_url = "https://lenta.ru/rss"
# rss_url = "https://ria.ru/export/rss2/archive/index.xml"
# rss_url = "https://www.vedomosti.ru/rss/news"
# rss_url = "https://www.rt.com/rss/"
rss_url = "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    print("Title:", entry.title)
    print("Link:", entry.link)
    print("Published:", entry.published)

    # Основные варианты получения описания:
    description = entry.get('description')  # Стандартное поле
    summary = entry.get('summary')  # Альтернативное поле
    content = entry.get('content')  # Полное содержимое (может быть списком)

    print("Description:", description)
    print("Summary:", summary)

    # Для полного контента (если есть):
    if hasattr(entry, 'content'):
        for item in entry.content:
            print("Content type:", item.type)
            print("Content value:", item.value)