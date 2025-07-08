from domain.sources.dal import SourceDAL
from domain.sources.schemas import SourceSchemaOut
from utils.downloads.work_with_photo import tg_app, download_avatar_to_base64


def detect_link_type(url: str) -> str:
    if "t.me/" in url or url.startswith("https://t.me/"):
        return "tg_url"
    elif url.endswith(".rss") or url.endswith(".xml") or "rss" in url:
        return "rss_url"
    else:
        return "unknown"


class SourceBL:
    @staticmethod
    def get_sources_by_channel_id(channel_id):
        sources = SourceDAL.get_sources_by_channel_id(channel_id)
        if sources:
            # Валидация и сериализация через Pydantic
            validated = [SourceSchemaOut.model_validate(item).model_dump() for item in sources]
            return validated
        return {'error': 'Не получили sources!'}

    @staticmethod
    def add_source(data):
        if detect_link_type(data['url']) == 'rss_url':
            pass
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
            return dict(res)['source_id']
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
