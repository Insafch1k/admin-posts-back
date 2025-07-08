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
        if type(res) == int or type(res) == str:
            return jsonify({'success': True, 'response': f'Source was successfully added with id {res} !'})
        else:
            return jsonify({'success': False, 'response': f'Something went wrong! {res}'})
    except Exception as e:
        return jsonify({'success': False, 'response': str(e)})


@sources_bp.route('/update/<int:source_id>', methods=['PATCH'])
def update_source(source_id):
    try:
        data = request.get_json()
        res = SourceBL.update_sources(source_id, updates=data)
        if res:
            return jsonify({'success': True, 'response': f'источник {res} был изменен!'})
    except Exception as e:
        return jsonify({'success': False, 'response': str(e)})


@sources_bp.route('/delete/<int:source_id>', methods=['DELETE'])
def delete_source(source_id):
    try:
        res = SourceBL.delete_source(source_id)
        if res:
            return jsonify({'success': True, 'response': res})
    except Exception as e:
        return jsonify({'success': False, 'response': str(e)})
