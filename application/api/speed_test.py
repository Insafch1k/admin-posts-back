from flask import Blueprint, jsonify
from domain.posts.bl import newPostBL
speed_bp = Blueprint('speed', __name__, url_prefix='/speed')

@speed_bp.route('/', methods=['GET'])
def get_speed():
    return jsonify(newPostBL.speed_test())