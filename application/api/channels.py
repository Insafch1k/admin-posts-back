from flask import Blueprint, jsonify
from domain.channels.bl import ChannelBL
from utils.data_state import DataState
from domain.keywords.dal import KeywordDAL
from domain.styles.dal import StyleDAL

channels_bp = Blueprint('channel', __name__, url_prefix='/channels')
channel_bl = ChannelBL()


@channels_bp.route('/<int:user_id>', methods=['GET'])
def get_user_channels(user_id: int):
    try:
        result = channel_bl.get_user_channels(user_id)

        if result.error_message:
            return jsonify({"error": result.error_message}), 404 if "не найдены" in result.error_message else 500

        return jsonify({
            "data": [channel.dict() for channel in result.data],
            "error": None
        })

    except Exception as e:
        return jsonify({"error": str(e), "data": None}), 500


@channels_bp.route('/<int:channel_id>/data', methods=['GET'])
def get_channel_data(channel_id: int):
    try:
        keywords_result = KeywordDAL.get_channel_keywords(channel_id)
        styles_result = StyleDAL.get_channel_styles(channel_id)

        if isinstance(keywords_result, DataState) and isinstance(styles_result, DataState):
            return jsonify({
                "keywords": keywords_result.data if keywords_result.data else [],
                "styles": styles_result.data if styles_result.data else [],
                "error": None
            })

        return jsonify({
            "keywords": [],
            "styles": [],
            "error": "Ошибка получения данных"
        }), 500

    except Exception as e:
        return jsonify({
            "keywords": [],
            "styles": [],
            "error": str(e)
        }), 500