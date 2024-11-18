from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.order import Order
from app.models.governorate import Governorate
from app.models.user import User
from app import db
from app.utils.security import get_current_user
from app.utils.validators import ValidationError

bp = Blueprint('order', __name__, url_prefix='/api/order')

@bp.route('/place', methods=['POST'])
@jwt_required()
def place_order():
    data = request.get_json()
    user = get_current_user()

    if user.is_blocked:
        return jsonify({'code': 403, 'message': 'Account is blocked', 'data': {}}), 403

    place_name = data.get('place_name')
    business_details = data.get('business_details')
    selected_govs = data.get('selected_govs')  # List of governorate names
    whatsapp_number = data.get('whatsapp_number')

    if not all([place_name, selected_govs]):
        raise ValidationError('Place name and selected governorates are required')

    # Update user's WhatsApp number if provided
    if whatsapp_number:
        user.whatsapp_number = whatsapp_number
        db.session.commit()

    # Calculate total_price
    if 'كل محافظات مصر' in selected_govs:
        # Custom price for all governorates
        total_price = 4000  # Assuming a fixed price
    else:
        govs = Governorate.query.filter(Governorate.name.in_(selected_govs)).all()
        total_price = sum([gov.price for gov in govs])

    order = Order(
        user_id=user.id,
        place_name=place_name,
        business_details=business_details,
        selected_govs=','.join(selected_govs),
        total_price=total_price,
        status='Awaiting Payment Confirmation'
    )
    db.session.add(order)
    db.session.commit()

    return jsonify({'code': 201, 'message': 'Order placed successfully', 'data': order.serialize()})

@bp.route('/my_orders', methods=['GET'])
@jwt_required()
def my_orders():
    user = get_current_user()
    orders = Order.query.filter_by(user_id=user.id).all()
    return jsonify({'code': 200, 'message': 'Success', 'data': [order.serialize() for order in orders]})
