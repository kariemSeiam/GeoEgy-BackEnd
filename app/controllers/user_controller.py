from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
)
from datetime import datetime
from app.models.user import User
from app.models.search_history import SearchHistory
from app import db
from app.utils.validators import validate_phone_number
from app.utils.security import get_current_user

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone_number = data.get('phone_number')
    validate_phone_number(phone_number)

    user = User.query.filter_by(phone_number=phone_number).first()

    if not user:
        # Automatically register the user
        user = User(phone_number=phone_number, creation_date=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

    if user.is_blocked:
        return jsonify({'code': 403, 'message': 'Account is blocked', 'data': {}}), 403

    access_token = create_access_token(identity={'phone_number': phone_number})
    return jsonify({'code': 200, 'message': 'Login successful', 'data': {'access_token': access_token}})

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user = get_current_user()
    return jsonify({'code': 200, 'message': 'Success', 'data': user.serialize()})

@bp.route('/update_whatsapp', methods=['POST'])
@jwt_required()
def update_whatsapp():
    data = request.get_json()
    whatsapp_number = data.get('whatsapp_number')
    user = get_current_user()
    user.whatsapp_number = whatsapp_number
    db.session.commit()
    return jsonify({'code': 200, 'message': 'WhatsApp number updated', 'data': {}})
