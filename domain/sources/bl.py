from domain.sources.dal import SourceDAL
from domain.sources.schemas import SourceSchemaOut
from utils.downloads.work_with_photo import tg_app, download_avatar_to_base64
from utils.rss.validators import validate_url
import feedparser

def detect_link_type(url: str) -> str:
    if "t.me/" in url or url.startswith("https://t.me/"):
        return "tg_url"
    elif url.endswith(".rss") or url.endswith(".xml") or "rss" in url:
        return "rss_url"
    else:
        return "unknown"


class SourceBL:
    @staticmethod
    def get_sources_by_channel_id(channel_id, type_name):
        sources = SourceDAL.get_sources_by_channel_id(channel_id, type_name)
        if sources:
            # Валидация и сериализация через Pydantic
            validated = [SourceSchemaOut.model_validate(item).model_dump() for item in sources]
            return validated
        return {'error': 'Не получили sources!'}

    @staticmethod
    def get_source_by_source_name(source_name: str):
        source = SourceDAL.get_source_by_source_name(source_name)
        if source:
            validated = SourceSchemaOut.model_validate(source).model_dump()
            return validated
        return {'error': 'Не получили source!'}

    @staticmethod
    def add_source(data):
        if detect_link_type(data['url']) == 'rss_url':
            print('rss_url')
            validated_url = validate_url(data['url'])
            feed = feedparser.parse(validated_url)
            tape_name = feed['feed']['title'] if feed['feed']['title'] else feed['feed']['subtitle']
            tape_photo = feed['feed']['image']['href'] if feed['feed']['image'] else None
            try:
                res = SourceDAL.add_source({
                    'source_name': tape_name,
                    'type_id': 2,
                    'rss_url': data['url'],
                    'channel_id': data['channel_id'],
                    'source_title': tape_name,
                    'source_photo': tape_photo
                })
                return res
            except Exception as e:
                return e
        elif detect_link_type(data['url']) == "tg_url":
            print('tg_url')
            source_name = data['url'].rsplit('/', 1)[-1]
            try:
                source_photo, source_title = download_avatar_to_base64(source_name)
                if source_photo or source_title:
                    res = SourceDAL.add_source({
                        'source_name': source_name,
                        'type_id': 1,
                        'rss_url': data['url'],
                        'channel_id': data['channel_id'],
                        'source_title': source_title,
                        'source_photo': source_photo
                    })
                    return res
            except Exception as e:
                return e
        else:
            raise Exception("Некорректная ссылка была передана!")

    @staticmethod
    def update_sources(source_id, updates):
        res = SourceDAL.update_sources_values(source_id, updates)
        if res:
            return res['source_id']
        else:
            raise Exception("Не удалось обновить данные!")


    @staticmethod
    def delete_source(source_id):
        res = SourceDAL.delete_source(source_id)
        if res:
            return res
        else:
            raise Exception("Не удалось удалить данные!")


# print(SourceBL.add_source({"channel_id": 6, "url": "https://t.me/crypto_vestnic"}))
# print(SourceBL.get_sources_by_channel_id(6))
