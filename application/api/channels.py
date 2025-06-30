from flask import Blueprint, jsonify
from domain.channels.bl import ChannelBL
from utils.data_state import DataState

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