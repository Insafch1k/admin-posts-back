from flask import Blueprint, jsonify, request
from domain.schedules.bl import ScheduleBL, format_schedule_for_frontend

schedules_bp = Blueprint('schedules', __name__, url_prefix='/schedules')


@schedules_bp.route('/schedule', methods=['GET'])
def get_posts_schedule_route():
    try:
        channel_id = request.args.get('channel_id')
        if channel_id is not None:
            schedule = ScheduleBL.get_posts_schedule_by_channel(int(channel_id))
        else:
            schedule = ScheduleBL.get_posts_schedule()
        posts = format_schedule_for_frontend(schedule)
        return jsonify({"posts": posts})
    except Exception as e:
        return jsonify({"error": str(e), "data": None}), 500