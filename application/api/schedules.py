from flask import Blueprint, jsonify, request
from domain.schedules.bl import ScheduleBL

schedules_bp = Blueprint('schedules', __name__, url_prefix='/schedules')


@schedules_bp.route('/schedule', methods=['GET'])
def get_posts_schedule_route():
    try:
        channel_id = request.args.get('channel_id')
        user_id = request.args.get('user_id')
        if channel_id is not None:
            posts, flags = ScheduleBL.get_posts_schedule_with_flags(int(channel_id))
        else:
            return jsonify({"error": "channel_id is required", "data": None}), 400
        posts_json = ScheduleBL.format_schedule_for_frontend(posts)
        response = {
            "user_id": user_id,
            "channel_id": int(channel_id),
            "posts": posts_json,
            **flags
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e), "data": None}), 500

@schedules_bp.route('/schedule', methods=['POST'])
def save_posts_schedule_route():
    try:
        data = request.get_json()
        channel_id = data.get('channel_id')
        user_id = data.get('user_id')
        posts = data.get('posts', [])
        duplication = data.get('duplication', False)
        dublicationWeek = data.get('dublicationWeek', False)
        random = data.get('random', False)
        if not channel_id or not posts:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        result = ScheduleBL.save_posts_schedule_with_flags(
            channel_id, posts, duplication, dublicationWeek, random
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@schedules_bp.route('/flags', methods=['POST'])
def update_schedule_flags():
    data = request.get_json()
    channel_id = data.get('channel_id')
    duplication = data.get('duplication')
    dublicationWeek = data.get('dublicationWeek')
    random = data.get('random')

    if channel_id is None or duplication is None or dublicationWeek is None or random is None:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    success = ScheduleBL.update_schedule_flags(channel_id, duplication, dublicationWeek, random)
    if not success:
        return jsonify({'success': False, 'error': 'Failed to update flags'}), 400
    return jsonify({'success': True})
