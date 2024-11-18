from flask import Blueprint, jsonify, request
from app.models.user import  User
from .. import db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/login', methods=['POST'])
def login_or_create_user():
    phone_number = request.json.get('phone_number')
    user = User.query.filter_by(phone_number=phone_number).first()

    if not user:
        # Create new user if not exists
        new_user = User(phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})

    # Example: Implement authentication logic (generate token, session management)
    # Example: session['user_id'] = user.id
    return jsonify({'message': 'Login successful'})

@bp.route('/get_profile', methods=['GET'])
def get_user_profile():
    phone_number = request.args.get('phone_number')
    if not phone_number:
        abort(400, 'Phone number is required')  # Bad request if phone number is missing
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        abort(404, 'User not found')  # User not found
    user_data = user.serialize()
    return jsonify({'user': user_data})
