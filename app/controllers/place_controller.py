from flask import Blueprint, jsonify, request
from app.models.place import Place
from app.utils.constants import MAX_SEARCH_RESULTS

bp = Blueprint('place', __name__, url_prefix='/place')

@bp.route('/search', methods=['GET'])
def search_places():
    query = request.args.get('query')
    results = Place.query.filter(Place.name.ilike(f'%{query}%')).limit(MAX_SEARCH_RESULTS).all()
    return jsonify({'places': [place.serialize() for place in results]})
