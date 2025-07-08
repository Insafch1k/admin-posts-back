from flask import Blueprint, jsonify, request
from utils.ai.gigachat_client import GigaChatManager
from domain.schedules.bl import ScheduleBL
from domain.posts.bl import PostsBL
from datetime import datetime

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

@posts_bp.route('/update_name', methods=['POST'])
def update_post_name():
    data = request.get_json()
    post_id = data.get('post_id')
    name = data.get('name')

    if not (post_id and name):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    success, error = PostsBL.update_post_name(post_id, name)
    if not success:
        return jsonify({'success': False, 'error': error}), 400
    return jsonify({'success': True})



