from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.place import Place
from app.models.search_history import SearchHistory
from app import db, limiter
from app.utils.security import get_current_user
from sqlalchemy import or_

bp = Blueprint('search', __name__, url_prefix='/api/search')

@bp.route('/places', methods=['GET'])
@jwt_required()
@limiter.limit("20 per minute")
def search_places():
    query = request.args.get('query')
    if not query:
        return jsonify({'code': 400, 'message': 'Query parameter is required', 'data': {}}), 400

    user = get_current_user()

    # Save search history
    search_history = SearchHistory(user_id=user.id, search_query=query)
    db.session.add(search_history)
    db.session.commit()

    # Search logic
    results = Place.query.filter(
        or_(
            Place.name.ilike(f'%{query}%'),
            Place.about.ilike(f'%{query}%'),
            Place.category.ilike(f'%{query}%'),
            Place.address.ilike(f'%{query}%'),
        )
    ).limit(8).all()

    return jsonify({'code': 200, 'message': 'Success', 'data': [place.serialize() for place in results]})
