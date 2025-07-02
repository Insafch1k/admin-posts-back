from flask import Blueprint, jsonify, request
from domain.channels.bl import ChannelBL
from utils.data_state import DataState
from domain.keywords.dal import KeywordDAL
from domain.styles.dal import StyleDAL
from utils.ai.gigachat_client import GigaChatManager

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/', methods=['POST'])
def get_user_channels():
    try:
        data = request.get_json()

        if not data or 'style' not in data or 'source' not in data:
            return jsonify({
                "message": "Missing required fields",
                "success": False
            }), 400

        style = data['style']
        source = data['source']

        gg_mng = GigaChatManager()

        result = gg_mng.send_message(style, source)
        print(result)
        return jsonify({
            "data": result,
            "error": None
        })

    except Exception as e:
        return jsonify({"error": str(e), "data": None}), 500