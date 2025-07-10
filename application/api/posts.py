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
    content_name = data.get('content_name')
    time_ = data.get('time')

    if not (post_id and content_name and time_):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    success_name, error_name = PostsBL.update_post_name(post_id, content_name)
    success_time, error_time = PostsBL.update_time_by_post_id(post_id, time_)

    if not success_name or not success_time:
        return jsonify({'success': False, 'error': error_name or error_time}), 400
    return jsonify({'success': True})

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    result = PostsBL.delete_post(post_id)
    if result:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to delete post'}), 400

@posts_bp.route('/create', methods=['POST'])
def create_post():
    data = request.get_json()
    content_name = data.get('content_name')
    content_text = data.get('content_text')
    date = data.get('date')
    time_ = data.get('time')
    channel_id = data.get('channel_id')
    prompt_id = data.get('prompt_id')

    if not (content_name and content_text and date and time_ and channel_id and prompt_id):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    post_id = PostsBL.create_post_and_return_id(
        content_name=content_name,
        content_text=content_text,
        date=date,
        time_=time_,
        channel_id=channel_id,
        prompt_id=prompt_id
    )
    if not post_id:
        return jsonify({'success': False, 'error': 'Failed to create post'}), 400

    return jsonify({'success': True, 'post_id': post_id})