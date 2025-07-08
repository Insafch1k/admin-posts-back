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
        res = SourceBL.add_source(data)
        if res:
            return jsonify({'success': True, 'response': f'Source was successfully added with id {res} !'})
        else:
            return jsonify({'success': False, 'response': 'Something went wrong!'})
    except Exception as e:
        return jsonify({'success': False, 'response': str(e)})
