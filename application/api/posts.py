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

@posts_bp.route('/update', methods=['POST'])
def update_post():
    data = request.get_json()
    post_id = data.get('post_id')
    name = data.get('name')
    date = data.get('date')
    time_ = data.get('time')

    if not post_id:
        return jsonify({'success': False, 'error': 'post_id is required'}), 400

    success, error = PostsBL.update_post(post_id, name, date, time_)
    if not success:
        return jsonify({'success': False, 'error': error}), 400
    return jsonify({'success': True})

@posts_bp.route('/create', methods=['POST'])
def create_post():
    data = request.get_json()
    channel_id = data.get('channel_id')
    prompt_id = data.get('prompt_id')
    content_name = data.get('content_name')
    content_text = data.get('content_text')
    date = data.get('date')
    time_ = data.get('time')

    if not (channel_id and prompt_id and content_name and content_text and date and time_):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    success = PostsBL.create_post(channel_id, prompt_id, content_name, content_text, date, time_)
    return jsonify({'success': success})