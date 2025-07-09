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

@schedules_bp.route('/update_time', methods=['POST'])
def update_schedule_time():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    publish_time = data.get('publish_time')

    if not (schedule_id and publish_time):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    success, error = ScheduleBL.update_schedule_time(schedule_id, publish_time)
    if not success:
        return jsonify({'success': False, 'error': error}), 400
    return jsonify({'success': True})

@schedules_bp.route('/create', methods=['POST'])
def create_schedule():
    data = request.get_json()
    channel_id = data.get('channel_id')
    post_id = data.get('post_id')
    publish_time = data.get('publish_time')

    if not (channel_id and post_id and publish_time):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    success = ScheduleBL.create_schedule(channel_id, post_id, publish_time)
    return jsonify({'success': success})

@schedules_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post_time(post_id):
    result = ScheduleBL.delete_post_time(post_id)
    if result:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to delete schedule'}), 400

