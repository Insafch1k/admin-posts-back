from domain.sources.dal import SourceDAL
from domain.sources.schemas import SourceSchemaOut
from utils.parse import download_avatar_to_base64, app


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
        source_name = data['url'].rsplit('/', 1)[-1]
        source_photo, source_title = download_avatar_to_base64(app, source_name)



# print(SourceBL.get_sources_by_channel_id(6))