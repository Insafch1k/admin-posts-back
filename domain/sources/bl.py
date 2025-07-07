from domain.sources.dal import SourceDAL
from domain.sources.schemas import SourceSchemaOut


class SourceBL:
    @staticmethod
    def get_sources_by_channel_id(channel_id):
        sources = SourceDAL.get_sources_by_channel_id(channel_id)
        if sources:
            # Валидация и сериализация через Pydantic
            validated = [SourceSchemaOut.model_validate(item).model_dump() for item in sources]
            return validated
        return {'error': 'Не получили sources!'}



# print(SourceBL.get_sources_by_channel_id(6))