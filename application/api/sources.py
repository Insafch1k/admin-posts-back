from flask import Blueprint, jsonify, request

from domain.sources.bl import SourceBL

sources_bp = Blueprint('sources', __name__, url_prefix='/sources')


@sources_bp.route('/<int:channel_id>', methods=['GET'])
def get_sources_by_channel_id(channel_id):
    sources = SourceBL.get_sources_by_channel_id(channel_id)
    if isinstance(sources, dict) and sources.get("error"):
        return jsonify(sources), 500

    return jsonify(sources)


@sources_bp.route('/add', methods=['POST'])
def add_new_source():
    try:
        data = request.get_json()
        content = data.get('url')
        print(content)
        return jsonify({'success': True, 'response': 'Source was successfully added!'})
    except Exception as e:
        return jsonify({'success': False, 'response': str(e)})
