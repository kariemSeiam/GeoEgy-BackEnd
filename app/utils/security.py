from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def get_current_user():
    from app.models.user import User
    identity = get_jwt_identity()
    user = User.query.filter_by(phone_number=identity['phone_number']).first()
    return user

def handle_unauthorized():
    return jsonify({'code': 401, 'message': 'Unauthorized', 'data': {}}), 401

def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user = get_current_user()
        if not user.is_admin:
            return jsonify({'code': 403, 'message': 'Forbidden', 'data': {}}), 403
        return f(*args, **kwargs)
    return decorator
